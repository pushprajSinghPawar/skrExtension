import os
import sys


def resource_path(relative_path):
    """Return an absolute path for resources, handling PyInstaller's _MEIPASS."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
