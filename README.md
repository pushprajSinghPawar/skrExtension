# Secure Image Viewer

This Python project allows you to create secure image files (.skr) and view them using a secure image viewer. The viewer ensures that the image can only be viewed under certain conditions, such as a specified time period or password protection.

## Prerequisites

Make sure you have the following libraries installed:

- `email.mime.image`
- `fileinput`
- `time`
- `PIL` (Python Imaging Library)
- `tkinter`
- `pickle`
- `uuid`
- `pyparsing`

You can install these libraries using `pip`:

## Installation Guide

To create a secure image file:

### Option 1: Running from Source (Recommended for Developers)

Use this method if you want to view the code, make changes, or run the program using a Python interpreter.

1. **Navigate to the Project Root:**
   Open your terminal or command prompt and change the directory to the folder where you downloaded the project:
   **Bash**

   ```
   cd path/to/SKREXTENSION
   ```
2. **Install Dependencies:**
   Run the following command to install all necessary libraries listed in the `requirements.txt` file:
   **Bash**

   ```
   pip install -r requirements.txt
   ```
3. **Run the Program:**
   Once the installation is complete, launch the application using:
   **Bash**

   ```
   python Secura.py
   ```

To create a secure image file:

1. Run the program.
2. Click on "Create File" in the menu.
3. Select the image file you want to convert.
4. Then Enter the Expire time (in seconds) and password if it has to be password protected and then submit .
6. Then enter the name of the file to be saved as a encrypted one in the memory.
7.


To view a secure image file:

1. Run the program.
2. Click on "View the File" in the menu.
3. Select the secure image file (.skr) you want to view.
4. The viewer will determine if the file is still valid based on the time period and password protection.
5. If allowed, the image will be displayed. If not, an error message will be shown.

## Notes

- The secure image viewer checks the time period and password protection to determine if the file can be viewed.
- If the time period has expired or the password is incorrect, the file may be corrupted and displayed accordingly.
- The secure image file (.skr) is a custom file format that stores the image and its associated information.
- The program uses the `pickle` module to handle file operations and `PIL` for image manipulation.
- The `uuid` module is used to generate a unique identifier for the device.
- The `pyparsing` module is used for parsing and validating input.
- The secure image file can only be viewed using the secure image viewer.

Please ensure that you have the necessary permissions to view and modify the files in your system.
