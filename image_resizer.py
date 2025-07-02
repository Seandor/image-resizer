import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os
from pathlib import Path

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer")
        self.root.geometry("420x280")
        self.root.resizable(False, False)

        # Default format
        self.format_options = ["JPG", "PNG", "WEBP"]
        self.selected_format = tk.StringVar(value="JPG")
        self.max_size_var = tk.StringVar(value="1000")
        self.overwrite_var = tk.BooleanVar(value=True)  # 默认覆盖原文件

        # Configure main window
        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Controls frame for better alignment
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=0, column=0, pady=(10, 0), sticky="n")
        controls_frame.grid_columnconfigure(0, weight=1)

        # Select folder button (first)
        self.select_btn = ttk.Button(
            controls_frame,
            text="选择文件夹",
            command=self.select_folder,
            width=22
        )
        self.select_btn.grid(row=0, column=0, pady=(0, 10), sticky="ew")

        # Output format label and dropdown (second)
        format_label = ttk.Label(controls_frame, text="输出格式 (Output Format):")
        format_label.grid(row=1, column=0, sticky="w", pady=(0, 0))
        self.format_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.selected_format,
            values=self.format_options,
            state="readonly",
            width=22
        )
        self.format_combo.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self.format_combo.set("JPG")
        self.format_combo_tooltip = CreateToolTip(self.format_combo, "选择导出图片格式，默认为JPG (Select export format, default is JPG)")

        # Max size label and entry (third)
        maxsize_label = ttk.Label(controls_frame, text="最大尺寸 (Max Size, px):")
        maxsize_label.grid(row=3, column=0, sticky="w", pady=(0, 0))
        self.maxsize_entry = ttk.Entry(controls_frame, textvariable=self.max_size_var, width=22, justify="center")
        self.maxsize_entry.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        # Overwrite checkbox (fourth)
        self.overwrite_checkbox = ttk.Checkbutton(
            controls_frame,
            text="覆盖原文件 (Overwrite original files)",
            variable=self.overwrite_var
        )
        self.overwrite_checkbox.grid(row=5, column=0, sticky="w", pady=(0, 10))
        self.overwrite_tooltip = CreateToolTip(self.overwrite_checkbox, "选中时覆盖原文件，取消时在子文件夹中保存 (Check to overwrite originals, uncheck to save in subfolder)")

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=10)

        # Status label
        self.status_var = tk.StringVar(value="请选择要处理的图片文件夹")
        self.status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var
        )
        self.status_label.grid(row=2, column=0, pady=10, sticky="ew")

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

        output_format = self.selected_format.get().upper()
        format_ext_map = {"JPG": ".jpg", "PNG": ".png", "WEBP": ".webp"}
        pil_format_map = {"JPG": "JPEG", "PNG": "PNG", "WEBP": "WEBP"}

        # Get max size from entry, fallback to 1000 if invalid
        try:
            max_size = int(self.max_size_var.get())
            if max_size <= 0:
                raise ValueError
        except Exception:
            max_size = 1000

        for img_path in image_files:
            try:
                self.status_var.set(f"处理中: {os.path.basename(img_path)} ({processed+1}/{total_files})")
                self.root.update()
                self.resize_image(img_path, output_format, format_ext_map, pil_format_map, max_size)
                processed += 1
                progress = (processed / total_files) * 100
                self.progress_var.set(progress)
            except Exception as e:
                messagebox.showerror("错误", f"处理图片时出错: {img_path}\n{str(e)}")

        # 显示完成消息
        if self.overwrite_var.get():
            message = f"所有图片处理完成！\n共处理 {processed} 个文件\n文件已覆盖原位置"
        else:
            message = f"所有图片处理完成！\n共处理 {processed} 个文件\n文件已保存到: resized_images_square 文件夹"
        messagebox.showinfo("完成", message)
        self.status_var.set("请选择要处理的图片文件夹")
        self.progress_var.set(0)

    def resize_image(self, image_path, output_format, format_ext_map, pil_format_map, max_size):
        with Image.open(image_path) as img:
            # Step 1: 如果图片超过max_size，先按比例缩放
            width, height = img.size
            
            if width > max_size or height > max_size:
                # 按比例缩放到max_size以内
                if width > height:
                    new_width = max_size
                    new_height = int(max_size * height / width)
                else:
                    new_height = max_size
                    new_width = int(max_size * width / height)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                width, height = new_width, new_height
            
            # Step 2: 智能正方形策略
            square_img = self.create_smart_square(img, width, height)
            
            # Step 3: 保存正方形图片
            self.save_with_format(square_img, image_path, output_format, format_ext_map, pil_format_map)

    def create_smart_square(self, img, width, height):
        """智能创建正方形图片：根据长宽比选择拉伸或填充策略"""
        # 计算长宽比
        aspect_ratio = max(width, height) / min(width, height)
        square_size = max(width, height)
        
        if aspect_ratio <= 1.2:
            # 长宽比差距较小：直接拉伸 (变形不明显)
            return img.resize((square_size, square_size), Image.Resampling.LANCZOS)
        else:
            # 长宽比差距较大：白色填充居中 (保持比例)
            # 创建白色正方形画布
            if img.mode in ('RGBA', 'LA'):
                # 对于有透明通道的图片，先创建RGBA画布
                square_canvas = Image.new('RGBA', (square_size, square_size), (255, 255, 255, 255))
            else:
                square_canvas = Image.new('RGB', (square_size, square_size), (255, 255, 255))
            
            # 计算居中位置
            paste_x = (square_size - width) // 2
            paste_y = (square_size - height) // 2
            
            # 将原图粘贴到画布中心
            if img.mode == 'RGBA':
                square_canvas.paste(img, (paste_x, paste_y), img)
            else:
                square_canvas.paste(img, (paste_x, paste_y))
            
            return square_canvas

    def save_with_format(self, img, orig_path, output_format, format_ext_map, pil_format_map):
        # 获取输出路径
        new_path = self.get_output_path(orig_path, output_format, format_ext_map)
        pil_format = pil_format_map[output_format]
        save_kwargs = {"quality": 95, "optimize": True} if pil_format == "JPEG" else {}

        # 处理透明通道和图片模式兼容性
        img = self.handle_transparency(img, pil_format)

        img.save(new_path, pil_format, **save_kwargs)
        
        # 只有在覆盖模式且文件扩展名改变时才删除原文件
        if self.overwrite_var.get() and new_path != orig_path and os.path.exists(orig_path):
            try:
                os.remove(orig_path)
            except Exception:
                pass

    def handle_transparency(self, img, pil_format):
        """处理透明通道和不兼容的图片模式"""
        if pil_format == "JPEG":
            if img.mode in ("RGBA", "LA"):
                # 处理透明通道：创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == "RGBA":
                    background.paste(img, mask=img.split()[-1])  # 使用alpha通道作为mask
                elif img.mode == "LA":
                    background.paste(img, mask=img.split()[-1])  # 使用alpha通道作为mask
                return background
            elif img.mode == "P":
                # 处理调色板模式：转换为RGB
                if "transparency" in img.info:
                    # 如果有透明度信息，先转换为RGBA再处理透明背景
                    img = img.convert("RGBA")
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    return background
                else:
                    # 直接转换为RGB
                    return img.convert("RGB")
            elif img.mode not in ("RGB", "L"):
                # 其他不兼容模式直接转换为RGB
                return img.convert("RGB")
        return img

    def get_output_path(self, orig_path, output_format, format_ext_map):
        """获取输出文件路径"""
        dir_name = os.path.dirname(orig_path)
        base_name = os.path.splitext(os.path.basename(orig_path))[0]
        new_ext = format_ext_map[output_format]
        
        if self.overwrite_var.get():
            # 覆盖模式：在原位置
            return os.path.join(dir_name, base_name + new_ext)
        else:
            # 非覆盖模式：创建子文件夹
            output_dir = os.path.join(dir_name, "resized_images_square")
            os.makedirs(output_dir, exist_ok=True)
            return os.path.join(output_dir, base_name + new_ext)

# Tooltip helper class
class CreateToolTip(object):
    """
    Create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     # miliseconds
        self.wraplength = 220   # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()

import sys

def main():
    # High-DPI awareness for Windows (improves clarity on 4K screens)
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    root = tk.Tk()
    # Set scaling for high-DPI screens (2.0 is good for 4K, adjust as needed)
    try:
        root.tk.call('tk', 'scaling', 2.0)
    except Exception:
        pass

    app = ImageResizerApp(root)
    # Set a minimum window width for harmony
    root.update_idletasks()
    root.minsize(340, root.winfo_height())
    root.mainloop()

if __name__ == "__main__":
    main()