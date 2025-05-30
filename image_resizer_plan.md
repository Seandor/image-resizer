# Image Resizer UX Improvement Plan

## Objective
Enhance the user experience of the Image Resizer app by allowing users to select the export format (defaulting to JPG), while continuing to overwrite the original images in the input folder.

---

## Features & Improvements

### 1. Output Format Selection
- Add a dropdown (ttk.Combobox) to the main window for selecting the output format: **JPG** (default), **PNG**, **WEBP**.
- The selected format will be used for all processed images.

### 2. Default to JPG
- The dropdown will default to **JPG**. If the user does not change it, all images will be exported as JPG.

### 3. Overwrite Originals
- Resized images will overwrite the originals in the input folder, using the selected format and updating the file extension as needed.

### 4. Improved Progress and Status Feedback
- The status label will show which file is currently being processed.
- The progress bar and completion message will remain.

### 5. General UX Enhancements
- Add tooltips or help text for the new format selection control.
- Use clear, descriptive labels for all controls.

---

## Proposed UI Layout

```mermaid
flowchart TD
    A[Main Window]
    A --> B[Select Input Folder Button]
    A --> C[Output Format Dropdown (JPG/PNG/WEBP)]
    A --> D[Progress Bar]
    A --> E[Status Label]
```

---

## Implementation Steps

1. Add a ttk.Combobox for format selection, defaulting to JPG.
2. Update the `resize_image` method to use the selected format and save with the correct extension.
3. Update the UI to show the current file being processed.
4. Refactor status/progress updates for clarity.
5. Add tooltips/help text for new controls.

---

## Notes

- The app will continue to overwrite original images in the input folder.
- No output folder selection will be added at this time.
- The README should be updated with new usage instructions after implementation.