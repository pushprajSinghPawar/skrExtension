import time
from io import BytesIO
from pickle import dump, load
from PIL import Image, ImageFilter
from tkinter import Toplevel, Label, Entry, Button, messagebox

from .logging_util import log

# compatibility: some previously-saved .skr files referenced a class or module
# path that no longer exists after refactor.  By making our module available
# under those names we allow pickle to locate the class when unpickling.
import sys

# alias this module under old import paths that appeared in earlier releases
for old_name in ("secura.secure_image", "secura.secura", "secura.secure.image"):
    if old_name not in sys.modules:
        sys.modules[old_name] = sys.modules.get(__name__)



class ProtectedImage:
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
                # import here to avoid circular dependency at module import time
                from .ui import display_image

                display_image(self.get_image())
        else:
            self.expire_image()

    def ask_password(self):
        def check():
            if entry.get() == self.password:
                log("OPENED | success (password ok)")
                from .ui import display_image

                display_image(self.get_image())
                pw_window.destroy()
            else:
                log("OPENED | wrong password")
                messagebox.showerror("Error", "Incorrect Password")

        pw_window = Toplevel()
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

        from .ui import display_image

        display_image(img)
