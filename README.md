# Secure Image Viewer

This Python project allows you to create secure image files (.skr) and view them using a secure image viewer. The viewer ensures that the image can only be viewed under certain conditions, such as a specified time period or password protection.

`I have given the executable file for anyone to download.`

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


## Usage

To create a secure image file:

1. Run the program.
2. Click on "Create a File" in the menu.
3. Select the image file you want to secure.
4. Enter the time period (in seconds) after which the file should be destroyed or corrupted.
5. Optionally, enter a password for additional protection.
6. Choose whether the file can only be opened on the current device or any device.
7. Click "Submit" to create the secure image file (.skr).

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
