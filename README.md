README.md

# Zefoy Multi Tool - TikTok Views & Hearts Automation

This is a GUI-based automation tool for increasing **hearts** and **views** on TikTok videos using [Zefoy.com](https://zefoy.com). It leverages Python, Selenium, and Tkinter to interact with Zefoy's website, solve CAPTCHA manually, and automate video promotion requests.

> ⚠️ **Disclaimer**: This project is for educational purposes only. Using this tool may violate TikTok's terms of service or Zefoy's website policies. The developer is not responsible for any misuse.

---

## 🚀 Features

- [x] Automate **hearts ❤️** or **views 👁️** boosting.
- [x] Graphical interface using `Tkinter`.
- [x] CAPTCHA capture and manual input handling.
- [x] Built-in browser automation with Selenium.
- [x] Pause, Resume, and Stop control buttons.
- [x] Real-time logs, progress bar, and link tracking.
- [x] Support for bulk TikTok video URLs.
- [x] Light/Dark mode toggle.
- [x] Countdown synchronization and auto-submit support.

---

## 🖼 Interface Preview

> GUI elements include:
- CAPTCHA preview box
- Link input area
- Drop-down for selecting between "Hearts" or "Views"
- Control buttons (Start Browser, Submit CAPTCHA, Load Links, etc.)
- Log output with scroll
- Real-time stats and progress bar

---

## 🛠 Installation

### Requirements

- Python 3.7+
- Google Chrome
- pip (Python package installer)

### Install Dependencies

```bash
pip install -r requirements.txt

Or manually install the required modules:

pip install selenium webdriver-manager pillow


---

🧠 How It Works

1. Launches a Selenium Chrome browser and opens zefoy.com.


2. Automatically removes ads and popups.


3. Captures the CAPTCHA image for manual solving.


4. After CAPTCHA is solved, you can start sending hearts or views.


5. You can provide a list of TikTok URLs (one per line).


6. The tool waits for the Zefoy cooldown timer and resends automatically when available.




---

🧾 Usage Instructions

Step-by-step

1. Run the script:



python zefoy\ both.py

2. Click "🌐 Start Browser" – This opens a new Chrome window and navigates to Zefoy.com.


3. Solve Cloudflare manually if prompted.


4. Click "🖼️ Fetch CAPTCHA" – It captures and displays the CAPTCHA image.


5. Enter the CAPTCHA into the text box and click "📤 Submit CAPTCHA".


6. Paste your TikTok video links (one per line) by clicking "📂 Load Links" or typing directly.


7. Select Mode – Choose either ❤️ Hearts or 👁️ Views.


8. Click "▶ Start" – The automation will begin sending views or likes.


9. Use Pause, Resume, and Stop buttons anytime.




---

📁 Example Input File

https://www.tiktok.com/@user/video/1234567890
https://www.tiktok.com/@user/video/9876543210

Save this as a .txt file and load it using "📂 Load Links".


---

📄 requirements.txt

selenium
webdriver-manager
pillow


---

💡 Tips

Ensure Chrome is installed and up to date.

Always wait 15 seconds after launching the browser before solving CAPTCHA.

CAPTCHA must be entered correctly to continue automation.

You can resize or zoom the GUI for convenience.

Logs can be saved to zefoy_log.txt on exit.



---

📌 Notes

This tool does not bypass CAPTCHA or Cloudflare. CAPTCHA must be solved manually.

Zefoy has cooldowns between submissions, which this tool respects and waits through.

You may encounter rate-limits or temporary blocks if abused.



---

⚠️ Disclaimer

This tool interacts with third-party websites (Zefoy.com). Use it responsibly and at your own risk. This software is provided "as is", without warranty of any kind.


---

📬 Contact

Have suggestions or found bugs? Open an issue or submit a pull request.


---

📜 License

This project is licensed under the MIT License. See LICENSE for more details.

---

### 📦 `requirements.txt`

```txt
selenium
webdriver-manager
pillow


---

📄 example_links.txt

https://www.tiktok.com/@user/video/1234567890
https://www.tiktok.com/@user/video/9876543210
