import os
import sys
import time
import json
import logging
from io import BytesIO
from pickle import dump, load

from PIL import Image, ImageFilter, ImageTk
from tkinter import (
    filedialog,
    messagebox,
    Toplevel,
    Entry,
    Menu,
    Label,
    Button,
    Tk,
    LabelFrame,
)

# =========================
# Resource Path (PyInstaller Safe)
# =========================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


# =========================
# LOGGING CONFIG
# =========================
logging.basicConfig(
    filename="secura.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log(msg):
    logging.info(msg)


# =========================
# CONFIG (Save Folder Preference)
# =========================
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"default_save_path": os.path.expanduser("~")}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

config = load_config()


# =========================
# Secure Image Class
# =========================
class SecureImage:
    def __init__(self, path, duration, has_password, password):
        with open(path, "rb") as f:
            self.image_bytes = f.read()

        self.make_time = time.time()
        self.duration = duration
        self.destruct_time = self.make_time + duration
        self.has_password = has_password
        self.password = password
        self.corrupted = False

        log(f"CREATED | image={path} | password={has_password} | expires_in={duration}s")

    def get_image(self):
        return Image.open(BytesIO(self.image_bytes))

    def show(self):
        if self.destruct_time > time.time():
            if self.has_password:
                self.ask_password()
            else:
                log("OPENED | success (no password)")
                display_image(self.get_image())
        else:
            self.expire_image()

    def ask_password(self):
        def check():
            if entry.get() == self.password:
                log("OPENED | success (password ok)")
                display_image(self.get_image())
                pw_window.destroy()
            else:
                log("OPENED | wrong password")
                messagebox.showerror("Error", "Incorrect Password")

        pw_window = Toplevel(root)
        pw_window.title("Password Required")

        Label(pw_window, text="Enter Password").pack(padx=20, pady=10)
        entry = Entry(pw_window, show="*")
        entry.pack(padx=20, pady=5)
        Button(pw_window, text="Submit", command=check).pack(pady=10)

    def expire_image(self):
        log("EXPIRED | Corrupting image")

        img = self.get_image()
        img = img.crop((0, 0, img.width // 2, img.height // 5))
        img = img.filter(ImageFilter.BoxBlur(7))

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        self.image_bytes = buffer.getvalue()
        self.corrupted = True

        display_image(img)


# =========================
# Image Display
# =========================
def display_image(img):
    global image_label

    max_size = (780, 520)
    img.thumbnail(max_size)

    tk_img = ImageTk.PhotoImage(img)
    image_label.config(image=tk_img)
    image_label.image = tk_img


def clear_preview():
    image_label.config(image="")
    image_label.image = None


# =========================
# Open Secure File
# =========================
def open_secure_file():
    file_path = filedialog.askopenfilename(
        title="Select Secure File",
        filetypes=(("Secure Files", "*.skr"),)
    )
    if not file_path:
        return

    try:
        with open(file_path, "rb") as f:
            obj = load(f)

        log(f"OPEN_ATTEMPT | file={file_path}")
        obj.show()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file\n{e}")


# =========================
# Create Secure File
# =========================
def create_secure_file():

    def save(event=None):
        duration = int(time_entry.get()) if time_entry.get().isdigit() else 60
        password = password_entry.get().strip()
        has_password = bool(password)
        file_name = filename_entry.get().strip()

        if not file_name:
            messagebox.showerror("Error", "Please provide file name")
            return

        obj = SecureImage(image_path, duration, has_password, password)

        save_path = os.path.join(
            config["default_save_path"],
            file_name + ".skr"
        )

        try:
            with open(save_path, "wb") as f:
                dump(obj, f)

            log(f"SAVED | secure_file={save_path}")
            settings_window.destroy()
            messagebox.showinfo("Success", f"Saved as:\n{save_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Save failed\n{e}")

    image_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=(("Images", "*.png *.jpg *.jpeg"),)
    )
    if not image_path:
        return

    settings_window = Toplevel(root)
    settings_window.title("Security Settings")

    Label(settings_window, text="Expire Time (seconds)").pack(padx=10, pady=5)
    time_entry = Entry(settings_window)
    time_entry.insert(0, "60")
    time_entry.pack(padx=10)

    Label(settings_window, text="Password (optional)").pack(padx=10, pady=5)
    password_entry = Entry(settings_window, show="*")
    password_entry.pack(padx=10)

    Label(settings_window, text="File Name").pack(padx=10, pady=5)
    filename_entry = Entry(settings_window)
    filename_entry.pack(padx=10)

    Button(settings_window, text="Secure & Save", command=save).pack(pady=15)
    settings_window.bind("<Return>", save)


# =========================
# Preferences Window
# =========================
def open_preferences():
    def choose_folder():
        folder = filedialog.askdirectory()
        if folder:
            config["default_save_path"] = folder
            save_config(config)
            messagebox.showinfo("Saved", "Default save folder updated")
            pref_window.destroy()

    pref_window = Toplevel(root)
    pref_window.title("Preferences")

    Label(pref_window, text="Default Save Folder").pack(padx=20, pady=10)
    Button(pref_window, text="Choose Folder", command=choose_folder).pack(pady=10)


# =========================
# UI Setup
# =========================
root = Tk()
root.title("Secura")
root.geometry("800x600")

# Safe icon loading
icon_path = resource_path("icon.ico")
if os.path.exists(icon_path):
    try:
        img_icon = Image.open(icon_path)
        tk_icon = ImageTk.PhotoImage(img_icon)
        root.iconphoto(True, tk_icon)
    except Exception:
        pass

# Menu
menu = Menu(root)
root.config(menu=menu)

file_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Create", menu=file_menu)
file_menu.add_command(label="Secure Image", command=create_secure_file)

view_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Open Secure File", command=open_secure_file)

menu.add_command(label="Preferences", command=open_preferences)
menu.add_command(label="Exit", command=root.quit)

# Display Frame
display_frame = LabelFrame(root, text="Preview", padx=10, pady=10)
display_frame.pack(fill="both", expand=True, padx=20, pady=20)

image_label = Label(display_frame)
image_label.pack(expand=True)

# Clear Preview Button
Button(root, text="Clear Preview", command=clear_preview).pack(pady=5)

root.mainloop()