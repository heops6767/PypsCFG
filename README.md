# PypsCFG — Агрегатор подписок / Subscription Aggregator

<p align="center">
  <a href="#-pypscfg--агрегатор-подписок">Русский</a> |
  <a href="#-pypscfg--subscription-aggregator">English</a>
</p>

---

## 🇷🇺 PypsCFG — Агрегатор подписок

### ℹ️ О проекте

**PypsCFG** — это репозиторий для сборки и обновления подписок из разных источников в одном месте.  
Он автоматически:

- 📥 забирает списки из указанных источников
- 🧹 очищает их от лишнего мусора
- 🚫 удаляет `ss://` и `ssr://`
- ♻️ убирает дубли
- 📦 собирает итоговые TXT и Base64-файлы
- 🔄 регулярно обновляет результат через GitHub Actions

Подходит, если нужна одна или несколько удобных ссылок на уже обработанные списки.

---

### ⚙️ Как это работает

В корне репозитория используются входные файлы:

- `BlackList`
- `WhiteList`
- `FavoriteSubBlack`
- `LiteBlackList`
- `LiteWhiteList`

В них можно указывать:

- ссылки на подписки
- готовые конфиги построчно

Если источник возвращает **Base64**, он автоматически декодируется.  
Если возвращается обычный текст — он обрабатывается как есть.

---

### 🧩 Что именно фильтруется

PypsCFG сохраняет и обрабатывает только нужные типы конфигов:

- `vless://`
- `vmess://`
- `trojan://`
- `hysteria2://`
- `hy2://`
- `tuic://`

Автоматически удаляются:

- `ss://`
- `ssr://`
- пустые строки
- часть дублей и повторов

---

### 📊 Типы списков

| Список | Назначение | Обновление | Формат |
|---|---|---:|---|
| `BlackList` | основной чёрный список | часто | TXT + Base64 |
| `WhiteList` | основной белый список | часто | TXT + Base64 |
| `FavoriteSubBlack` | отдельная подборка | часто | TXT + Base64 |
| `LiteBlackList` | облегчённый чёрный список | часто | TXT + Base64 |
| `LiteWhiteList` | облегчённый белый список | часто | TXT + Base64 |
| `*Checked` | версии после endpoint-проверки | реже | TXT + Base64 |
| `merged_all` | общий объединённый список | часто | TXT + Base64 |
| `merged_all_Checked` | общий checked-список | реже | TXT + Base64 |

---

### 🔄 Автообновление

В репозитории используются два режима обновления:

- ⚡ **быстрое обновление** — обычная сборка без тяжёлой проверки
- ✅ **checked-обновление** — отдельная сборка с проверкой endpoint'ов

Обычная сборка запускается чаще, checked-сборка — реже.

---

### 🔗 Ссылки

#### GitHub Raw

<details>
<summary>Показать ссылки GitHub Raw</summary>

**Обычные списки**

- BlackList.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/BlackList.txt`
- BlackList.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/BlackList.b64`

- WhiteList.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/WhiteList.txt`
- WhiteList.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/WhiteList.b64`

- FavoriteSubBlack.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/FavoriteSubBlack.txt`
- FavoriteSubBlack.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/FavoriteSubBlack.b64`

- LiteBlackList.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteBlackList.txt`
- LiteBlackList.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteBlackList.b64`

- LiteWhiteList.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteWhiteList.txt`
- LiteWhiteList.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteWhiteList.b64`

- merged_all.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/merged_all.txt`
- merged_all.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/merged_all.b64`

**Checked-списки**

- BlackListChecked.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/BlackListChecked.txt`
- BlackListChecked.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/BlackListChecked.b64`

- WhiteListChecked.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/WhiteListChecked.txt`
- WhiteListChecked.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/WhiteListChecked.b64`

- FavoriteSubBlackChecked.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/FavoriteSubBlackChecked.txt`
- FavoriteSubBlackChecked.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/FavoriteSubBlackChecked.b64`

- LiteBlackListChecked.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteBlackListChecked.txt`
- LiteBlackListChecked.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteBlackListChecked.b64`

- LiteWhiteListChecked.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteWhiteListChecked.txt`
- LiteWhiteListChecked.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteWhiteListChecked.b64`

- merged_all_Checked.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/merged_all_Checked.txt`
- merged_all_Checked.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/merged_all_Checked.b64`

</details>

#### jsDelivr

<details>
<summary>Показать ссылки jsDelivr</summary>

**Обычные списки**

- BlackList.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/BlackList.txt`
- BlackList.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/BlackList.b64`

- WhiteList.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/WhiteList.txt`
- WhiteList.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/WhiteList.b64`

- FavoriteSubBlack.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/FavoriteSubBlack.txt`
- FavoriteSubBlack.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/FavoriteSubBlack.b64`

- LiteBlackList.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteBlackList.txt`
- LiteBlackList.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteBlackList.b64`

- LiteWhiteList.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteWhiteList.txt`
- LiteWhiteList.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteWhiteList.b64`

- merged_all.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/merged_all.txt`
- merged_all.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/merged_all.b64`

**Checked-списки**

- BlackListChecked.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/BlackListChecked.txt`
- BlackListChecked.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/BlackListChecked.b64`

- WhiteListChecked.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/WhiteListChecked.txt`
- WhiteListChecked.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/WhiteListChecked.b64`

- FavoriteSubBlackChecked.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/FavoriteSubBlackChecked.txt`
- FavoriteSubBlackChecked.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/FavoriteSubBlackChecked.b64`

- LiteBlackListChecked.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteBlackListChecked.txt`
- LiteBlackListChecked.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteBlackListChecked.b64`

- LiteWhiteListChecked.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteWhiteListChecked.txt`
- LiteWhiteListChecked.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteWhiteListChecked.b64`

- merged_all_Checked.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/merged_all_Checked.txt`
- merged_all_Checked.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/merged_all_Checked.b64`

</details>

---

### 🛠️ Как добавить свои источники

Если вы хотите использовать этот репозиторий у себя:

1. Сделайте **fork**
2. Добавьте свои ссылки или конфиги в нужные входные файлы
3. При необходимости настройте GitHub Actions под себя
4. Используйте готовые ссылки из `output/`

---

## 🇬🇧 PypsCFG — Subscription Aggregator

### ℹ️ About the Project

**PypsCFG** is a repository for collecting and updating subscriptions from multiple sources in one place.  
It automatically:

- 📥 fetches subscription sources
- 🧹 cleans unnecessary junk
- 🚫 removes `ss://` and `ssr://`
- ♻️ removes duplicates
- 📦 builds final TXT and Base64 outputs
- 🔄 updates everything via GitHub Actions

It is useful when you want one or several ready-to-use processed subscription links.

---

### ⚙️ How It Works

The repository uses these input files in the root directory:

- `BlackList`
- `WhiteList`
- `FavoriteSubBlack`
- `LiteBlackList`
- `LiteWhiteList`

Each file may contain:

- subscription URLs
- raw configs line by line

If a source returns **Base64**, it is decoded automatically.  
If it returns plain text, it is processed as-is.

---

### 🧩 What Gets Filtered

PypsCFG keeps and processes only these config types:

- `vless://`
- `vmess://`
- `trojan://`
- `hysteria2://`
- `hy2://`
- `tuic://`

The following are removed automatically:

- `ss://`
- `ssr://`
- empty lines
- some duplicates and repeated entries

---

### 📊 List Types

| List | Purpose | Update rate | Format |
|---|---|---:|---|
| `BlackList` | main blacklist | frequent | TXT + Base64 |
| `WhiteList` | main whitelist | frequent | TXT + Base64 |
| `FavoriteSubBlack` | separate selected list | frequent | TXT + Base64 |
| `LiteBlackList` | lighter blacklist | frequent | TXT + Base64 |
| `LiteWhiteList` | lighter whitelist | frequent | TXT + Base64 |
| `*Checked` | lists after endpoint checking | less frequent | TXT + Base64 |
| `merged_all` | combined merged list | frequent | TXT + Base64 |
| `merged_all_Checked` | combined checked list | less frequent | TXT + Base64 |

---

### 🔄 Auto Update

The repository uses two update modes:

- ⚡ **fast update** — regular build without heavy checking
- ✅ **checked update** — separate build with endpoint validation

The regular build runs more often, while the checked build runs less frequently.

---

### 🔗 Links

#### GitHub Raw

<details>
<summary>Show GitHub Raw links</summary>

**Regular lists**

- BlackList.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/BlackList.txt`
- BlackList.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/BlackList.b64`

- WhiteList.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/WhiteList.txt`
- WhiteList.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/WhiteList.b64`

- FavoriteSubBlack.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/FavoriteSubBlack.txt`
- FavoriteSubBlack.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/FavoriteSubBlack.b64`

- LiteBlackList.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteBlackList.txt`
- LiteBlackList.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteBlackList.b64`

- LiteWhiteList.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteWhiteList.txt`
- LiteWhiteList.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteWhiteList.b64`

- merged_all.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/merged_all.txt`
- merged_all.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/merged_all.b64`

**Checked lists**

- BlackListChecked.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/BlackListChecked.txt`
- BlackListChecked.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/BlackListChecked.b64`

- WhiteListChecked.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/WhiteListChecked.txt`
- WhiteListChecked.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/WhiteListChecked.b64`

- FavoriteSubBlackChecked.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/FavoriteSubBlackChecked.txt`
- FavoriteSubBlackChecked.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/FavoriteSubBlackChecked.b64`

- LiteBlackListChecked.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteBlackListChecked.txt`
- LiteBlackListChecked.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteBlackListChecked.b64`

- LiteWhiteListChecked.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteWhiteListChecked.txt`
- LiteWhiteListChecked.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/LiteWhiteListChecked.b64`

- merged_all_Checked.txt  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/merged_all_Checked.txt`
- merged_all_Checked.b64  
  `https://raw.githubusercontent.com/heops6767/PypsCFG/main/output/merged_all_Checked.b64`

</details>

#### jsDelivr

<details>
<summary>Show jsDelivr links</summary>

**Regular lists**

- BlackList.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/BlackList.txt`
- BlackList.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/BlackList.b64`

- WhiteList.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/WhiteList.txt`
- WhiteList.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/WhiteList.b64`

- FavoriteSubBlack.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/FavoriteSubBlack.txt`
- FavoriteSubBlack.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/FavoriteSubBlack.b64`

- LiteBlackList.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteBlackList.txt`
- LiteBlackList.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteBlackList.b64`

- LiteWhiteList.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteWhiteList.txt`
- LiteWhiteList.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteWhiteList.b64`

- merged_all.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/merged_all.txt`
- merged_all.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/merged_all.b64`

**Checked lists**

- BlackListChecked.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/BlackListChecked.txt`
- BlackListChecked.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/BlackListChecked.b64`

- WhiteListChecked.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/WhiteListChecked.txt`
- WhiteListChecked.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/WhiteListChecked.b64`

- FavoriteSubBlackChecked.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/FavoriteSubBlackChecked.txt`
- FavoriteSubBlackChecked.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/FavoriteSubBlackChecked.b64`

- LiteBlackListChecked.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteBlackListChecked.txt`
- LiteBlackListChecked.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteBlackListChecked.b64`

- LiteWhiteListChecked.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteWhiteListChecked.txt`
- LiteWhiteListChecked.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/LiteWhiteListChecked.b64`

- merged_all_Checked.txt  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/merged_all_Checked.txt`
- merged_all_Checked.b64  
  `https://cdn.jsdelivr.net/gh/heops6767/PypsCFG@main/output/merged_all_Checked.b64`

</details>

---

### 🛠️ How to Use Your Own Sources

If you want to use this repository for your own setup:

1. Fork the repository
2. Put your links or configs into the input files
3. Adjust GitHub Actions if needed
4. Use the generated links from `output/`

---
