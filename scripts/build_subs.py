import base64
import json
import os
import re
import socket
import time
import urllib.parse
import urllib.request
from pathlib import Path

INPUT_FILES = ["BlackList", "WhiteList", "FavoriteSubBlack"]
OUTPUT_DIR = Path("output")
REPORT_DIR = Path("reports")
OUTPUT_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

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

fetch_log = []
filter_log = []
ping_log = []


def is_url(s: str) -> bool:
    s = s.strip()
    return s.startswith("http://") or s.startswith("https://")


def fetch_text(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 PypsCFG-Actions",
            "Accept": "*/*",
        },
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        raw = resp.read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="ignore")


def looks_like_base64_blob(text: str) -> bool:
    s = "".join(text.strip().split())
    if not s or len(s) < 16:
        return False
    if re.search(r"(://)|[\r\n]", text):
        return False
    return re.fullmatch(r"[A-Za-z0-9+/=]+", s) is not None


def try_decode_base64_text(text: str) -> str:
    s = "".join(text.strip().split())
    pad = (-len(s)) % 4
    s += "=" * pad
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
    label = label.strip()
    if not label:
        return ""
    label = label.split("|", 1)[0].strip()
    label = label.split(" ", 1)[0].strip()
    return label


def normalize_non_vmess(line: str) -> str:
    line = line.strip()
    main = line
    label = ""

    if "#" in line:
        main, frag = line.split("#", 1)
        label = short_label(urllib.parse.unquote(frag))
    else:
        main = line.split("|", 1)[0].strip()

    main = main.strip()
    if label:
        return f"{main}#{label}"
    return main


def decode_vmess_payload(payload: str):
    s = payload.strip()
    pad = (-len(s)) % 4
    s += "=" * pad
    raw = base64.b64decode(s)
    return json.loads(raw.decode("utf-8", errors="ignore"))


def encode_vmess_payload(data: dict) -> str:
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return "vmess://" + base64.b64encode(raw.encode("utf-8")).decode("ascii")


def normalize_vmess(line: str) -> str:
    payload = line[len("vmess://"):].strip()
    data = decode_vmess_payload(payload)

    label = short_label(str(data.get("ps", "")).strip())

    for k in ["ps"]:
        data.pop(k, None)

    normalized = json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    if label:
        return f"vmess-json:{normalized}#${label}"
    return f"vmess-json:{normalized}"


def extract_host_port(line: str):
    try:
        if line.startswith("vmess://"):
            data = decode_vmess_payload(line[len("vmess://"):].strip())
            host = str(data.get("add", "")).strip()
            port = int(str(data.get("port", "")).strip())
            return host, port

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


def tcp_check(host: str, port: int, timeout=3.5):
    started = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            elapsed = round((time.time() - started) * 1000)
            return True, elapsed
    except Exception:
        elapsed = round((time.time() - started) * 1000)
        return False, elapsed


def keep_protocol(line: str) -> bool:
    low = line.lower()
    if low.startswith(BLOCKED_PREFIXES):
        return False
    if low.startswith(ALLOWED_PREFIXES):
        return True
    return False


def normalize_key(line: str) -> str:
    if line.startswith("vmess://"):
        try:
            return normalize_vmess(line)
        except Exception:
            return "BROKEN_VM:" + line.strip()
    return normalize_non_vmess(line)


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
    src_path = Path(filename)
    if not src_path.exists():
        fetch_log.append(f"MISSING FILE {filename}")
        return []

    raw_lines = split_lines(src_path.read_text(encoding="utf-8", errors="ignore"))

    expanded = []
    for line in raw_lines:
        expanded.extend(collect_from_source(line))

    final = []
    seen = set()

    for line in expanded:
        line = line.strip()
        if not line:
            continue

        if not keep_protocol(line):
            filter_log.append(f"DROP unsupported/blocked :: {line[:180]}")
            continue

        key = normalize_key(line)
        if key in seen:
            filter_log.append(f"DROP duplicate key :: {key}")
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
    b64_path.write_text(base64.b64encode(txt.encode("utf-8")).decode("ascii"), encoding="utf-8")


def ping_report(lines, name: str):
    report_lines = []
    for line in lines:
        host, port = extract_host_port(line)
        if not host or not port:
            report_lines.append(f"SKIP ??:?? :: {line[:180]}")
            continue
        ok, ms = tcp_check(host, port)
        status = "OK" if ok else "FAIL"
        report_lines.append(f"{status} {ms}ms {host}:{port} :: {line[:180]}")
    (REPORT_DIR / f"{name}_ping.txt").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    ping_log.extend(report_lines)


def main():
    all_merged = []
    global_seen = set()

    per_file = {}

    for name in INPUT_FILES:
        lines = process_input_file(name)
        per_file[name] = lines
        save_txt_and_b64(name, lines)
        ping_report(lines, name)

        for line in lines:
            key = normalize_key(line)
            if key in global_seen:
                continue
            global_seen.add(key)
            all_merged.append(line)

    save_txt_and_b64("merged_all", all_merged)

    (REPORT_DIR / "fetch_report.txt").write_text("\n".join(fetch_log) + "\n", encoding="utf-8")
    (REPORT_DIR / "filtered_report.txt").write_text("\n".join(filter_log) + "\n", encoding="utf-8")
    (REPORT_DIR / "summary.txt").write_text(
        "\n".join(
            [
                f"{name}: {len(per_file[name])}" for name in INPUT_FILES
            ] + [f"merged_all: {len(all_merged)}"]
        ) + "\n",
        encoding="utf-8"
    )

    print("Done.")
    for name in INPUT_FILES:
        print(f"{name}: {len(per_file[name])}")
    print(f"merged_all: {len(all_merged)}")


if __name__ == "__main__":
    main()
