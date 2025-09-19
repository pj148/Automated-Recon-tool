# Automated-Recon-tool
A Python-based tool that automates subdomain discovery, port scanning, and vulnerability scanning for bug bounty recon.
🚀 Automated Recon Tool
📌 Overview

This project is a Python-based automation tool designed for bug bounty reconnaissance.
It integrates multiple security tools to:

Discover subdomains

Check live hosts

Scan open ports

Extract JavaScript secrets

Run vulnerability templates with Nuclei

Generate PDF/HTML reports

⚙️ Features

🔎 Subdomain Discovery → using subfinder

🌐 Live Host Detection → using httpx

📡 Open Port Scanning → using naabu

🗝️ JS Secret Detection → using gau + xnLinkFinder

⚡ Vulnerability Scanning → using nuclei

📑 Report Generation → export findings in clean report

🛠️ Tech Stack / Tools

Python 3

Bash

Tools: subfinder, httpx, naabu, nuclei, gau, xnLinkFinder, shodan

📂 Project Structure
Automated-Recon-Tool/
├── code/             # Scripts
├── reports/          # Generated reports (PDF/HTML)
├── sample_targets/   # Example target lists
└── README.md         # Documentation

🚀 How to Use

Clone the repository:

git clone https://github.com/<your-username>/Automated-Recon-Tool.git
cd Automated-Recon-Tool


Run the tool:

python3 recon.py -d target.com


Reports will be saved inside reports/.

📸 Sample Output

(Add screenshot of your report or terminal output later)

📌 Future Improvements

Add multi-threading for faster scans

Create a simple dashboard for results

Integrate Slack/Discord notifications

✨ Author

👩‍💻 Pooja Sharma
Cybersecurity & Bug Bounty Enthusiast

