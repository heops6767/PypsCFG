import base64
import urllib.request
from pathlib import Path

# Конфигурация
BLACK_SOURCES = ["BlackList", "FavoriteSubBlack", "LiteBlackList"]
WHITE_SOURCES = ["WhiteList", "LiteWhiteList"]

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def get_score(line: str) -> int:
    """Приоритет: Trojan с Reality/TLS выше обычного"""
    low = line.lower()
    score = 0
    if "security=reality" in low:
        score += 50
    if "security=tls" in low or "sni=" in low:
        score += 20
    return score


def fetch_content(source: str) -> str:
    source = source.strip()

    if source.startswith("http"):
        try:
            req = urllib.request.Request(
                source, headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.read().decode("utf-8", errors="ignore")
        except Exception as e:
            print(f"[ERROR] Fetch {source}: {e}")
            return ""

    path = Path(source)
    if path.exists():
        return path.read_text(encoding="utf-8", errors="ignore")

    return ""


def try_decode_base64(content: str) -> str:
    """Пытаемся декодировать Base64 безопасно"""
    try:
        decoded = base64.b64decode(content, validate=True)
        return decoded.decode("utf-8", errors="ignore")
    except Exception:
        return content


def process_list(files_list):
    unique_links = set()

    for filename in files_list:
        content = fetch_content(filename)
        if not content:
            continue

        # Попытка декодировать Base64
        decoded = try_decode_base64(content)

        # Если после декода появились ссылки — используем его
        if "://" in decoded:
            content = decoded

        for line in content.splitlines():
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            # 🔥 СТРОГИЙ ФИЛЬТР
            if line.startswith(("trojan://", "hysteria2://", "hy2://")):
                unique_links.add(line.split()[0])

    return sorted(unique_links, key=get_score, reverse=True)


def save_output(name_prefix, links):
    if not links:
        return

    content = "\n".join(links) + "\n"

    txt_file = OUTPUT_DIR / f"{name_prefix}Hy2Trojan.txt"
    b64_file = OUTPUT_DIR / f"{name_prefix}Hy2Trojan.b64"

    txt_file.write_text(content, encoding="utf-8")
    b64_file.write_text(
        base64.b64encode(content.encode()).decode(), encoding="utf-8"
    )


def main():
    black = process_list(BLACK_SOURCES)
    save_output("Black", black)

    white = process_list(WHITE_SOURCES)
    save_output("White", white)

    print(f"Done! Hy2/Trojan found -> Black: {len(black)}, White: {len(white)}")


if __name__ == "__main__":
    main()
