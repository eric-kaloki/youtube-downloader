import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import logging
from yt_dlp import YoutubeDL

# Configure logging
#logging.basicConfig(filename='download.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to download video or audio
def download():
    url = url_entry.get()
    if not url:
        messagebox.showerror('Error', 'Please enter a URL')
        return
    try:
        if download_type.get() == 'audio':
            options = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(os.path.expanduser('~/Music'), '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }],
                'progress_hooks': [progress_hook],
                'keepvideo': True,
            }
        elif download_type.get() == 'both':
            options = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': os.path.join(os.path.expanduser('~/Videos'), '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',  # Ensure merging happens in MP4 format
                'postprocessors': [{
                    'key': 'FFmpegMerger'
                }],
                'progress_hooks': [progress_hook],
                'keepvideo': True,
            }
        else:
            options = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': os.path.join(os.path.expanduser('~/Videos'), '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegMerger',
                }],
                'progress_hooks': [progress_hook],
                'keepvideo': True,
            }
        with YoutubeDL(options) as ydl:
            #logging.info(f'Starting download for URL: {url}')
            ydl.download([url])
            # logging.info('Download completed!')
            messagebox.showinfo('Success', 'Download completed!')
            url_entry.delete(0, tk.END)  # Clear the URL entry
            print("Download Complete")
            
    except Exception as e:
        #logging.error(f'Error occurred: {str(e)}')
        messagebox.showerror('Error', str(e))

# Progress hook function
def progress_hook(d):
    # logging.debug(f'Progress data: {d}')
    if d['status'] == 'downloading':
        if 'downloaded_bytes' in d and 'total_bytes' in d:
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100
            progress_bar['value'] = percent
            root.update_idletasks()
    elif d['status'] == 'finished':
        progress_bar['value'] = 100
        root.update_idletasks()
        
        
        

# GUI setup
root = tk.Tk()
root.title('YouTube Downloader')

url_label = tk.Label(root, text='Enter YouTube URL:')
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

download_type = tk.StringVar(value='audio')

audio_radio = tk.Radiobutton(root, text='Download Audio', variable=download_type, value='audio')
audio_radio.pack()

both_radio = tk.Radiobutton(root, text='Download Video', variable=download_type, value='both')
both_radio.pack()

progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress_bar.pack(pady=10)

download_button = tk.Button(root, text='Download', command=download)
download_button.pack()

root.mainloop()
