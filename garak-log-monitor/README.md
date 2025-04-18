# 🔍 Garak Live Log Monitor with Highlights

This Bash script lets you **monitor Garak logs in real-time**, while automatically **highlighting important events** and saving a colorized log to file for later analysis or sharing.

---

## ✅ Features

- 🟢 Highlights successful HTTP 200 responses
- 🔴 Flags timeouts and request failures
- 🟡 Spots retry/backoff events
- 🟣 Highlights large responses (>900 bytes)
- 🗃️ Saves a timestamped copy of the live log session with all highlights

---

## 🛠️ Requirements

- Linux/macOS system with a Bash shell (e.g., Kali, Ubuntu, WSL, etc.)
- [Garak](https://github.com/leondz/garak) installed and generating logs
- `awk`, `sed`, `date`, and `tput` (default in most Linux distros)

---

## 🚀 Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/azeemnow/RandomScripts/tree/master/garak-log-monitor.git
   cd garak-log-monitor
   ```

2. Make the script executable:
   ```bash
   chmod +x garak_log_monitor_highlight.sh
   ```

3. Make sure your Garak logs are being written to:
   ```
   /home/kali/.local/share/garak/garak.log
   ```

   > If you use a different path, edit the script and update the `LOG_FILE` variable.

---

## ▶️ How to Use

To start monitoring your Garak logs in real time:

```bash
./garak_log_monitor_highlight.sh
```

- You’ll see live colorized output in your terminal.
- A log of the session will also be saved to:
  ```
  ~/Documents/GARAK/garak-log/garak-live-log-YYYYMMDD-HHMMSS.log
  ```

---

## 📁 Example Output

Here's a sample of what the live output looks like:

```
[INFO] Starting live Garak log monitor...
Highlighting:
  ✔ HTTP 200 OK
  ✖ Timeouts / Failures
  ↻ Backoffs
  ⇪ Large Responses (>900 bytes)

[+] 200 OK response from llama3:8b...
[!] ReadTimeout from gpt-4-0314
[↻] Backing off _call_model for 10s
[⇪] Large Content-Length: 1217 bytes
```

All of this will be saved in a file like:

```
garak-live-log-20250415-135622.log
```

---

## 💡 Benefits

- 🔎 Quickly spot errors, retries, and anomalies during scans
- 🛠️ Ideal for **live debugging**, **pentesting sessions**, or **eval comparisons**
- 📝 Save and share color-coded logs for collaboration or reporting
- 🧠 Great tool for CTI/Red Teamers and LLM security researchers

---

## 🧰 Customization

Want to:
- Add your own match patterns?
- Change color schemes?
- Filter specific models or plugin names?

👉 Open the script and tweak the `awk` logic to match your own needs.

---


Disclosure 🕵️‍♂️💻  
— This project includes contributions from AI (e.g., ChatGPT)
