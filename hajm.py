import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import json

def get_file_size(file_path):
    """حجم فایل را با استفاده از os به بایت می‌خواند."""
    try:
        return os.path.getsize(file_path)  # اندازه فایل به بایت
    except Exception as e:
        messagebox.showerror("خطا", f"خطا در دریافت حجم فایل: {str(e)}")
        return None

def get_video_size(file_path):
    """این تابع حجم ویدیو را می‌خواند و اطلاعات ابعاد را می‌گیرد."""
    try:
        # استفاده از ffprobe برای استخراج اطلاعات ویدیو
        probe = subprocess.check_output(
            ['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height', '-of', 'json', file_path],
            stderr=subprocess.STDOUT, universal_newlines=True
        )
        print(probe)  # چاپ خروجی برای بررسی اطلاعات کامل
        data = json.loads(probe)

        # بررسی اینکه اطلاعات مورد نظر موجود است
        if 'streams' not in data or len(data['streams']) == 0:
            messagebox.showerror("خطا", "اطلاعات ویدیویی در فایل پیدا نشد.")
            return None, None, None
        
        # انتخاب اولین جریان ویدیو
        video_stream = None
        for stream in data['streams']:
            if 'width' in stream and 'height' in stream:
                video_stream = stream
                break

        if not video_stream:
            messagebox.showerror("خطا", "جریان ویدیو پیدا نشد.")
            return None, None, None

        width = int(video_stream['width'])  # عرض ویدیو
        height = int(video_stream['height'])  # ارتفاع ویدیو

        # گرفتن حجم فایل از طریق os.path.getsize
        size = get_file_size(file_path)
        if size is None:
            return None, None, None

        return size, width, height
    except subprocess.CalledProcessError as e:
        print("خطا در پردازش ویدیو:", e.output)
        messagebox.showerror("خطا", "مشکلی در پردازش ویدیو پیش آمد.")
        return None, None, None
    except ValueError as e:
        print("خطا در استخراج ابعاد ویدیو:", e)
        messagebox.showerror("خطا", "اطلاعات ویدیو به‌درستی استخراج نشد.")
        return None, None, None

def estimate_compression_size(size):
    """تخمین حجم پس از فشرده‌سازی (به‌عنوان مثال 40% از حجم اصلی)"""
    estimated_size = size * 0.4  # تخمین کاهش حجم به 40% از حجم اصلی
    return estimated_size

def choose_video():
    """این تابع برای انتخاب ویدیو از طریق فایل‌دایلاگ استفاده می‌شود."""
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.mkv *.avi *.mov")])
    if file_path:
        # نمایش اطلاعات ویدیو
        size, width, height = get_video_size(file_path)
        if size and width and height:
            original_size_label.config(text=f"حجم اولیه: {size / (1024 * 1024):.2f} MB")
            video_info_label.config(text=f"ابعاد ویدیو: {width}x{height}")
            
            # تخمین حجم پس از کاهش
            estimated_size = estimate_compression_size(size)
            estimated_size_label.config(text=f"حجم تخمینی بعد از کاهش: {estimated_size / (1024 * 1024):.2f} MB")
            
            # دکمه انتخاب مسیر خروجی فعال می‌شود
            save_button.config(state=tk.NORMAL, command=lambda: choose_output_path(file_path))

def choose_output_path(input_path):
    """این تابع به کاربر اجازه می‌دهد مسیر و نام فایل خروجی را انتخاب کند."""
    output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if output_path:
        # دکمه شروع فرآیند فشرده‌سازی فعال می‌شود
        compress_button.config(state=tk.NORMAL, command=lambda: compress_video_task(input_path, output_path))

def compress_video_task(input_path, output_path):
    """این تابع فشرده‌سازی ویدیو را انجام می‌دهد و به کاربر اطلاع می‌دهد."""
    try:
        # فرمان ffmpeg برای فشرده‌سازی ویدیو
        command = [
            'ffmpeg', '-i', input_path, '-vcodec', 'libx264', '-crf', '18', '-preset', 'medium', 
            '-vf', 'scale=-2:1080', output_path
        ]
        subprocess.run(command, check=True)
        messagebox.showinfo("عملیات موفق", f"ویدیو با موفقیت فشرده شد: {output_path}")
    except subprocess.CalledProcessError as e:
        print("خطا در فشرده‌سازی ویدیو:", e.output)
        messagebox.showerror("خطا", "مشکلی در فشرده‌سازی ویدیو پیش آمد.")

# ایجاد پنجره اصلی
root = tk.Tk()
root.title("کاهش حجم ویدیو بدون افت کیفیت")

# نمایش اطلاعات
original_size_label = tk.Label(root, text="حجم اولیه: -- MB", font=('Arial', 12))
original_size_label.pack(pady=10)

video_info_label = tk.Label(root, text="ابعاد ویدیو: --x--", font=('Arial', 12))
video_info_label.pack(pady=10)

estimated_size_label = tk.Label(root, text="حجم تخمینی بعد از کاهش: -- MB", font=('Arial', 12))
estimated_size_label.pack(pady=10)

# دکمه انتخاب ویدیو
choose_button = tk.Button(root, text="انتخاب ویدیو", command=choose_video, font=('Arial', 12))
choose_button.pack(pady=20)

# دکمه انتخاب مسیر خروجی
save_button = tk.Button(root, text="انتخاب مسیر خروجی", state=tk.DISABLED, font=('Arial', 12))
save_button.pack(pady=10)

# دکمه فشرده‌سازی
compress_button = tk.Button(root, text="شروع فشرده‌سازی", state=tk.DISABLED, font=('Arial', 12))
compress_button.pack(pady=20)

# شروع برنامه
root.mainloop()
