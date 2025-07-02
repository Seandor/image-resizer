# Image Resizer - Enhanced Version

A powerful batch image resizer with intelligent square output and transparent background handling. Select a folder of images, choose output format, and convert all images to perfect squares using smart algorithms.

---

## ✨ Features

- **智能正方形输出 (Smart Square Output)**:
  - 长宽比≤1.2: 直接拉伸 (minimal distortion)
  - 长宽比>1.2: 白色填充居中 (preserve aspect ratio)
- **透明背景处理 (Transparency Handling)**: PNG透明部分转换为白色背景
- **输出选项 (Output Options)**: 选择覆盖原文件或保存到子文件夹
- **多格式支持 (Format Support)**: JPG, PNG, WEBP输入输出
- **批处理 (Batch Processing)**: 一键处理整个文件夹
- **进度显示 (Progress Tracking)**: 实时显示处理进度

---

## 📖 Usage

1. **安装依赖 (Install requirements):**
   ```bash
   pip install -r requirements.txt
   ```

2. **运行程序 (Run the app):**
   ```bash
   python image_resizer.py
   ```

3. **使用方法 (How to use):**
   - 点击 **"选择文件夹"** 按钮选择包含图片的文件夹
   - 选择 **"输出格式"**: JPG (默认), PNG, 或 WEBP
   - 设置 **"最大尺寸"**: 默认1000像素
   - 选择 **"覆盖原文件"**:
     - ✅ 选中: 覆盖原文件位置
     - ❌ 取消: 保存到 `resized_images_square` 子文件夹
   - 程序将所有图片转换为正方形并显示进度

4. **智能正方形算法 (Smart Square Algorithm):**
   - 📐 **长宽比 ≤ 1.2**: 轻微拉伸成正方形
   - 🖼️ **长宽比 > 1.2**: 白色背景填充，图片居中

---

## 📝 Notes

- 🔄 **智能处理**: 自动选择最佳的正方形转换策略
- 🎨 **透明背景**: PNG透明部分自动转换为白色背景
- 📁 **输出选项**: 可选择覆盖原文件或保存到新文件夹
- 🎯 **支持格式**: JPG, JPEG, PNG, WEBP (输入和输出)
- ⚠️ **备份提醒**: 覆盖模式下建议先备份原文件

---

## Requirements

- Python 3.7+
- Pillow
- tkinter (usually included with Python)