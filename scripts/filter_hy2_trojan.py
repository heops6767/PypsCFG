import base64
import urllib.request
from pathlib import Path

BLACK_SOURCES = [
    "BlackList",
    "FavoriteSubBlack",
    "LiteBlackList",
    "https://cdn.jsdelivr.net/gh/EtoNeYaProject/EtoNeYaProject.github.io@refs/heads/main/youtube",
]

WHITE_SOURCES = ["WhiteList", "LiteWhiteList"]

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def fetch_content(url: str) -> str:
    url = url.strip()

    if url.startswith("http"):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "*/*",
                },
            )
            with urllib.request.urlopen(req, timeout=25) as r:
                raw = r.read()
                return raw.decode("utf-8", errors="ignore")
        except Exception as e:
            print(f"[FETCH FAIL] {url} -> {e}")
            return ""

    path = Path(url)
    if path.exists():
        return path.read_text(encoding="utf-8", errors="ignore")

    return ""


def score(line: str) -> int:
    l = line.lower()
    if "trojan://" in l:
        return 100
    if "hysteria2://" in l or "hy2://" in l:
        return 80
    return 0


def process(files):
    links = set()

    for src in files:
        content = fetch_content(src)
        if not content:
            continue

        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue

            l = line.lower()

            # 🔥 ТОЛЬКО ТВОИ ПРОТОКОЛЫ
            if l.startswith("trojan://") or l.startswith("hysteria2://") or l.startswith("hy2://"):
                links.add(line.split()[0])

    return sorted(links, key=score, reverse=True)


def save(name, links):
    txt = OUTPUT_DIR / f"{name}.txt"
    b64 = OUTPUT_DIR / f"{name}.b64"

    data = "\n".join(links) + "\n"

    txt.write_text(data, encoding="utf-8")
    b64.write_text(base64.b64encode(data.encode()).decode(), encoding="utf-8")

    print(f"{name}: {len(links)} links")


def main():
    black = process(BLACK_SOURCES)
    white = process(WHITE_SOURCES)

    save("BlackHy2Trojan", black)
    save("WhiteHy2Trojan", white)

    print("DONE")


if __name__ == "__main__":
    main()
