import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os
from pathlib import Path

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        
        # Configure main window
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Select folder button
        self.select_btn = ttk.Button(
            main_frame, 
            text="选择文件夹",
            command=self.select_folder
        )
        self.select_btn.grid(row=0, column=0, pady=20)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Status label
        self.status_var = tk.StringVar(value="请选择要处理的图片文件夹")
        self.status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var
        )
        self.status_label.grid(row=2, column=0, pady=10)
        
    def select_folder(self):
        folder_path = filedialog.askdirectory(title="选择图片文件夹")
        if not folder_path:
            return
            
        self.process_folder(folder_path)
        
    def process_folder(self, folder_path):
        # Get all image files in the folder
        image_files = []
        supported_formats = {'.jpg', '.jpeg', '.png', '.webp'}
        
        for entry in os.scandir(folder_path):
            if entry.is_file():
                ext = Path(entry.name).suffix.lower()
                if ext in supported_formats:
                    image_files.append(entry.path)
                    
        if not image_files:
            messagebox.showinfo("完成", "所选文件夹中没有支持的图片文件")
            return
            
        total_files = len(image_files)
        processed = 0
        
        for img_path in image_files:
            try:
                self.resize_image(img_path)
                processed += 1
                progress = (processed / total_files) * 100
                self.progress_var.set(progress)
                self.status_var.set(f"处理中: {processed}/{total_files}")
                self.root.update()
            except Exception as e:
                messagebox.showerror("错误", f"处理图片时出错: {img_path}\n{str(e)}")
                
        messagebox.showinfo("完成", f"所有图片处理完成！\n共处理 {processed} 个文件")
        self.status_var.set("请选择要处理的图片文件夹")
        self.progress_var.set(0)
        
    def resize_image(self, image_path):
        with Image.open(image_path) as img:
            # Calculate new dimensions
            width, height = img.size
            max_size = 1000
            
            if width <= max_size and height <= max_size:
                return  # No need to resize
                
            # Calculate aspect ratio
            aspect_ratio = width / height
            
            if width > height:
                new_width = max_size
                new_height = int(max_size / aspect_ratio)
            else:
                new_height = max_size
                new_width = int(max_size * aspect_ratio)
                
            # Resize image
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save with original format
            resized_img.save(image_path, quality=95, optimize=True)

def main():
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()