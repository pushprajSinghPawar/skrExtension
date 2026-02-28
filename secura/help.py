"""Help content and helper for Secura UI."""

HELP_TEXT = (
    "Welcome to Secura!\n"
    "===================\n\n"
    "Secura lets you protect images by converting them into self-destructing,\
"
    "secure files (.skr). To get started, follow these simple steps:\n\n"
    "1. **Create a Secure Image**\n"
    "   * Choose `Create -> Secure Image` from the menu.\n"
    "   * Pick an image file (PNG/JPEG). The dialog will start in your Source Folder.\n"
    "   * Enter how many seconds it should remain viewable and an optional password.\n"
    "   * Give the output a name. The resulting .skr file will be saved to the Destination Folder.\n\n"
    "2. **View a Secure Image**\n"
    "   * Select `View -> Open Secure File` and pick a .skr file.\n"
    "   * If the file has expired or the password is wrong, it will corrupt and\
"
    "     become unreadable. Otherwise the original image appears.\n\n"
    "3. **Change Defaults**\n"
    "   * Use `Preferences -> Source Folder` / `Destination Folder` to set your\
"
    "     most-used locations. The application remembers them across runs.\n\n"
    "4. **Help Panel**\n"
    "   * Toggle this guide via `Help -> Help` or press the `?` key. You can\
"
    "     resize or close the panel anytime.\n\n"
    "Tips:\n"
    "* Files are stored using Python's `pickle` so avoid untrusted sources.\n"
    "* The secure format prevents viewing after the lifetime expires.\n"
    "* You can distribute the .skr files, but the recipient needs Secura too.\n"
)


def make_help_frame(parent):
    """Return a frame containing help text suitable for embedding in the UI.

    The caller is responsible for adding/removing the returned widget from a
    `PanedWindow`.
    """
    from tkinter import LabelFrame, Frame, Button, Text

    frame = LabelFrame(parent, text="Help", padx=5, pady=5)
    header = Frame(frame)
    header.pack(fill="x", side="top")
    close_btn = Button(header, text="✕", width=3)
    close_btn.pack(side="left")

    text_widget = Text(frame, wrap="word")
    text_widget.insert("1.0", HELP_TEXT)
    text_widget.config(state="disabled")
    text_widget.pack(fill="both", expand=True)

    return frame, close_btn
