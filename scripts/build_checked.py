import asyncio
import base64
import json
import re
import socket
import time
import urllib.parse
import urllib.request
from pathlib import Path

INPUT_FILES = [
    "BlackList",
    "WhiteList",
    "FavoriteSubBlack",
    "LiteBlackList",
    "LiteWhiteList",
]

OUTPUT_DIR = Path("output")
REPORT_DIR = Path("reports")
CACHE_DIR = Path("cache")

OUTPUT_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

ALLOWED_PREFIXES = (
    "vless://",
    "vmess://",
    "trojan://",
    "hysteria2://",
    "hy2://",
    "tuic://",
)

BLOCKED_PREFIXES = (
    "ss://",
    "ssr://",
)

CONNECT_TIMEOUT = 1.2
CONCURRENCY = 100
CACHE_TTL_SECONDS = 60 * 60 * 24  # 24 hours

fetch_log = []
filter_log = []
checked_log = []


def is_url(s: str) -> bool:
    s = s.strip()
    return s.startswith("http://") or s.startswith("https://")


def fetch_text(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 PypsCFG-Checked",
            "Accept": "*/*",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read()
    return raw.decode("utf-8", errors="ignore")


def looks_like_base64_blob(text: str) -> bool:
    s = "".join(text.strip().split())
    if not s or len(s) < 16:
        return False
    if "://" in text:
        return False
    return re.fullmatch(r"[A-Za-z0-9+/=]+", s) is not None


def try_decode_base64_text(text: str) -> str:
    s = "".join(text.strip().split())
    s += "=" * ((4 - len(s) % 4) % 4)
    try:
        decoded = base64.b64decode(s)
        out = decoded.decode("utf-8", errors="ignore")
        if "://" in out or "\n" in out:
            return out
    except Exception:
        pass
    return text


def split_lines(text: str):
    return [x.strip() for x in text.replace("\r", "\n").split("\n") if x.strip()]


def short_label(label: str) -> str:
    label = urllib.parse.unquote(label.strip())
    if not label:
        return ""
    label = label.split("|", 1)[0].strip()
    label = label.split(" ", 1)[0].strip()
    return label


def keep_protocol(line: str) -> bool:
    low = line.lower().strip()
    if low.startswith(BLOCKED_PREFIXES):
        return False
    return low.startswith(ALLOWED_PREFIXES)


def decode_vmess_payload(payload: str):
    s = payload.strip()
    s += "=" * ((4 - len(s) % 4) % 4)
    raw = base64.b64decode(s)
    return json.loads(raw.decode("utf-8", errors="ignore"))


def vmess_dup_key(line: str) -> str:
    data = decode_vmess_payload(line[len("vmess://"):].strip())
    label = short_label(str(data.get("ps", "")))
    data.pop("ps", None)

    normalized = json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    if label:
        return f"vmess::{normalized}##{label}"
    return f"vmess::{normalized}"


def non_vmess_dup_key(line: str) -> str:
    line = line.strip()

    if "#" in line:
        main, frag = line.split("#", 1)
        label = short_label(frag)
        if label:
            return f"{main.strip()}##{label}"
        return main.strip()

    main = line.split("|", 1)[0].strip()
    return main


def duplicate_key(line: str) -> str:
    if line.startswith("vmess://"):
        try:
            return vmess_dup_key(line)
        except Exception:
            return f"broken-vmess::{line.strip()}"
    return non_vmess_dup_key(line)


def extract_endpoint(line: str):
    try:
        if line.startswith("vmess://"):
            data = decode_vmess_payload(line[len("vmess://"):].strip())
            host = str(data.get("add", "")).strip()
            port = str(data.get("port", "")).strip()
            if host and port:
                return host, int(port)
            return None, None

        core = line.split("|", 1)[0]
        core = core.split("#", 1)[0]
        parsed = urllib.parse.urlsplit(core)
        host = parsed.hostname
        port = parsed.port
        if host and port:
            return host, int(port)
    except Exception:
        return None, None
    return None, None


def collect_from_source(source_line: str):
    source_line = source_line.strip()
    if not source_line or source_line.startswith("#"):
        return []

    if is_url(source_line):
        try:
            text = fetch_text(source_line)
            fetch_log.append(f"OK URL {source_line}")
        except Exception as e:
            fetch_log.append(f"FAIL URL {source_line} :: {e}")
            return []

        if looks_like_base64_blob(text):
            decoded = try_decode_base64_text(text)
            if decoded != text:
                fetch_log.append(f"DECODED base64 from {source_line}")
            text = decoded

        return split_lines(text)

    return [source_line]


def process_input_file(filename: str):
    path = Path(filename)
    if not path.exists():
        fetch_log.append(f"MISSING FILE {filename}")
        return []

    source_lines = split_lines(path.read_text(encoding="utf-8", errors="ignore"))

    expanded = []
    for line in source_lines:
        expanded.extend(collect_from_source(line))

    final = []
    seen = set()

    for line in expanded:
        line = line.strip()
        if not line:
            continue

        if not keep_protocol(line):
            filter_log.append(f"DROP unsupported/blocked :: {line[:200]}")
            continue

        key = duplicate_key(line)
        if key in seen:
            filter_log.append(f"DROP duplicate :: {key}")
            continue

        seen.add(key)
        final.append(line)

    return final


def save_txt_and_b64(name: str, lines):
    txt_path = OUTPUT_DIR / f"{name}.txt"
    b64_path = OUTPUT_DIR / f"{name}.b64"

    txt = "\n".join(lines).strip()
    if txt:
        txt += "\n"

    txt_path.write_text(txt, encoding="utf-8")
    b64_path.write_text(
        base64.b64encode(txt.encode("utf-8")).decode("ascii"),
        encoding="utf-8",
    )


def load_cache():
    path = CACHE_DIR / "endpoint_cache.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_cache(cache: dict):
    path = CACHE_DIR / "endpoint_cache.json"
    path.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


async def check_one(host: str, port: int, timeout: float):
    started = time.perf_counter()
    try:
        fut = asyncio.open_connection(host, port)
        reader, writer = await asyncio.wait_for(fut, timeout=timeout)
        elapsed = round((time.perf_counter() - started) * 1000)
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass
        return True, elapsed
    except Exception:
        elapsed = round((time.perf_counter() - started) * 1000)
        return False, elapsed


async def check_endpoints(endpoints: list):
    sem = asyncio.Semaphore(CONCURRENCY)
    cache = load_cache()
    now = int(time.time())
    results = {}

    async def worker(host: str, port: int):
        key = f"{host}:{port}"

        cached = cache.get(key)
        if cached and now - int(cached.get("ts", 0)) < CACHE_TTL_SECONDS:
            results[key] = {
                "ok": bool(cached.get("ok", False)),
                "ms": int(cached.get("ms", 9999)),
                "cached": True,
            }
            return

        async with sem:
            ok, ms = await check_one(host, port, CONNECT_TIMEOUT)
            results[key] = {
                "ok": ok,
                "ms": ms,
                "cached": False,
            }
            cache[key] = {
                "ok": ok,
                "ms": ms,
                "ts": now,
            }

    await asyncio.gather(*(worker(h, p) for h, p in endpoints))
    save_cache(cache)
    return results


def write_endpoint_report(name: str, endpoints: list, results: dict):
    lines = []
    for host, port in endpoints:
        key = f"{host}:{port}"
        item = results.get(key, {})
        ok = item.get("ok", False)
        ms = item.get("ms", 9999)
        cached = item.get("cached", False)
        status = "OK" if ok else "FAIL"
        suffix = " cached" if cached else ""
        lines.append(f"{status} {ms}ms {host}:{port}{suffix}")

    (REPORT_DIR / f"{name}_Checked_endpoints.txt").write_text(
        "\n".join(lines) + ("\n" if lines else ""),
        encoding="utf-8",
    )


def write_summary(per_file: dict, checked_per_file: dict, merged_checked: list):
    lines = []
    for name in INPUT_FILES:
        raw_count = len(per_file.get(name, []))
        checked_count = len(checked_per_file.get(name, []))
        lines.append(f"{name}: raw={raw_count}, checked={checked_count}")
    lines.append(f"merged_all_Checked: {len(merged_checked)}")

    (REPORT_DIR / "summary_checked.txt").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main():
    per_file = {}
    checked_per_file = {}

    for name in INPUT_FILES:
        per_file[name] = process_input_file(name)

    endpoint_set = set()
    for lines in per_file.values():
        for line in lines:
            host, port = extract_endpoint(line)
            if host and port:
                endpoint_set.add((host, port))

    endpoints = sorted(endpoint_set)
    print(f"Unique endpoints to check: {len(endpoints)}")

    results = asyncio.run(check_endpoints(endpoints))

    merged_checked = []
    global_seen = set()

    for name in INPUT_FILES:
        raw_lines = per_file[name]
        checked_lines = []

        for line in raw_lines:
            host, port = extract_endpoint(line)
            if not host or not port:
                continue

            endpoint_key = f"{host}:{port}"
            r = results.get(endpoint_key)
            if not r or not r.get("ok"):
                checked_log.append(f"DROP dead endpoint :: {endpoint_key}")
                continue

            checked_lines.append(line)

        checked_per_file[name] = checked_lines
        save_txt_and_b64(f"{name}Checked", checked_lines)

        used_endpoints = []
        used_seen = set()
        for line in checked_lines:
            host, port = extract_endpoint(line)
            if host and port:
                ep = (host, port)
                if ep not in used_seen:
                    used_seen.add(ep)
                    used_endpoints.append(ep)
        write_endpoint_report(name, used_endpoints, results)

        for line in checked_lines:
            key = duplicate_key(line)
            if key in global_seen:
                continue
            global_seen.add(key)
            merged_checked.append(line)

    save_txt_and_b64("merged_all_Checked", merged_checked)

    merged_eps = []
    merged_seen = set()
    for line in merged_checked:
        host, port = extract_endpoint(line)
        if host and port:
            ep = (host, port)
            if ep not in merged_seen:
                merged_seen.add(ep)
                merged_eps.append(ep)
    write_endpoint_report("merged_all", merged_eps, results)

    (REPORT_DIR / "fetch_report_checked.txt").write_text(
        "\n".join(fetch_log) + ("\n" if fetch_log else ""),
        encoding="utf-8",
    )
    (REPORT_DIR / "filtered_report_checked.txt").write_text(
        "\n".join(filter_log + checked_log) + ("\n" if (filter_log or checked_log) else ""),
        encoding="utf-8",
    )
    write_summary(per_file, checked_per_file, merged_checked)

    print("Done checked build.")
    for name in INPUT_FILES:
        print(f"{name}: raw={len(per_file.get(name, []))}, checked={len(checked_per_file.get(name, []))}")
    print(f"merged_all_Checked: {len(merged_checked)}")


if __name__ == "__main__":
    main()
