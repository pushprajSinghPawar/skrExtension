import time
import logging
from io import BytesIO
from PIL import Image, ImageFilter
from tkinter import filedialog, messagebox, Toplevel, Entry, Menu, Label, Button, Tk
from pickle import dump, load

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
# Secure Image Class
# =========================
class secureimg:
    def __init__(self, Rasta, samay, gopniyata, kavach) -> None:
        with open(Rasta, "rb") as f:
            self.image_bytes = f.read()

        self.MakeTime = time.time()
        self.Duration = samay
        self.DestructTime = self.MakeTime + self.Duration
        self.ThereIsPaswword = gopniyata
        self.Password = kavach
        self.corrupted = False
        self.original_name = Rasta

        log(
            f"CREATED | image={Rasta} | "
            f"password={'yes' if gopniyata else 'no'} | "
            f"expires_in={samay}s"
        )

    def get_image(self):
        return Image.open(BytesIO(self.image_bytes))

    def dikado(image):
        def show_image(img):
            img.show()

        def dr():
            entered_password = e3.get()
            if entered_password == image.Password:
                log("OPENED | status=success (password ok)")
                img = image.get_image()
                show_image(img)
                open_window.destroy()
            else:
                log("OPENED | status=wrong_password")
                messagebox.showerror("Wrong Password", "Incorrect password")

        # ===== FILE STILL VALID =====
        if image.DestructTime > time.time():

            if image.ThereIsPaswword:
                open_window = Toplevel()
                Label(open_window, text="Enter password").grid(row=0,column=0,padx=20,pady=10)
                e3 = Entry(open_window, show="*")
                e3.grid(row=1,column=0,padx=20,pady=10)
                Button(open_window, text="Submit", command=dr).grid(row=2,column=0,pady=10)

            else:
                log("OPENED | status=success (no password)")
                img = image.get_image()
                show_image(img)

        # ===== FILE EXPIRED =====
        else:
            log("EXPIRED | file time exceeded, corrupting image")

            img = image.get_image()
            img = img.crop((0, 0, img.width // 2, img.height // 5))
            img = img.filter(ImageFilter.BoxBlur(7))

            buf = BytesIO()
            img.save(buf, format="PNG")
            image.image_bytes = buf.getvalue()
            image.corrupted = True

            dump(image, open(str(root.filename2), "wb"))

            log("EXPIRED | image corrupted and saved")
            show_image(img)

# =========================
# Open Secure File
# =========================
def opener():
    root.filename2 = filedialog.askopenfilename(
        title="Select Secure File",
        filetypes=(("secure files","*.skr"),)
    )
    if not root.filename2:
        return

    file_to_object = load(open(root.filename2, "rb"))
    log(f"OPEN_ATTEMPT | file={root.filename2}")
    secureimg.dikado(file_to_object)

# =========================
# Create Secure File
# =========================
import os # Make sure this is at the very top of your file!

# =========================
# Create Secure File
# =========================
def insert_file():
    def fr(event=None):
        p1 = e1.get()
        p2 = e2.get()

        # Input validation
        time_file = int(p1) if p1.isnumeric() else 60
        givenPassword = bool(p2.strip())
        passkey = p2 if givenPassword else ""

        # Create the object
        tmp = secureimg(root.filename, time_file, givenPassword, passkey)

        # 1. Ask where to save (Returns a string path)
        save_path = filedialog.asksaveasfilename(
            title="Save Secure File",
            filetypes=(("secure file", "*.skr"),),
            defaultextension=".skr"
        )

        if save_path:
            # 2. Refactor the name: strip old extension and force .skr
            # os.path.splitext("path/file.png") -> ("path/file", ".png")
            clean_name = os.path.splitext(save_path)[0] + ".skr"

            # 3. Save the file
            with open(clean_name, "wb") as f:
                dump(tmp, f)
            
            log(f"SAVED | secure_file={clean_name}")
            
            # 4. UI Cleanup
            inerter.destroy() 
            messagebox.showinfo("Success", f"File saved successfully as:\n{os.path.basename(clean_name)}")

    # Selection of source image
    root.filename = filedialog.askopenfilename(
        title="Select Image",
        filetypes=(("images","*.png *.jpg *.jpeg"),)
    )
    
    if not root.filename:
        return

    # Create the settings popup
    inerter = Toplevel()
    inerter.title("Security Settings")

    Label(inerter, text="Expire time (seconds)").grid(row=0, column=0, padx=10, pady=5)
    e1 = Entry(inerter)
    e1.insert(0, "60") # Default value for convenience
    e1.grid(row=0, column=1, padx=10)

    Label(inerter, text="Password (optional)").grid(row=1, column=0, padx=10, pady=5)
    e2 = Entry(inerter, show="*")
    e2.grid(row=1, column=1, padx=10)

    Button(inerter, text="Secure & Save", command=fr).grid(row=2, column=0, columnspan=2, pady=15)
    inerter.bind('<Return>', fr)

# =========================
# UI
# =========================
root = Tk()
root.title("Secura")
root.geometry("800x600")
root.iconbitmap("icon.ico")

menu = Menu(root)
root.config(menu=menu)

m1 = Menu(menu, tearoff=0)
menu.add_cascade(label="Create File", menu=m1)
m1.add_command(label="Secure Image", command=insert_file)

m2 = Menu(menu, tearoff=0)
menu.add_cascade(label="View File", menu=m2)
m2.add_command(label="Open Secure File", command=opener)

menu.add_command(label="Exit", command=root.quit)

root.mainloop()
