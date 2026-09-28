# Automatic Birthday Wisher

A lightweight, zero-maintenance Python automation tool scheduled via GitHub Actions to monitor dates and send personalized celebratory greetings via Gmail SMTP.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Scheduled_Cron-2088FF?style=flat-square&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Gmail SMTP](https://img.shields.io/badge/Gmail-SMTP_Relay-EA4335?style=flat-square&logo=gmail&logoColor=white)](https://mail.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

---

## Overview

Remembering and timely acknowledging birthdays across large personal and professional circles can be challenging. **Automatic Birthday Wisher** provides an automated, serverless solution that eliminates reliance on proprietary third-party reminder applications.

The script runs on a daily GitHub Actions cron workflow. Every day at midnight UTC, it parses a secure CSV record of friends and colleagues, computes current calendar matches (day and month), and automatically formats and dispatches customized birthday wishes through Gmail's SMTP service with secure App Passwords.

---

## Features

- **Serverless & Zero-Cost**: Runs entirely on GitHub Actions' free runner tier without needing a dedicated 24/7 VPS.
- **Daily Automated Execution**: Scheduled via GitHub Actions cron syntax (`0 0 * * *`) to trigger at the start of each day.
- **CSV Data Ingestion**: Clean, decoupled record storage via CSV (`Name`, `Email`, `BirthDay`, `BirthMonth`).
- **Dynamic Email Template Engine**: Injects recipient names into personalized, warm HTML/text email templates.
- **Secure Secret Handling**: Zero hardcoded credentials; uses GitHub repository secrets for email and SMTP app password security.
- **Extensible Architecture**: Modular design ready for multi-channel notification dispatchers (e.g., WhatsApp, Telegram).

---

## Tech Stack

- **Core Engine**: Python 3.10+
- **Scheduler & CI/CD**: GitHub Actions
- **Protocol**: Standard Library `smtplib` & `email.mime`
- **Data Parser**: Python built-in `csv` & `datetime` modules

---

## Architecture

```text
┌─────────────────────────┐
│  GitHub Actions Cron    │  Triggers daily at 00:00 UTC
└─────────────────────────┘
             │
             ▼
┌─────────────────────────┐
│     Python Script       │  Reads friends_birthdays.csv
│   (birthday_wisher.py)  │  Compares current DD/MM with record
└─────────────────────────┘
             │
             ▼ If Match Found
┌─────────────────────────┐
│   Gmail SMTP Gateway    │  Dispatches personalized email
│  (smtp.gmail.com:587)   │  using GitHub Actions Secrets
└─────────────────────────┘
             │
             ▼
┌─────────────────────────┐
│    Recipient Inbox      │
└─────────────────────────┘
```

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/hritikkumarpd/Automatic-Birthday-Wisher.git
cd Automatic-Birthday-Wisher
```

### 2. Configure Recipient Data
Edit the CSV file with your friends' details:
```csv
Name,Email,BirthDay,BirthMonth
John Doe,john@example.com,15,10
Jane Smith,jane@example.com,22,4
```

### 3. Setup GitHub Secrets
Navigate to your repository on GitHub: **Settings > Secrets and variables > Actions > New repository secret**.

Add the following secrets:
- `SENDER_EMAIL`: Your Gmail address (e.g. `yourname@gmail.com`).
- `SENDER_PASSWORD`: Your 16-character [Google App Password](https://myaccount.google.com/apppasswords).

### 4. Enable GitHub Actions
Ensure GitHub Actions is enabled under the **Actions** tab of your repository. The workflow will run automatically every day at 00:00 UTC, and can also be tested manually using the **Run workflow** button.

---

## Environment Variables

When running locally, set the following environment variables:

```env
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_16_character_app_password
RECIPIENT_CSV_PATH=birthday_wisher/birthdays.csv
```

---

## License

This project is licensed under the [MIT License](LICENSE) — see the LICENSE file for details.
