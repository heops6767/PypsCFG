import base64
import json
import re
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


def is_url(s: str) -> bool:
    s = s.strip()
    return s.startswith("http://") or s.startswith("https://")


def fetch_text(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 PypsCFG-Fast",
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


def strip_trash_suffix(line: str) -> str:
    line = line.strip()
    if " | " in line:
        line = line.split(" | ", 1)[0].strip()
    return line


def normalize_label(label: str) -> str:
    label = urllib.parse.unquote(label.strip())
    if not label:
        return ""
    label = label.split("|", 1)[0].strip()
    label = label.split(" ", 1)[0].strip()

    if re.fullmatch(r"\d+", label):
        return ""

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


def duplicate_key(line: str) -> str:
    line = strip_trash_suffix(line)

    if line.startswith("vmess://"):
        try:
            data = decode_vmess_payload(line[len("vmess://"):].strip())
            label = normalize_label(str(data.get("ps", "")))
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
        except Exception:
            return f"broken-vmess::{line}"

    if "#" in line:
        main, frag = line.split("#", 1)
        label = normalize_label(frag)
        if label:
            return f"{main.strip()}##{label}"
        return main.strip()

    return line.strip()


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

    for raw_line in expanded:
        line = strip_trash_suffix(raw_line)
        if not line:
            continue

        if not keep_protocol(line):
            filter_log.append(f"DROP unsupported/blocked :: {raw_line[:200]}")
            continue

        key = duplicate_key(line)
        if key in seen:
            filter_log.append(f"DROP duplicate :: {key}")
            continue

        seen.add(key)
        final.append(line)

    return final


def save_txt_and_b64(name: str, lines):
    txt = "\n".join(lines).strip()
    if txt:
        txt += "\n"

    (OUTPUT_DIR / f"{name}.txt").write_text(txt, encoding="utf-8")
    (OUTPUT_DIR / f"{name}.b64").write_text(
        base64.b64encode(txt.encode("utf-8")).decode("ascii"),
        encoding="utf-8",
    )


def write_summary(per_file: dict, merged_all: list):
    lines = [f"{name}: {len(per_file.get(name, []))}" for name in INPUT_FILES]
    lines.append(f"merged_all: {len(merged_all)}")
    (REPORT_DIR / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    per_file = {}
    merged_all = []
    global_seen = set()

    for name in INPUT_FILES:
        lines = process_input_file(name)
        per_file[name] = lines
        save_txt_and_b64(name, lines)

        for line in lines:
            key = duplicate_key(line)
            if key in global_seen:
                continue
            global_seen.add(key)
            merged_all.append(line)

    save_txt_and_b64("merged_all", merged_all)

    (REPORT_DIR / "fetch_report.txt").write_text(
        "\n".join(fetch_log) + ("\n" if fetch_log else ""),
        encoding="utf-8",
    )
    (REPORT_DIR / "filtered_report.txt").write_text(
        "\n".join(filter_log) + ("\n" if filter_log else ""),
        encoding="utf-8",
    )
    write_summary(per_file, merged_all)

    print("Done.")
    for name in INPUT_FILES:
        print(f"{name}: {len(per_file.get(name, []))}")
    print(f"merged_all: {len(merged_all)}")


if __name__ == "__main__":
    main()
