import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from PIL import Image, ImageTk
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import random
import os

# Global Variables
driver = None
stop_flag = False
pause_flag = False
counter = 0

# ---------------- CAPTCHA Functions ----------------
def periodically_remove_ads():
    log("[🧹] Ads removed after initial delay.")
    while driver and not stop_flag:
        try:
            remove_ads()
            log("[🧹] Ads cleaned (auto)")
            # Check for CAPTCHA presence once per cycle only if image not loaded
            if captcha_label.image == blank_img:
                try:
                    if driver.find_elements(By.XPATH, "//div[contains(@class, 'word-load')]//img"):
                        log("[👀] CAPTCHA element detected during ad cleanup. Attempting to capture...")
                        fetch_captcha_image()
                except Exception as e:
                    log(f"[❌] CAPTCHA auto-check during cleanup failed: {e}")
            time.sleep(5)
        except:
            break
def periodically_remove_popups():
    while driver and not stop_flag:
        try:
            driver.execute_script("""
                let popup = document.querySelector('.fc-monetization-dialog-container');
                if (popup) { popup.remove(); }
            """)
        except Exception:
            pass
        time.sleep(0.5)

def start_browser():
    global driver
    log("\n[🧭] Starting browser...")
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-popup-blocking")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    log("[🌐] Navigating to zefoy.com...")
    driver.get("https://zefoy.com")
    log("[⌛] Waiting 15 seconds after page load...")
    time.sleep(15)
    remove_ads()
    log("[🧹] Ads removed after initial wait.")

    # Trigger CAPTCHA fetch directly after initial wait
    try:
        log("[👀] Attempting to fetch CAPTCHA after initial wait...")
        fetch_captcha_image()
    except Exception as e:
        log(f"[❌] CAPTCHA auto-check failed: {e}")

    log("[🌐] Opened Zefoy. Please solve Cloudflare manually.")
    threading.Thread(target=periodically_remove_ads, daemon=True).start()
    threading.Thread(target=periodically_remove_popups, daemon=True).start()

def fetch_captcha_image():
    try:
        log("[🔍] Fetching CAPTCHA image...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'word-load')]//img"))
        )
        img_element = driver.find_element(By.XPATH, "//div[contains(@class, 'word-load')]//img")
        img_element.screenshot("captcha_element.png")
        img_data = Image.open("captcha_element.png").resize((200, 60))
        photo = ImageTk.PhotoImage(img_data)
        captcha_label.config(image=photo)
        captcha_label.image = photo
        log("[🖼️] CAPTCHA image loaded.")
    except Exception as e:
        log(f"[❌] CAPTCHA fetch failed: {e}")

def submit_captcha():
    try:
        value = captcha_entry.get().strip()
        if not value:
            messagebox.showwarning("Input Required", "Enter CAPTCHA text first.")
            return
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "captchatoken"))
        )
        driver.find_element(By.ID, "captchatoken").send_keys(value)
        driver.find_element(By.CLASS_NAME, "submit-captcha").click()
        log("[✅] CAPTCHA submitted.")
    except Exception as e:
        log(f"[❌] CAPTCHA submit failed: {e}")

def remove_ads():
    try:
        driver.execute_script("""
            document.querySelectorAll("iframe, .ads, .adsbygoogle, #ads, .popup, .modal, .alert")
                .forEach(el => el.remove());
        """)
        log("[🧹] Ads removed.")
    except Exception as e:
        log(f"[❌] Failed to remove ads: {e}")

# ---------------- Automation Logic ----------------
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException

def handle_alert():
    try:
        alert = driver.switch_to.alert
        log(f"[⚠️] Alert Detected: {alert.text}")
        alert.accept()
        log("[ℹ️] Alert accepted.")
        return True
    except NoAlertPresentException:
        return False
def parse_countdown(text):
    match = re.search(r'(\d+)\s*minute\(s\)?\s*(\d+)?\s*second', text)
    return int(match.group(1)) * 60 + int(match.group(2)) if match else 0

def automate(video_links, mode):
    global stop_flag, counter
    stop_flag = False
    counter = 0
    try:
        wait = WebDriverWait(driver, 60)
        remove_ads()

        mode_button = {
            'hearts': "t-hearts-button",
            'views': "t-views-button"
        }[mode]

        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, mode_button))).click()
        log(f"[🔘] Selected '{mode.capitalize()}' section.")
        time.sleep(2)

        total_links = len(video_links)
        start_time = time.time()
        for index, link in enumerate(video_links):
            if stop_flag: break
            log(f"[🔗] Link {index+1}/{total_links}: {link}")

            input_xpath = f"//div[contains(@class, 't-{mode}-menu')]//input[@type='search']"
            search_xpath = f"//div[contains(@class, 't-{mode}-menu')]//button[@type='submit' and contains(., 'Search')]"

            input_field = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
            input_field.clear()
            input_field.send_keys(link)
            log("[📥] Link entered.")

            wait.until(EC.element_to_be_clickable((By.XPATH, search_xpath))).click()
            handle_alert()
            log("[🔎] Search clicked.")
            time.sleep(random.uniform(2, 5))

            while not stop_flag:
                while pause_flag:
                        time.sleep(0.5)
                try:
                    countdown_xpath = "//span[contains(@class, 'br') or contains(@class, 'views-countdown')]"
                    countdown_text = driver.find_element(By.XPATH, countdown_xpath).text.strip()
                    log(f"[⏳] Countdown: {countdown_text}")

                    if "READY" in countdown_text:
                        wait.until(EC.element_to_be_clickable((By.XPATH, search_xpath))).click()
                        time.sleep(random.uniform(2, 5))
                        submit_xpath = "//form//button[@type='submit' and contains(@class, 'wbutton')]"
                        wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath))).click()
                        handle_alert()

                        counter += 25 if mode == 'hearts' else 500
                        count_label_var.set(f"{mode.capitalize()} Sent: {counter}")

                        percent_value = int(((index + 1) / total_links) * 100)
                        progress_bar['value'] = percent_value
                        progress_percent.config(
                            text=f"{percent_value}%",
                            fg="green" if percent_value == 100 else "orange"
                        )

                        log(f"[✅] {mode.capitalize()} submitted.")
                        break
                    else:
                        time.sleep(min(5, parse_countdown(countdown_text) or 5))
                except Exception as e:
                    log(f"[⚠️] Countdown check failed: {e}")
                    handle_alert()
                    time.sleep(3)
        log("[✅] Automation complete.")
    except Exception as e:
        log(f"[❌] Error: {e}")
        messagebox.showerror("Error", str(e))
    finally:
        stop_flag = False
        # Re-enable all buttons after automation ends
        for child in ctrl_frame.winfo_children() + action_frame.winfo_children():
            child.config(state="normal")

def clear_log():
    log_box.config(state='normal')
    log_box.delete('1.0', tk.END)
    log_box.config(state='disabled')

# ---------------- GUI + Threads ----------------
def log(msg):
    log_box.config(state='normal')
    log_box.insert(tk.END, msg + '\n')
    log_box.see(tk.END)
    log_box.config(state='disabled')

def start_thread(mode):
    links = [line.strip() for line in input_box.get("1.0", tk.END).splitlines() if line.strip()]
    if not links:
        messagebox.showwarning("Missing Input", "Please enter at least one video URL.")
        return

    # Disable all buttons except Pause/Resume
    for child in ctrl_frame.winfo_children() + action_frame.winfo_children():
        if child['text'] not in ["⏸ Pause", "▶ Resume", "⛔ Stop"]:
            child.config(state="disabled")

    threading.Thread(target=automate, args=(links, mode), daemon=True).start()

def pause():
    global pause_flag
    pause_flag = True
    log("[⏸] Automation paused.")

def resume():
    global pause_flag
    pause_flag = False
    log("[▶] Automation resumed.")

def stop():
    global stop_flag
    stop_flag = True
    progress_bar['value'] = 0
    progress_percent.config(text="0%", fg="blue")
    count_label_var.set("Ready")
    captcha_label.config(image=blank_img)
    captcha_label.image = blank_img

def load_file():
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if path:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        input_box.config(state="normal")
        input_box.delete("1.0", tk.END)
        input_box.insert(tk.END, content)
        input_box.config(state="disabled")

# ---------------- GUI Setup ----------------
def toggle_dark_mode():
    bg_color = '#2e2e2e' if root['bg'] != '#2e2e2e' else 'SystemButtonFace'
    fg_color = 'white' if bg_color == '#2e2e2e' else 'black'
    widgets = root.winfo_children()
    root.configure(bg=bg_color)
    for w in widgets:
        try:
            w.configure(bg=bg_color, fg=fg_color)
        except:
            pass

root = tk.Tk()
root.title("Zefoy Multi Tool - Hearts + Views")
root.state('zoomed')  # Maximized window
root.resizable(True, True)

# Apply modern styling
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Segoe UI", 10), padding=6, relief="flat")
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TCombobox", font=("Segoe UI", 10))
style.configure("TEntry", font=("Segoe UI", 10))
style.configure("TProgressbar", thickness=20)
style.map("TButton",
    foreground=[('pressed', 'white'), ('active', '#0044cc')],
    background=[('pressed', '#3366cc'), ('active', '#cce0ff')]
)

# Add hover effect for all standard buttons
hover_bg = "#e6f0ff"
def on_enter(e): e.widget.config(bg=hover_bg)
def on_leave(e): e.widget.config(bg="SystemButtonFace")

root.option_add("*Font", ("Segoe UI", 10))  # Maximized window
root.resizable(True, True)

# Theme & Control Buttons
menu_frame = tk.Frame(root)
menu_frame.pack(pady=5)
btn_dark_mode = tk.Button(menu_frame, text="🌓 Toggle Dark Mode", command=toggle_dark_mode)
btn_dark_mode.pack()
btn_dark_mode.bind("<Enter>", on_enter)
btn_dark_mode.bind("<Leave>", on_leave)

# Control Buttons
ctrl_frame = tk.Frame(root)
ctrl_frame.pack(pady=10)
tk.Button(ctrl_frame, text="🧹 Clear Log", command=lambda: clear_log(), width=18).pack(side=tk.LEFT, padx=5)
tk.Button(ctrl_frame, text="🌐 Start Browser", command=lambda: threading.Thread(target=start_browser).start(), width=18).pack(side=tk.LEFT, padx=5)
tk.Button(ctrl_frame, text="🖼️ Fetch CAPTCHA", command=lambda: threading.Thread(target=fetch_captcha_image).start(), width=18).pack(side=tk.LEFT, padx=5)
tk.Button(ctrl_frame, text="📤 Submit CAPTCHA", command=lambda: threading.Thread(target=submit_captcha).start(), width=18).pack(side=tk.LEFT, padx=5)
tk.Button(ctrl_frame, text="📂 Load Links", command=load_file, width=18).pack(side=tk.LEFT, padx=5)

# CAPTCHA Section
from PIL import Image
blank_img = ImageTk.PhotoImage(Image.new("RGB", (200, 60), "white"))
captcha_frame = tk.LabelFrame(root, text="CAPTCHA", padx=10, pady=10)
captcha_frame.pack(padx=10, pady=10, fill="x")
captcha_label = tk.Label(captcha_frame, image=blank_img, bg="white", relief="solid")
captcha_label.image = blank_img
captcha_label.pack(pady=5)
captcha_entry = tk.Entry(captcha_frame, width=40)
captcha_entry.pack()

# URL Input Section
input_frame = tk.LabelFrame(root, text="TikTok Video Links", padx=10, pady=10)
input_frame.pack(padx=10, pady=10, fill="both", expand=True)
tk.Label(input_frame, text="Enter TikTok Video URLs (one per line):", font=("Arial", 12)).pack(anchor="w")
input_box = tk.Text(input_frame, height=7, wrap="word", state="disabled")
input_box.pack(fill="both", expand=True)

# Mode Selection
mode_frame = tk.Frame(root)
mode_frame.pack(pady=5)
mode_var = tk.StringVar(value="❤️ Hearts")
tk.Label(mode_frame, text="Select Mode:", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
mode_menu = ttk.Combobox(mode_frame, textvariable=mode_var, values=["❤️ Hearts", "👁️ Views"], state="readonly", width=20)
mode_menu.pack(side=tk.LEFT)

# Action Buttons
action_frame = tk.Frame(root)
action_frame.pack(pady=10)
tk.Button(action_frame, text="▶ Start", bg="blue", fg="white", width=20, command=lambda: start_thread("hearts" if "Heart" in mode_var.get() else "views")).pack(side=tk.LEFT, padx=10)
tk.Button(action_frame, text="⏸ Pause", bg="orange", fg="white", width=15, command=pause).pack(side=tk.LEFT, padx=10)
tk.Button(action_frame, text="▶ Resume", bg="green", fg="white", width=15, command=resume).pack(side=tk.LEFT, padx=10)
tk.Button(action_frame, text="⛔ Stop", bg="gray", fg="white", width=15, command=stop).pack(side=tk.LEFT, padx=10)

# Log Output Section
log_frame = tk.LabelFrame(root, text="Log", padx=10, pady=10)
log_frame.pack(padx=10, pady=10, fill="both", expand=True)
log_box = scrolledtext.ScrolledText(log_frame, height=15, state='disabled', wrap="word")
log_box.pack(fill="both", expand=True)

# Count + Progress
count_label_var = tk.StringVar(value="Ready")
tk.Label(root, textvariable=count_label_var, font=("Arial", 12), fg="darkblue").pack(pady=5)
progress_frame = tk.Frame(root)
progress_frame.pack(pady=5)
progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', mode='determinate', length=600)
progress_bar.pack(side=tk.LEFT, padx=5, fill='x', expand=True)
progress_percent = tk.Label(progress_frame, text="0%", font=("Arial", 10, "bold"), fg="blue")
progress_percent.pack(side=tk.RIGHT, padx=5)
progress_bar.pack()

log("[📋] Log initialized...")
def save_log_to_file():
    try:
        with open("zefoy_log.txt", "w", encoding="utf-8") as f:
            f.write(log_box.get("1.0", tk.END).strip())
        print("[💾] Log saved to 'zefoy_log.txt'")
    except Exception as e:
        print(f"[❌] Failed to save log: {e}")

root.protocol("WM_DELETE_WINDOW", lambda: save_log_to_file() or root.destroy())
root.mainloop()
