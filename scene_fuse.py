import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview
import subprocess
import time

def get_video_duration(video_path):
    """محاسبه مدت زمان ویدیو با FFprobe"""
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
        return float(result.stdout.decode().strip())
    except:
        return 0

def merge_media(video_folder, image_paths, output_path, image_duration=3):
    """ادغام ویدیوها و تصاویر با FFmpeg (نسخه پایدار)"""
    video_files = sorted([f for f in os.listdir(video_folder) if f.lower().endswith(('.mp4', '.avi', '.mov'))])
    
    inputs = []
    filters = []
    audio_count = 0
    image_times = []
    current_time = 0  # زمان شروع تصاویر و ویدیوها (ثانیه)
    
    # 1. ایجاد ورودی‌های تصاویر با صدای خالی
    for idx, img in enumerate(image_paths[:len(video_files)]):
        if img:
            inputs.extend([ 
                '-loop', '1', 
                '-t', str(image_duration), 
                '-i', img, 
                '-f', 'lavfi', 
                '-t', str(image_duration), 
                '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100'
            ])
            filters.extend([ 
                f"[{2*idx}:v]scale=1920:1080,setsar=1[v{idx}];", 
                f"[{2*idx+1}:a]aformat=sample_fmts=fltp:channel_layouts=stereo[a{idx}];"
            ])
            audio_count += 1
            
            # ثبت زمان قرارگیری تصویر
            start_minutes = int(current_time // 60)
            start_seconds = int(current_time % 60)
            image_times.append(f"تصویر {idx+1} : {start_minutes:02}:{start_seconds:02}")
            current_time += image_duration
    
    # 2. اضافه کردن ویدیوهای اصلی
    for vid in video_files:
        inputs.extend(['-i', os.path.join(video_folder, vid)])
    
    # 3. ساخت زنجیره فیلترها
    video_chain = []
    audio_chain = []
    total_inputs = len(image_paths) * 2
    
    for i in range(len(video_files)):
        # اگر تصویر کاور وجود دارد
        if i < len(image_paths) and image_paths[i]:
            video_chain.append(f"[v{i}]")
            audio_chain.append(f"[a{i}]")
        
        # اضافه کردن ویدیو اصلی و تغییر رزولوشن آن به 1920x1080
        video_chain.append(f"[v{total_inputs + i}]")
        audio_chain.append(f"[{total_inputs + i}:a]")
        
        # اعمال فیلتر scale به ویدیو اصلی
        filters.append(f"[{total_inputs + i}:v]scale=1920:1080,setsar=1[v{total_inputs + i}];")
        
        # زمان شروع و پایان هر ویدیو
        start_minutes = int(current_time // 60)
        start_seconds = int(current_time % 60)
        video_duration = get_video_duration(os.path.join(video_folder, video_files[i]))
        end_minutes = int((current_time + video_duration) // 60)
        end_seconds = int((current_time + video_duration) % 60)
        
        # ثبت زمان شروع و پایان ویدیو
        image_times.append(f"ویدیو {i+1} : {start_minutes:02}:{start_seconds:02}")
        current_time += video_duration
    
    # 4. فیلتر نهایی concat
    filters.append(
        f"{''.join(video_chain)}concat=n={len(video_chain)}:v=1:a=0[outv];"
        f"{''.join(audio_chain)}concat=n={len(audio_chain)}:v=0:a=1[outa]"
    )
    
    # 5. دستور نهایی
    cmd = [
        'ffmpeg',
        '-y',
        *inputs,
        '-filter_complex', ''.join(filters),
        '-map', '[outv]',
        '-map', '[outa]',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-r', '30',
        '-b:v', '12000k',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-strict', 'experimental',
        '-threads', '4',
        output_path
    ]

    try:
        subprocess.run(cmd, check=True, stderr=subprocess.STDOUT)
        messagebox.showinfo("موفق", "ویدیو با موفقیت ساخته شد!")
        
        # ثبت زمان‌ها در فایل TXT
        with open(output_path.replace('.mp4', '_image_times.txt'), 'w', encoding='utf-8') as file:
            file.write("قانون ترتیب نمایش تصاویر:\n")
            file.write("تصویر اول از 00:00 شروع می‌شود.\n")
            
            # محاسبه زمان شروع تصاویر بعدی
            for i in range(1, len(video_files)):
                video_end_time = current_time  # زمان پایان ویدیو قبلی
                video_duration = get_video_duration(os.path.join(video_folder, video_files[i-1]))
                start_minutes = int(video_end_time // 60)
                start_seconds = int(video_end_time % 60)
                file.write(f"تصویر {i+1} زمانی شروع می‌شود که ویدیو {i} به پایان برسد: {start_minutes:02}:{start_seconds:02}\n")
                current_time += video_duration
            
            file.write("\n")
            for time in image_times:
                file.write(time + '\n')
            
            # محاسبه زمان شروع ویدیوها با اضافه کردن 3 ثانیه به پایان ویدیو قبلی
            file.write("\nزمان شروع ویدیوها با اضافه کردن 3 ثانیه:\n")
            current_time_with_pause = 0  # زمان شروع اولیه
            for i in range(len(video_files)):
                video_duration = get_video_duration(os.path.join(video_folder, video_files[i]))
                start_minutes = int(current_time_with_pause // 60)
                start_seconds = int(current_time_with_pause % 60)
                file.write(f"ویدیو {i+1} : {start_minutes:02}:{start_seconds:02}\n")
                current_time_with_pause += video_duration + 3  # اضافه کردن 3 ثانیه به تایم بعدی
            
        return True
    except subprocess.CalledProcessError as e:
        messagebox.showerror("خطا", f"خطا در پردازش:\n{str(e)}")
        return False

# ----------------- GUI Part -----------------
class VideoMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ادغام کننده ویدیوهای حرفه‌ای")
        self.root.geometry("1000x700")
        
        # متغیرها
        self.video_folder = ""
        self.image_paths = {}
        self.output_file = ""
        self.image_duration = 3  # مدت زمان پیش‌فرض تصاویر
        
        # ایجاد رابط کاربری
        self.create_widgets()
    
    def create_widgets(self):
        # فریم جدول
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # جدول
        self.table = Treeview(
            table_frame, 
            columns=('video', 'duration', 'cover'),
            show='headings'
        )
        self.table.heading('video', text='نام ویدیو')
        self.table.heading('duration', text='مدت زمان')
        self.table.heading('cover', text='تصویر کاور')
        self.table.pack(fill='both', expand=True)
        
        # اسکرول بار
        scrollbar = tk.Scrollbar(self.table, orient='vertical')
        scrollbar.pack(side='right', fill='y')
        self.table.config(yscrollcommand=scrollbar.set)
        
        # دکمه‌ها
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(
            btn_frame, 
            text='انتخاب فولدر ویدیوها',
            command=self.select_video_folder
        ).pack(side='left')
        
        tk.Button(
            btn_frame, 
            text='ساخت ویدیو',
            command=self.start_merge,
            bg='green',
            fg='white'
        ).pack(side='right')

        # دکمه اضافه کردن تصاویر گروهی
        tk.Button(
            btn_frame,
            text='انتخاب پوشه تصاویر',
            command=self.select_image_folder
        ).pack(side='left')

            
         # دکمه آبی برای اجرای hajm.py
        button = tk.Button(self.root, text="کاهش حجم فایل خروجی بدون افت کیفیت", command=self.run_script, bg='blue', fg='white')
        button.pack(pady=20)


        # وارد کردن مدت زمان نمایش تصاویر
        duration_label = tk.Label(self.root, text="مدت زمان نمایش هر تصویر (ثانیه):")
        duration_label.pack(padx=10, pady=5)
        
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.insert(0, str(self.image_duration))
        self.duration_entry.pack(padx=10, pady=5)
        
        # رویداد دوبار کلیک
        self.table.bind('<Double-1>', self.select_cover_image)
    
    def run_script(self):
        """این تابع برای اجرای hajm.py است"""
        subprocess.run(['python', 'hajm.py'])

    def select_video_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.video_folder = folder
            self.load_videos()
    
    def load_videos(self):
        self.table.delete(*self.table.get_children())
        videos = sorted([f for f in os.listdir(self.video_folder) if f.lower().endswith(('.mp4', '.avi', '.mov'))])
        
        for vid in videos:
            path = os.path.join(self.video_folder, vid)
            duration = get_video_duration(path)
            mins = int(duration // 60)
            secs = int(duration % 60)
            row_id = self.table.insert('', 'end', values=(vid, f"{mins:02}:{secs:02}", ""))
            self.image_paths[row_id] = ""
    
    def select_cover_image(self, event):
        item = self.table.selection()[0]
        file = filedialog.askopenfilename(filetypes=[("تصاویر", "*.jpg;*.jpeg;*.png")])
        if file:
            self.table.set(item, 'cover', file)
            self.image_paths[item] = file

    def select_image_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            image_files = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            for idx, img in enumerate(image_files):
                if idx < len(self.table.get_children()):
                    row_id = list(self.table.get_children())[idx]
                    self.table.set(row_id, 'cover', os.path.join(folder, img))
                    self.image_paths[row_id] = os.path.join(folder, img)
    
    def start_merge(self):
        output = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 Files", "*.mp4")]
        )
        if output:
            try:
                self.image_duration = int(self.duration_entry.get())  # دریافت مدت زمان وارد شده توسط کاربر
            except ValueError:
                messagebox.showerror("خطا", "لطفاً مدت زمان صحیح وارد کنید!")
                return
            
            image_list = [self.image_paths[row] for row in self.table.get_children()]
            
            # تخمین زمان پردازش
            total_duration = len(image_list) * self.image_duration + sum([get_video_duration(os.path.join(self.video_folder, f)) for f in os.listdir(self.video_folder) if f.lower().endswith(('.mp4', '.avi', '.mov'))])
            minutes = total_duration // 60
            seconds = total_duration % 60
            messagebox.showinfo("تخمین زمان", f"تخمین زمان پردازش: {minutes} دقیقه و {seconds} ثانیه")
            
            # تخفیف فشار CPU با خواباندن کوتاه
            time.sleep(1)
            
            # ساخت ویدیو
            merge_media(self.video_folder, image_list, output, self.image_duration)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoMergerApp(root)
    root.mainloop()
