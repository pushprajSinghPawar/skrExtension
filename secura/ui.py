import os
from pickle import dump, load
from tkinter import (
    filedialog,
    messagebox,
    Toplevel,
    Entry,
    Label,
    Button,
    Menu,
    LabelFrame,
    Tk,
    StringVar,
    OptionMenu,
    Text,
    PanedWindow,
    Frame,
)

from PIL import Image
try:
    from PIL import ImageTk
except ImportError:
    ImageTk = None
    # We'll display a warning when the UI starts if this is needed

from .config import config, save_config
from .logging_util import log
from .resources import resource_path
from .secure_image import ProtectedImage as SecureImage
from .help import make_help_frame


# === display helpers ===

image_label = None  # initialized in main()
root = None  # main Tk instance
# internal paned reference for help toggling
_paned = None


def display_image(img):
    # thumbnail in place to honor max size without copying data
    max_size = (780, 520)
    img.thumbnail(max_size)

    if ImageTk is None:
        # cannot render; inform the user once
        log("WARNING | cannot display image preview because ImageTk is unavailable")
        messagebox.showwarning(
            "Preview unavailable",
            "Image preview requires the Pillow ImageTk module.\n"
            "Install it with:\n    pip install pillow"
        )
        return

    tk_img = ImageTk.PhotoImage(img)
    image_label.config(image=tk_img)
    image_label.image = tk_img


def clear_preview():
    image_label.config(image="")
    image_label.image = None


# === file operations ===

def open_secure_file():
    file_path = filedialog.askopenfilename(
        title="Select Secure File",
        initialdir=config.get("default_save_path", os.path.expanduser("~")),
        filetypes=(("Secure Files", "*.skr"),),
    )
    if not file_path:
        return

    try:
        with open(file_path, "rb") as f:
            obj = load(f)

        log(f"OPEN_ATTEMPT | file={file_path}")
        obj.show()

    except Exception as e:
        # log the detailed exception for debugging
        log(f"OPEN_ERROR | file={file_path} | error={e}")
        messagebox.showerror(
            "Error",
            "Unable to open the selected file. It may be corrupted or incompatible with this version of Secura."
        )


def create_secure_file():

    def save(event=None):
        duration = int(time_entry.get()) if time_entry.get().isdigit() else 60
        password = password_entry.get().strip()
        has_password = bool(password)
        file_name = filename_entry.get().strip()

        if not file_name:
            messagebox.showerror("Error", "Please provide file name")
            return

        obj = SecureImage(image_path, duration, has_password, password)  # alias for ProtectedImage

        save_path = os.path.join(
            config["default_save_path"], file_name + ".skr"
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
        initialdir=config.get("default_image_path", os.path.expanduser("~")),
        filetypes=(("Images", "*.png *.jpg *.jpeg"),),
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
# preference helpers
# =========================

def choose_source_folder():
    """Ask user for image-source folder and save to config."""
    current = config.get("default_image_path", os.path.expanduser("~"))
    folder = filedialog.askdirectory(initialdir=current)
    if folder:
        config["default_image_path"] = folder
        save_config(config)
        messagebox.showinfo("Saved", f"Source folder updated to:\n{folder}")


def choose_destination_folder():
    """Ask user for secure-file destination folder and save to config."""
    current = config.get("default_save_path", os.path.expanduser("~"))
    folder = filedialog.askdirectory(initialdir=current)
    if folder:
        config["default_save_path"] = folder
        save_config(config)
        messagebox.showinfo("Saved", f"Destination folder updated to:\n{folder}")


# === application bootstrap ===

def main():
    global root, image_label

    root = Tk()
    root.title("Secura")
    root.geometry("800x600")
    # log if ImageTk missing; avoid modal dialog on startup
    if ImageTk is None:
        log("WARNING | Pillow ImageTk module not available; image previews may not work.")
    # bind '?' key to open help panel
    root.bind("?", lambda e: toggle_help())

    icon_path = resource_path("icon.ico")
    if os.path.exists(icon_path):
        try:
            img_icon = Image.open(icon_path)
            tk_icon = ImageTk.PhotoImage(img_icon)
            root.iconphoto(True, tk_icon)
        except Exception:
            pass

    menu = Menu(root)
    root.config(menu=menu)

    file_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Create", menu=file_menu)
    file_menu.add_command(label="Secure Image", command=create_secure_file)

    view_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="View", menu=view_menu)
    view_menu.add_command(label="Open Secure File", command=open_secure_file)

    preferences_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Prefereed folder for source/destination", menu=preferences_menu)
    preferences_menu.add_command(label="Source Folder", command=choose_source_folder)
    preferences_menu.add_command(label="Destination Folder", command=choose_destination_folder)

    menu.add_command(label="Exit", command=root.quit)
    menu.add_command(label="Help", command=toggle_help)
    

    # use PanedWindow to host preview and (optionally) help side-by-side
    paned = PanedWindow(root, orient="horizontal")
    paned.pack(fill="both", expand=True, padx=20, pady=20)
    # store global for toggle_help
    global _paned
    _paned = paned

    display_frame = LabelFrame(paned, text="Preview", padx=10, pady=10)
    paned.add(display_frame)

    image_label = Label(display_frame)
    image_label.pack(expand=True)

    Button(root, text="Clear Preview", command=clear_preview).pack(pady=5)

    # create help frame via helper (returns frame and close button)
    help_frame, close_btn = make_help_frame(paned)
    # bind close button to the toggle behavior
    close_btn.config(command=toggle_help)

    # store help_frame in module-level variable for toggle_access
    global _help_frame
    _help_frame = help_frame

    root.mainloop()



# reusable help toggle function; defined at module level so menus can reference it
_help_frame = None
_help_visible = False

def toggle_help():
    """Show or hide the help pane inside the main paned window."""
    global _help_frame, _paned, _help_visible
    if _paned is None or _help_frame is None:
        return
    if _help_visible:
        _paned.forget(_help_frame)
        _help_visible = False
    else:
        _paned.add(_help_frame)
        _help_visible = True

if __name__ == "__main__":
    main()
