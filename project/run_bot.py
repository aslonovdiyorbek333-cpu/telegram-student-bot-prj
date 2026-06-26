import os
import runpy

try:
    import winreg
except ImportError:
    winreg = None   

# Agar Windows bo'lsa va winreg yuklangan bo'lsa, registrdan o'qiydi
if winreg:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment")
        token = winreg.QueryValueEx(key, "TELEGRAM_TOKEN")[0]
        os.environ["TELEGRAM_TOKEN"] = token
    except (FileNotFoundError, Exception):
        token = os.environ.get("TELEGRAM_TOKEN")
else:
    # Linux (Render) muhitida tokenni to'g'ridan-to'g'ri server sozlamalaridan oladi
    token = os.environ.get("TELEGRAM_TOKEN")

# Token umuman topilmasa, xatolik qaytaradi
if not token:
    raise RuntimeError("TELEGRAM_TOKEN muhit o'zgaruvchilaridan yoki registrdan topilmadi!")

# Botni ishga tushirish qismi
runpy.run_path(os.path.join(os.path.dirname(__file__), "bot.py"), run_name="__main__")