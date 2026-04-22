import base64, json, re, urllib.parse, urllib.request
from pathlib import Path

# Конфигурация
INPUT_FILES = ["BlackList", "WhiteList", "FavoriteSubBlack", "LiteBlackList", "LiteWhiteList"]
OUTPUT_DIR = Path("output")
REPORT_DIR = Path("reports")
OUTPUT_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

ALLOWED_PROTOCOLS = ("vless://", "trojan://", "hysteria2://", "hy2://")

def get_masking_score(line: str) -> int:
    score = 0
    low = line.lower()
    # Приоритеты для "самых мощных"
    if "reality" in low: score += 50
    if "security=tls" in low: score += 20
    if "flow=xtls-rprx-vision" in low: score += 30
    if "sni=" in low: score += 10
    if "fp=chrome" in low: score += 5
    return score

def is_super_config(line: str) -> bool:
    # Фильтр: оставляем только то, что имеет хоть какую-то защиту (Reality или TLS/SNI)
    return get_masking_score(line) >= 20

def fetch_text(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 PypsCFG-Fast"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except: return ""

def main():
    all_links = []
    seen = set()

    # Сбор данных
    for raw_file in INPUT_FILES:
        path = Path(raw_file)
        if not path.exists(): continue
        
        lines = path.read_text(encoding="utf-8").splitlines()
        for link in lines:
            link = link.strip()
            if not link or link.startswith("#"): continue
            
            # Если это ссылка на подписку - скачиваем
            content = fetch_text(link) if link.startswith("http") else link
            
            # Декодируем base64 если нужно
            if content and not "://" in content:
                try: content = base64.b64decode(content + "==").decode("utf-8", errors="ignore")
                except: pass

            for line in content.splitlines():
                line = line.strip()
                if line.startswith(ALLOWED_PROTOCOLS):
                    # Очистка от мусора в названии
                    clean_line = line.split(" | ")[0] if " | " in line else line
                    if clean_line not in seen:
                        seen.add(clean_line)
                        all_links.append(clean_line)

    # --- СУПЕР ФИЛЬТРАЦИЯ ---
    # 1. Только Vless, Trojan, Hy2
    # 2. Только с высоким скором маскировки
    filtered = [l for l in all_links if is_super_config(l)]
    
    # Сортировка: самые мощные (Reality) в самом верху
    filtered.sort(key=get_masking_score, reverse=True)

    # Сохранение главного файла
    output_file = OUTPUT_DIR / "FiltredHy2VlessTrojan.txt"
    output_file.write_text("\n".join(filtered) + "\n", encoding="utf-8")
    
    # Дубликат в base64 для некоторых клиентов
    b64_content = base64.b64encode("\n".join(filtered).encode("utf-8")).decode("ascii")
    (OUTPUT_DIR / "FiltredHy2VlessTrojan.b64").write_text(b64_content)

    print(f"Done! Saved {len(filtered)} super-configs to {output_file}")

if __name__ == "__main__":
    main()
