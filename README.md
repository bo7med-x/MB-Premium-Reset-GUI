# MBResetX
> GUI wrapper for [Scrut1ny's Malwarebytes-Premium-Reset](https://github.com/Scrut1ny/MB-Premium-Reset)  
> Original batch script by **Scrut1ny** — GUI by **BO7MEDX**

---

## What is this?
The original project by Scrut1ny is a batch script (`.bat`) that resets the Malwarebytes Premium trial.  
This fork adds a modern GUI built with Python + customtkinter so you don't have to run the script manually.  
The original `.bat` file is kept in this repo as a reference to the source.

---

## How to use

### 1. Download Malwarebytes
> Skip this step if Malwarebytes is already installed.

⬇️ [MBSetup.exe](https://data-cdn.mbamupdates.com/web/mb5-setup-consumer/MBSetup.exe)

### 2. Run MBResetX.exe as Administrator
- Right-click `MBResetX.exe` → **Run as administrator**
- Click **"Reset The Trial"** and wait for it to finish

> ⚠️ The app will warn you if you're not running as Administrator.

### 3. Open Malwarebytes
- Let it open normally after the reset

### 4. Setup Malwarebytes
- **DO NOT** click "Activate subscription" or "Buy now"
- Just proceed with the free/trial setup

### 5. Done!
Your premium trial has been reset back to **14 days**.

---

## Files
| File | Description |
|------|-------------|
| `gui/MBResetX.py` | Python GUI source code |
| `gui/icon.ico` | App icon |
| `gui/background.png` | GUI background |
| `Malwarebytes-Premium-Reset.bat` | Original batch script by Scrut1ny (kept as reference) |

---

## Credits
- Original script: [Scrut1ny](https://github.com/Scrut1ny/MB-Premium-Reset)
- GUI wrapper: [BO7MEDX](https://github.com/DevBO7MED) — Telegram: [@PVT_BO](https://t.me/PVT_BO)
