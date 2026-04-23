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
    if "security=reality" in low: score += 50
    if "security=tls" in low or "sni=" in low: score += 20
    return score

def fetch_content(source: str) -> str:
    source = source.strip()
    if source.startswith("http"):
        try:
            req = urllib.request.Request(source, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.read().decode("utf-8", errors="ignore")
        except: return ""
    path = Path(source)
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""

def process_list(files_list):
    unique_links = set()
    for filename in files_list:
        content = fetch_content(filename)
        if not content: continue
        
        # Обработка Base64 подписок
        if "://" not in content[:30]:
            try:
                content = base64.b64decode(content + "==").decode("utf-8", errors="ignore")
            except: pass
            
        for line in content.splitlines():
            line = line.strip()
            # 🔥 СТРОГИЙ ФИЛЬТР: Только Hy2 и Trojan
            if line.startswith(("trojan://", "hysteria2://", "hy2://")):
                unique_links.add(line.split()[0])
    
    return sorted(list(unique_links), key=get_score, reverse=True)

def save_output(name_prefix, links):
    if not links: return
    content = "\n".join(links).strip() + "\n"
    
    # Файлы без слова Vless
    txt_name = OUTPUT_DIR / f"{name_prefix}Hy2Trojan.txt"
    b64_name = OUTPUT_DIR / f"{name_prefix}Hy2Trojan.b64"
    
    txt_name.write_text(content, encoding="utf-8")
    b64_val = base64.b64encode(content.encode("utf-8")).decode("ascii")
    b64_name.write_text(b64_val, encoding="utf-8")

def main():
    # Черный список
    black = process_list(BLACK_SOURCES)
    save_output("Black", black)
    
    # Белый список
    white = process_list(WHITE_SOURCES)
    save_output("White", white)

    print(f"Done! Hy2/Trojan found -> Black: {len(black)}, White: {len(white)}")

if __name__ == "__main__":
    main()
