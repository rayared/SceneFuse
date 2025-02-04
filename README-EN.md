
# SceneFuse

SceneFuse is software for automatically connecting clips together and adding custom covers to videos without losing audio or video quality. This tool is designed for use on video platforms like Aparat or YouTube. With this software, you can easily connect clips and insert custom covers before each clip.



## 🚀 Why I Built This Software
The goal of creating this software was to produce a suitable output for YouTube. I am an instructor, and each of my lessons is between 7 to 15 minutes long, and uploading each one as a separate file in a playlist is really hard. With this tool, I can easily merge everything and publish it as one video. It might come in handy for you as well.


## Features

- Automatic Clip Connection: The software automatically connects different clips together.
- Adding Covers: You can add covers with a custom duration before each clip.
- Text Output: Creates a text file that shows the position of the covers within the video (for use in Aparat and YouTube).
- No Quality Loss: All operations are done without any quality loss in audio or video.
- Written in Python: The software is developed using Python.








## How to Use

### Warning
To run this software correctly, FFmpeg must be installed on your system. FFmpeg is a powerful tool for processing video and audio files, which SceneFuse uses for processing and merging videos.


#### Installing FFmpeg: For Windows:


- Visit the official FFmpeg website: https://ffmpeg.org/download.html
- Select the Windows version and download the zip file.
- After downloading, extract the zip file.
- Add the path of the extracted folder to your system's PATH environment variable:
- In the Windows search bar, search for "Environment Variables."
- Click on "Edit the system environment variables."
- In the window that opens, click on "Environment Variables."
- Under "System Variables," select Path and click "Edit."
- Add the FFmpeg folder path (e.g., C:\ffmpeg\bin) to the list of system variables.
- Restart your system.


#### Installing FFmpeg: For Linux:

Use the following command to install FFmpeg:

```bash
sudo apt update
sudo apt install ffmpeg
ffmpeg -version
```

#### Installing FFmpeg: For Mac:

Use the following command to install FFmpeg:

```bash
brew install ffmpeg

```
### Installing the Software

To install the software, follow these steps:

```python
git clone https://github.com/rayared/SceneFuse.git
cd SceneFuse
pip install -r tkinter
python scene_fuse.py

```

### Usage Guide


After running the code, a graphical interface will open where you can provide the folder containing the videos to automatically add them to the software. Then, to add cover images that will be displayed before each video, you can use the bulk add button or double-click on each video.

- Videos can have no covers.
- Enter the cover display time, which is set to 3 seconds by default (recommended), and click on "Create Output."
- Specify the output path and write the name of the final video.
- Wait for the output to be prepared.
- To estimate the output time, consider the total duration of the videos plus an additional 10%.
- After the output is created, a text file indicating the position of the images in the main video will also be placed next to the video.


```bash
Start times of videos with 3 seconds added:
Video 1: 00:00
Video 2: 01:25
Video 3: 09:46
Video 4: 18:06

```
You can use this content to create a table of contents on YouTube.



## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

