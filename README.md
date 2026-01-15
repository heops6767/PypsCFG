# PypsCFG - Агрегатор подписок

<p align="center">
  <a href="#pypscfg---subscription-aggregator">English</a> |
  <a href="#pypscfg---агрегатор-подписок">Русский</a>
</p>

---

## 🇷🇺 PypsCFG - Агрегатор подписок

### ℹ️ О проекте

**PypsCFG** — это репозиторий, который служит агрегатором подписок из различных источников. Основная цель — объединить несколько списков подписок в один, который будет автоматически обновляться. Это позволяет использовать единую ссылку на агрегированный список в ваших приложениях.

### 🚀 Как это работает

Этот репозиторий использует GitHub Actions для автоматического сбора и объединения подписок из указанных источников. Процесс настроен на запуск по расписанию (например, каждые 24 часа), что гарантирует актуальность данных.

### ✨ Как добавить свои подписки

Если вы хотите, чтобы ваши подписки были добавлены в общий список, выполните следующие шаги:

1.  **Сделайте форк (Fork)** этого репозитория.
2.  В вашем форке найдите и откройте файл `subscriptions.txt` (или как вы его назовете).
3.  **Добавьте ссылки** на ваши источники подписок. Каждая ссылка должна быть на новой строке.
4.  **Создайте Pull Request** в этот репозиторий.
5.  После проверки и слияния вашего Pull Request, ваши подписки будут автоматически включены в общий агрегированный список.

### 🔄 Автообновление

*   **Для пользователей:** Если вы используете ссылку на финальный файл из этого репозитория, вы будете автоматически получать все обновления, как только они будут добавлены.
*   **Для контрибьюторов:** После того как ваш Pull Request будет принят, вам не нужно ничего делать. Система автоматически будет обновлять данные из ваших источников.

---

## 🇬🇧 PypsCFG - Subscription Aggregator

### ℹ️ About the Project

**PypsCFG** is a repository that serves as a subscription aggregator from various sources. The main goal is to combine multiple subscription lists into a single one that updates automatically. This allows you to use a single link to the aggregated list in your applications.

### 🚀 How It Works

This repository uses GitHub Actions to automatically collect and merge subscriptions from the specified sources. The process is scheduled to run at regular intervals (e.g., every 24 hours), which ensures that the data is always up-to-date.

### ✨ How to Add Your Subscriptions

If you want your subscriptions to be added to the main list, please follow these steps:

1.  **Fork** this repository.
2.  In your forked repository, find and open the `subscriptions.txt` file (or whatever you name it).
3.  **Add the links** to your subscription sources. Each link should be on a new line.
4.  **Create a Pull Request** to this repository.
5.  After your Pull Request is reviewed and merged, your subscriptions will be automatically included in the main aggregated list.

### 🔄 Auto-update

*   **For Users:** If you are using the link to the final file from this repository, you will automatically receive all updates as soon as they are added.
*   **For Contributors:** Once your Pull Request is merged, you don't need to do anything else. The system will automatically update the data from your sources.

