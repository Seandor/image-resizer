# Image Resizer

A simple batch image resizer with a graphical interface. Select a folder of images, choose the output format (JPG, PNG, WEBP), and resize all images to a maximum of 1000px (width or height). The app overwrites the original images with the resized versions in the selected format.

---

## Features

- **Batch resize** all images in a selected folder.
- **Output format selection:** JPG (default), PNG, or WEBP.
- **Overwrites original images** with the resized images in the selected format.
- **Progress bar** and status updates during processing.
- **Simple, user-friendly interface.**

---

## Usage

1. **Install requirements:**
   ```
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```
   python image_resizer.py
   ```

3. **How to use:**
   - Click the **"选择文件夹"** ("Select Folder") button to choose a folder containing images.
   - Use the **"输出格式 (Output Format)"** dropdown to select the desired export format (JPG, PNG, or WEBP). The default is JPG.
   - The app will resize all supported images (`.jpg`, `.jpeg`, `.png`, `.webp`) in the folder to a maximum of 1000px (width or height), and overwrite them in the selected format.
   - Progress and status will be displayed during processing.
   - When finished, a message box will show the number of files processed.

---

## Notes

- The app will **overwrite original images** in the selected folder. Make backups if needed.
- The file extension will be updated to match the selected format.
- Supported input formats: JPG, JPEG, PNG, WEBP.

---

## Requirements

- Python 3.7+
- Pillow
- tkinter (usually included with Python)