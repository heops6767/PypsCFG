import base64
import urllib.request
from pathlib import Path

# Настройки входа
BLACK_SOURCES = ["BlackList", "FavoriteSubBlack", "LiteBlackList"]
WHITE_SOURCES = ["WhiteList", "LiteWhiteList"]

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def get_score(line: str) -> int:
    """Приоритет: Reality > Vision > TLS"""
    low = line.lower()
    if "security=reality" in low: return 50
    if "flow=xtls-rprx-vision" in low: return 30
    if "security=tls" in low or "sni=" in low: return 20
    return 0

def fetch_content(source: str) -> str:
    """Загрузка из URL или чтение локального файла"""
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
    """Сбор, декодирование и фильтрация ссылок"""
    unique_links = set()
    for filename in files_list:
        content = fetch_content(filename)
        if not content: continue
        
        # Декодирование, если это подписка в Base64
        if "://" not in content[:20]:
            try: 
                content = base64.b64decode(content + "==").decode("utf-8", errors="ignore")
            except: pass
            
        for sub_line in content.splitlines():
            sub_line = sub_line.strip()
            # Строгий фильтр протоколов
            if sub_line.startswith(("vless://", "trojan://", "hysteria2://", "hy2://")):
                unique_links.add(sub_line.split()[0])
    
    # Сортировка по весу (Reality наверх)
    return sorted(list(unique_links), key=get_score, reverse=True)

def save_files(name_prefix, links):
    """Сохранение .txt и .b64"""
    if not links: return
    txt_data = "\n".join(links).strip() + "\n"
    
    (OUTPUT_DIR / f"{name_prefix}FiltredHy2VlessTrojan.txt").write_text(txt_data, encoding="utf-8")
    
    b64_data = base64.b64encode(txt_data.encode("utf-8")).decode("ascii")
    (OUTPUT_DIR / f"{name_prefix}FiltredHy2VlessTrojan.b64").write_text(b64_data, encoding="utf-8")

def main():
    # Обработка Чёрного списка
    black_links = process_list(BLACK_SOURCES)
    save_files("Black", black_links)
    
    # Обработка Белого списка
    white_links = process_list(WHITE_SOURCES)
    save_files("White", white_links)

    print(f"Готово! Black: {len(black_links)}, White: {len(white_links)}")

if __name__ == "__main__":
    main()
