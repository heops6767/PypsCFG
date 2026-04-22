import os
import re
import base64

# Пути к папкам
RAW_DIR = 'raw'        # Сюда кладем сырые конфиги/ссылки
RESULT_DIR = 'configs' # Сюда будут сохраняться отсортированные файлы

# Создаем папки, если их нет
os.makedirs(RESULT_DIR, exist_ok=True)

def sort_configs():
    # Словари для хранения протоколов
    sorted_data = {
        "vless": [],
        "trojan": [],
        "hysteria2": []
    }

    # Читаем все файлы из raw
    for filename in os.listdir(RAW_DIR):
        with open(os.path.join(RAW_DIR, filename), 'r', encoding='utf-8') as f:
            content = f.read()
            # Поиск ссылок по протоколам
            vless = re.findall(r'vless://[^\s]+', content)
            trojan = re.findall(r'trojan://[^\s]+', content)
            hy2 = re.findall(r'hy2://[^\s]+|hysteria2://[^\s]+', content)

            sorted_data["vless"].extend(vless)
            sorted_data["trojan"].extend(trojan)
            sorted_data["hysteria2"].extend(hy2)

    for proto, links in sorted_data.items():
        # Удаляем дубликаты
        unique_links = list(set(links))
        
        # Фильтр "Максимальной маскировки": отдаем приоритет Reality и TLS
        # Сортируем так, чтобы ссылки с Reality были вверху
        unique_links.sort(key=lambda x: ("reality" in x.lower() or "security=tls" in x.lower()), reverse=True)

        if unique_links:
            output_file = os.path.join(RESULT_DIR, f"{proto}.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(unique_links))
            
            # Также создаем Base64 версию для подписок
            with open(os.path.join(RESULT_DIR, f"{proto}_base64.txt"), 'w', encoding='utf-8') as f:
                b64_content = base64.b64encode('\n'.join(unique_links).encode()).decode()
                f.write(b64_content)

    print("Сортировка завершена успешно.")

if __name__ == "__main__":
    sort_configs()
