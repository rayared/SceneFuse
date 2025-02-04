# SceneFuse
SceneFuse نرم‌افزاری است برای اتصال خودکار کلیپ‌ها به یکدیگر و افزودن کاورهای دلخواه به فیلم‌ها، بدون افت کیفیت صدا و تصویر. این ابزار برای استفاده در پلتفرم‌های ویدئویی مانند آپارات یا یوتیوب طراحی شده است. با این نرم‌افزار می‌توانید کلیپ‌ها را به راحتی به هم متصل کنید و کاورهای سفارشی را پیش از هر کلیپ قرار دهید.

ویژگی‌ها:
اتصال خودکار کلیپ‌ها: این نرم‌افزار به‌طور خودکار کلیپ‌های مختلف را به یکدیگر متصل می‌کند.
قرار دادن کاور: قابلیت افزودن کاور با مدت زمان دلخواه قبل از هر کلیپ.
خروجی تکست: ایجاد فایل تکست که موقعیت قرارگیری کاور‌ها را در ویدیو یکپارچه نمایش می‌دهد (برای استفاده در آپارات و یوتیوب).
بدون افت کیفیت: تمام عملیات انجام‌شده بدون هیچ‌گونه افت کیفیتی در صدا و تصویر صورت می‌گیرد.
نوشته‌شده با پایتون: نرم‌افزار با زبان پایتون توسعه یافته است.

نحوه استفاده:
پروژه را کلون کنید.
تمام وابستگی‌ها را نصب کنید.
برنامه را اجرا کنید و کلیپ‌ها و کاورها را اضافه کنید.
خروجی نهایی و فایل تکست را دریافت کنید.

هشدار:
برای اجرای صحیح این نرم‌افزار، نیاز است که FFmpeg بر روی سیستم شما نصب باشد. FFmpeg یک ابزار قدرتمند برای پردازش فایل‌های ویدیویی و صوتی است که نرم‌افزار SceneFuse برای پردازش و ادغام ویدیوها از آن استفاده می‌کند.

نصب FFmpeg:
برای ویندوز:
به وب‌سایت رسمی FFmpeg بروید: https://ffmpeg.org/download.html
نسخه Windows را انتخاب کرده و فایل زیپ را دانلود کنید.
پس از دانلود، فایل زیپ را استخراج کنید.
مسیر پوشه استخراج‌شده را به متغیر محیطی PATH سیستم خود اضافه کنید:
در نوار جستجوی ویندوز، عبارت "Environment Variables" را جستجو کنید.
بر روی "Edit the system environment variables" کلیک کنید.
در پنجره بازشده، روی "Environment Variables" کلیک کنید.
در بخش "System Variables"، گزینه Path را انتخاب کنید و روی "Edit" کلیک کنید.
مسیر پوشه FFmpeg (مثلاً C:\ffmpeg\bin) را به لیست متغیرهای سیستم اضافه کنید.
سیستم خود را ریستارت کنید.
برای لینوکس:
از دستور زیر برای نصب FFmpeg استفاده کنید:
bash
Data format:

Copy
Edit
sudo apt update
sudo apt install ffmpeg
برای اطمینان از نصب صحیح، دستور زیر را وارد کنید:
bash
Data format:

Copy
Edit
ffmpeg -version


نصب:
git clone https://github.com/rayared/SceneFuse.git
cd SceneFuse
pip install tkinter
python scene_fuse.py

English:
SceneFuse
SceneFuse is a software tool for automatically merging video clips and adding custom covers to videos, without losing audio or video quality. It is designed for use on video platforms like Aparat or YouTube. With this tool, you can easily merge clips and add custom covers before each clip.

Warning:
To run this software properly, FFmpeg must be installed on your system. FFmpeg is a powerful tool for processing video and audio files, and SceneFuse relies on it for video processing and merging.

FFmpeg Installation Guide:
For Windows:
Go to the official FFmpeg website: https://ffmpeg.org/download.html
Select the Windows version and download the zip file.
Extract the downloaded zip file.
Add the path of the extracted folder to the system's PATH environment variable:
Search for "Environment Variables" in the Windows search bar.
Click "Edit the system environment variables."
In the "System Properties" window, click "Environment Variables."
In the "System Variables" section, select Path and click "Edit."
Add the path of the FFmpeg folder (e.g., C:\ffmpeg\bin) to the list.
Restart your system.
For Linux:
Use the following commands to install FFmpeg:
bash
Data format:

Copy
Edit
sudo apt update
sudo apt install ffmpeg
To verify the installation, use:
bash
Data format:

Copy
Edit
ffmpeg -version
For macOS:
Use Homebrew to install FFmpeg:
bash
Data format:

Copy
Edit
brew install ffmpeg
Features:
Automatic Clip Merging: The software automatically merges different clips into one.
Add Covers: Ability to add covers with a custom duration before each clip.
Text Output: Generates a text file displaying the positions of the covers in the integrated video (for use on Aparat or YouTube).
No Quality Loss: All operations are performed without any loss of audio or video quality.
Written in Python: The software is developed using Python.
How to Use:
Clone the project.
Install all dependencies.
Run the program and add clips and covers.
Receive the final output and the text file.
Installation:
bash
Data format:

Copy
Edit
git clone https://github.com/username/SceneFuse.git
cd SceneFuse
pip install tkinter
python scene_fuse.py
