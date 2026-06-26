import os
import runpy
import winreg

key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment")
try:
    token = winreg.QueryValueEx(key, "TELEGRAM_TOKEN")[0]
except FileNotFoundError:
    token = None

if not token:
    raise RuntimeError("TELEGRAM_TOKEN not found in HKCU\\Environment")

os.environ["TELEGRAM_TOKEN"] = token
runpy.run_path(os.path.join(os.path.dirname(__file__), "bot.py"), run_name="__main__")
