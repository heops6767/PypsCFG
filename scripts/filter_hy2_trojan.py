import base64
import urllib.request
from pathlib import Path

# ---------------- CONFIG ----------------
BLACK_SOURCES = ["BlackList", "FavoriteSubBlack", "LiteBlackList"]
WHITE_SOURCES = ["WhiteList", "LiteWhiteList"]

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------- SCORE ----------------
def get_score(line: str) -> int:
    low = line.lower()
    score = 0

    if "trojan://" in low:
        score += 100
    if "hysteria2://" in low or "hy2://" in low:
        score += 80

    # бонусы (если есть — хорошо, если нет — не важно)
    if "reality" in low:
        score += 30
    if "tls" in low:
        score += 20
    if "sni=" in low:
        score += 10

    return score


# ---------------- FETCH ----------------
def fetch_content(source: str) -> str:
    source = source.strip()

    if source.startswith("http"):
        try:
            print(f"[FETCH] {source}")
            req = urllib.request.Request(
                source,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                data = r.read().decode("utf-8", errors="ignore")
                print(f"[OK] size={len(data)}")
                return data
        except Exception as e:
            print(f"[ERROR] {source} -> {e}")
            return ""

    path = Path(source)
    if path.exists():
        data = path.read_text(encoding="utf-8", errors="ignore")
        print(f"[LOCAL] {source} size={len(data)}")
        return data

    print(f"[MISS] {source}")
    return ""


# ---------------- BASE64 ----------------
def try_decode_base64(content: str) -> str:
    try:
        decoded = base64.b64decode(content, validate=True)
        text = decoded.decode("utf-8", errors="ignore")

        if "://" in text:
            print("[B64] decoded OK")
            return text

    except Exception:
        pass

    return content


# ---------------- PARSER ----------------
def extract_links(content: str):
    links = []

    for line in content.splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "://" in line:
            links.append(line.split()[0])

    return links


def filter_links(links):
    result = []

    for link in links:
        low = link.lower()

        if (
            "trojan://" in low or
            "hysteria2://" in low or
            "hy2://" in low
        ):
            result.append(link)

    return result


# ---------------- PROCESS ----------------
def process_list(files_list):
    unique_links = set()

    for filename in files_list:
        print(f"\n=== {filename} ===")

        content = fetch_content(filename)
        if not content:
            continue

        content = try_decode_base64(content)

        raw_links = extract_links(content)

        if any("trojan://" in x.lower() or "hysteria2://" in x.lower() for x in raw_links):
            print(f"[FOUND] {filename} has target protocols")
        else:
            print(f"[EMPTY] {filename}")

        filtered = filter_links(raw_links)

        for link in filtered:
            unique_links.add(link)

    print(f"\n[TOTAL] {len(unique_links)} links found\n")

    return sorted(unique_links, key=get_score, reverse=True)


# ---------------- SAVE ----------------
def save_output(name_prefix, links):
    content = "\n".join(links) + "\n"

    txt_file = OUTPUT_DIR / f"{name_prefix}Hy2Trojan.txt"
    b64_file = OUTPUT_DIR / f"{name_prefix}Hy2Trojan.b64"

    txt_file.write_text(content, encoding="utf-8")
    b64_file.write_text(
        base64.b64encode(content.encode()).decode(),
        encoding="utf-8"
    )

    print(f"[SAVE] {txt_file} ({len(links)} lines)")


# ---------------- MAIN ----------------
def main():
    black = process_list(BLACK_SOURCES)
    save_output("Black", black)

    white = process_list(WHITE_SOURCES)
    save_output("White", white)

    print(f"\nDONE → Black: {len(black)} | White: {len(white)}")


if __name__ == "__main__":
    main()
