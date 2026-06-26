# =============================================
#  MBResetX - Malwarebytes Trial Reset GUI
# =============================================
#  Original batch script by : Scrut1ny
#  Source : https://github.com/Scrut1ny/MB-Premium-Reset
#
#  GUI wrapper by : BO7MEDX
#  GitHub   : https://github.com/bo7med-x
# =============================================

import customtkinter as ctk
import subprocess
import threading
import os
import time
import sys
from tkinter import messagebox
from customtkinter import CTkImage
from PIL import Image
import tkinter as tk

CREATE_NO_WINDOW = 0x08000000

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# =============================================
# Basic Setup
# =============================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()

try:
    window.iconbitmap(resource_path("icon.ico"))
except:
    try:
        icon_img = tk.PhotoImage(file=resource_path("icon.png"))
        window.iconphoto(True, icon_img)
        window.icon_img = icon_img
    except:
        pass

window.title("MBResetX BY BO7MEDX")
window.geometry("500x340")
window.resizable(False, False)

window.update_idletasks()
width = window.winfo_width()
height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)
window.geometry(f"{width}x{height}+{x}+{y}")

is_running = False

# =============================================
# Admin Check at Startup
# =============================================
def is_admin():
    try:
        return subprocess.run(
            ["fltmc"],
            capture_output=True,
            creationflags=CREATE_NO_WINDOW
        ).returncode == 0
    except:
        return False

if not is_admin():
    msg = ("This program requires Administrator privileges to run.\n\n"
           "Please restart the program as Administrator.")
    messagebox.showerror("Admin Rights Required", msg, parent=window)
    sys.exit(1)

# =============================================
# Button 1 - Check Admin Rights
# =============================================
def check_admin():
    if is_admin():
        messagebox.showinfo("Admin Check — OK", "You are running as Administrator.\n\nYou're good to go!", parent=window)
    else:
        messagebox.showwarning("Admin Check — Failed", "Not running as Administrator.\n\nPlease restart the program as Administrator.", parent=window)

# =============================================
# Helper Functions
# =============================================

def stop_services():
    path_x86 = os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "Malwarebytes", "Anti-Malware", "malwarebytes_assistant.exe")
    path_x64 = os.path.join(os.environ.get("PROGRAMFILES", ""), "Malwarebytes", "Anti-Malware", "malwarebytes_assistant.exe")

    if os.path.exists(path_x86):
        subprocess.run([path_x86, "--stopservice"], capture_output=True, creationflags=CREATE_NO_WINDOW)
    elif os.path.exists(path_x64):
        subprocess.run([path_x64, "--stopservice"], capture_output=True, creationflags=CREATE_NO_WINDOW)
    else:
        messagebox.showwarning("Not Found", "Malwarebytes assistant not found in expected locations.", parent=window)
        return

    subprocess.run(["taskkill", "/f", "/im", "MBAMService.exe"], capture_output=True, creationflags=CREATE_NO_WINDOW)
    time.sleep(5)

def refresh_machine_guid():
    result = subprocess.run(
        ["powershell", "-c", "[guid]::NewGuid().ToString()"],
        capture_output=True,
        text=True,
        creationflags=CREATE_NO_WINDOW
    )
    new_guid = result.stdout.strip()
    if new_guid:
        subprocess.run([
            "reg", "add",
            r"HKLM\SOFTWARE\Microsoft\Cryptography",
            "/v", "MachineGuid",
            "/t", "REG_SZ",
            "/d", new_guid,
            "/f"
        ], capture_output=True, creationflags=CREATE_NO_WINDOW)

def manage_scheduled_task(action):
    task_name = "Malwarebytes-Premium-Reset"

    if action == "delete":
        check = subprocess.run(
            ["schtasks", "/query", "/tn", task_name],
            capture_output=True,
            creationflags=CREATE_NO_WINDOW
        )
        if check.returncode == 0:
            subprocess.run(
                ["schtasks", "/delete", "/tn", task_name, "/f"],
                capture_output=True,
                creationflags=CREATE_NO_WINDOW
            )
            time.sleep(2)

    elif action == "create":
        cmd = f'"{os.environ.get("COMSPEC", "cmd.exe")}" /c "echo Task executed"'
        subprocess.run([
            "schtasks", "/create",
            "/tn", task_name,
            "/tr", cmd,
            "/sc", "daily",
            "/mo", "13",
            "/rl", "highest"
        ], capture_output=True, creationflags=CREATE_NO_WINDOW)
        time.sleep(3)

    elif action == "run":
        subprocess.run(
            ["schtasks", "/run", "/tn", task_name],
            capture_output=True,
            creationflags=CREATE_NO_WINDOW
        )
        time.sleep(5)

def restart_malwarebytes():
    path_x86 = os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "Malwarebytes", "Anti-Malware", "malwarebytes_assistant.exe")
    path_x64 = os.path.join(os.environ.get("PROGRAMFILES", ""), "Malwarebytes", "Anti-Malware", "malwarebytes_assistant.exe")

    if os.path.exists(path_x86):
        subprocess.Popen([path_x86], creationflags=CREATE_NO_WINDOW)
    elif os.path.exists(path_x64):
        subprocess.Popen([path_x64], creationflags=CREATE_NO_WINDOW)
    time.sleep(5)

def run_mbsetup():
    script_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
    mbsetup_path = os.path.join(script_dir, "MBSetup.exe")
    if os.path.exists(mbsetup_path):
        subprocess.Popen([mbsetup_path], creationflags=CREATE_NO_WINDOW)

# =============================================
# Button 2 - Run Full Maintenance
# =============================================

def run_full_maintenance():
    global is_running

    if is_running:
        messagebox.showwarning("Please Wait", "Maintenance is already running.\n\nPlease wait for it to finish.", parent=window)
        return

    confirm = messagebox.askyesno("Confirm", "This will run the full Malwarebytes maintenance.\n\nAre you sure you want to continue?", parent=window)
    if not confirm:
        return

    is_running = True
    btn_maintenance.configure(state="disabled", text=" Please Wait...")

    def maintenance_thread():
        global is_running

        try:
            stop_services()
            time.sleep(5)
            manage_scheduled_task("delete")
            time.sleep(3)
            refresh_machine_guid()
            time.sleep(3)
            manage_scheduled_task("create")
            time.sleep(5)
            manage_scheduled_task("run")
            time.sleep(3)
            restart_malwarebytes()
            run_mbsetup()

            window.after(100, lambda: messagebox.showinfo(
                "Done!",
                "Maintenance completed successfully!\n\n"
                "You can now restart Malwarebytes if needed.",
                parent=window
            ))

        except Exception as e:
            window.after(100, lambda: messagebox.showerror(
                "Error",
                f"Something went wrong during maintenance.\n\n{e}",
                parent=window
            ))

        is_running = False
        btn_maintenance.configure(state="normal", text=" Reset The Trial")

    t = threading.Thread(target=maintenance_thread)
    t.daemon = True
    t.start()

# =============================================
# About
# =============================================
def show_about():
    about_text = (
        "MBResetX v1.0\n"
        "Malwarebytes Trial Reset — GUI Edition\n\n"
        "Original batch script by: Scrut1ny\n"
        "github.com/Scrut1ny/MB-Premium-Reset\n\n"
        "GUI wrapper by: BO7MEDX\n"
        "GitHub: github.com/bo7med-x\n"
    )
    messagebox.showinfo("About", about_text, parent=window)

# =============================================
# UI
# =============================================

window.configure(fg_color="#0D1117")

window.grid_rowconfigure(0, weight=0)
window.grid_rowconfigure(1, weight=0)
window.grid_rowconfigure(2, weight=1)
window.grid_columnconfigure(0, weight=1)

bg_path = resource_path("background.png")
if os.path.exists(bg_path):
    pil_image = Image.open(bg_path)
    bg_image = CTkImage(light_image=pil_image, size=(500, 340))
    bg_label = ctk.CTkLabel(window, image=bg_image, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    window.bg_image = bg_image
else:
    window.configure(fg_color="#0D1117")

# Title Frame
frame_title = ctk.CTkFrame(window, corner_radius=14, fg_color="#161B22", border_width=1, border_color="#30363D")
frame_title.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 10))

frame_title.grid_columnconfigure(0, weight=1)
frame_title.grid_rowconfigure(0, weight=1)

label_icon = ctk.CTkLabel(
    frame_title,
    text="    🛡️",
    font=ctk.CTkFont(family="Segoe UI", size=44, weight="bold")
)
label_icon.grid(row=0, column=0, pady=(15, 2))

label_title = ctk.CTkLabel(
    frame_title,
    text="Malwarebytes Trial Reset",
    font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
    text_color="green"
)
label_title.grid(row=1, column=0, pady=(0, 2))

label_subtitle = ctk.CTkLabel(
    frame_title,
    text="v1.0  |  BY: BO7MEDX",
    font=ctk.CTkFont(family="Segoe UI", size=13),
    text_color="Red"
)
label_subtitle.grid(row=2, column=0, pady=(2, 14))

# Buttons Frame
frame_buttons = ctk.CTkFrame(window, corner_radius=14, fg_color="#161B22", border_width=1, border_color="#30363D")
frame_buttons.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 12))

frame_buttons.grid_columnconfigure(0, weight=1)
frame_buttons.grid_columnconfigure(1, weight=0)
frame_buttons.grid_columnconfigure(2, weight=0)
frame_buttons.grid_columnconfigure(3, weight=1)
frame_buttons.grid_rowconfigure(0, weight=1)

btn_check = ctk.CTkButton(
    frame_buttons,
    text="Check Admin Rights",
    height=48,
    width=160,
    corner_radius=10,
    font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
    fg_color="#21262D",
    hover_color="#2D333B",
    border_width=1,
    border_color="#388BFD",
    text_color="#58A6FF",
    command=check_admin
)
btn_check.grid(row=0, column=1, padx=5, pady=14)

btn_maintenance = ctk.CTkButton(
    frame_buttons,
    text=" Reset The Trial",
    height=48,
    width=180,
    corner_radius=10,
    font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
    fg_color="#1F6FEB",
    hover_color="#388BFD",
    text_color="white",
    command=run_full_maintenance
)
btn_maintenance.grid(row=0, column=2, padx=5, pady=14)

# Status Frame
frame_status = ctk.CTkFrame(window, height=40, corner_radius=10, fg_color="#161B22", border_width=1, border_color="#30363D")
frame_status.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 14))
frame_status.grid_propagate(False)

frame_status.grid_columnconfigure(0, weight=1)
frame_status.grid_columnconfigure(1, weight=0)
frame_status.grid_columnconfigure(2, weight=1)
frame_status.grid_rowconfigure(0, weight=1)

btn_about = ctk.CTkButton(
    frame_status,
    text="About",
    width=70,
    height=28,
    corner_radius=6,
    font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
    fg_color="#21262D",
    hover_color="#2D333B",
    border_width=1,
    border_color="#30363D",
    text_color="#8B949E",
    command=show_about
)
btn_about.grid(row=0, column=1, padx=0, pady=0)

window.mainloop()