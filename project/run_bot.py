import os
import runpy
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

try:
    import winreg
except ImportError:
    winreg = None   

if winreg:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment")
        token = winreg.QueryValueEx(key, "TELEGRAM_TOKEN")[0]
        os.environ["TELEGRAM_TOKEN"] = token
    except (FileNotFoundError, Exception):
        token = os.environ.get("TELEGRAM_TOKEN")
else:
    token = os.environ.get("TELEGRAM_TOKEN")

if not token:
    raise RuntimeError("TELEGRAM_TOKEN muhit o'zgaruvchilaridan yoki registrdan topilmadi!")

# ---- SOXTA PORT OCHISH (RENDER ALDASH UCHUN) ----
def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"Soxta server {port}-portda ishga tushdi...")
    server.serve_forever()

# Serverni alohida oqimda (thread) yuritish
threading.Thread(target=run_dummy_server, daemon=True).start()
# --------------------------------------------------

# Botni ishga tushirish qismi
runpy.run_path(os.path.join(os.path.dirname(__file__), "bot.py"), run_name="__main__")