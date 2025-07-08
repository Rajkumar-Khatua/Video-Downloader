# 📥 Streamlit Video/Audio Downloader

A modern Streamlit app for downloading and previewing videos and audio from YouTube, Facebook, Instagram, and more.
Easily select video/audio quality, preview before downloading, and manage your files — all in one place.

---

![screenshot](/image.png) <!-- Replace with your screenshot path or remove if not available -->

## 🚀 Features

- Paste any public video or audio URL (YouTube, Facebook, Instagram, etc.)
- Instant preview: Title, channel, duration, views, and thumbnail
- Download **video with audio** (no more silent videos!) or **audio only**
- Choose quality and format (MP4, MP3, etc.)
- Download progress bar & command logs
- Responsive, mobile-friendly UI
- Sidebar dashboard: See and manage downloaded files, with a total size donut ring and categorized file lists
- Preview and download or delete any file instantly
- Delete all downloads with one click

---

## 🛠️ Setup

### Requirements

- Python 3.8 or higher
- [ffmpeg](https://ffmpeg.org/download.html) (add to your PATH)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- streamlit
- matplotlib

### Install dependencies

```bash
pip install streamlit yt-dlp matplotlib
```

### Run the app

```bash
streamlit run downloader.py
```

### Access the app
Open your browser and go to [http://localhost:8501](http://localhost:8501)

## 📂 File Management
- Downloads are stored in a temporary folder on your PC (see DOWNLOAD_DIR in code).
- You can preview, download, and delete files directly from the app.
- Preview, download, or delete individual files right from the sidebar.
- Supports both video (MP4, WEBM, etc.) and audio (MP3, M4A, etc.).
- Delete all downloads with one click from the sidebar.

### Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.
- If you’d like to improve this app, add features, or fix bugs:
1. Fork the repository
2. Create a new branch
```bash
git checkout -b feature/my-feature
```
3. Make your changes
4. Commit your changes
```bash
git commit -m "Add my feature"
```
5. Push to the branch
```bash
git push origin feature/my-feature
```
6. Open a pull request and describe your changes
Suggestions and feedback:
- If you have ideas for improvements or new features, please open an issue or submit a pull request.

### Credits
- This app uses [yt-dlp](https://streamlit.io/) for downloading videos and audio.
- Thanks to [Streamlit](https://streamlit.io/) for making it easy to build interactive web apps in Python.
- Inspired by open-source video tools and the awesome developer community
- Special thanks to contributors who help improve this project!

### Desclaimer
- This app is for educational purposes only. Please respect copyright and terms of service of the platforms
you use.
- Ensure you have permission to download and use any content.
- The app does not store any user data or downloaded files permanently.
- The author is not responsible for misuse or downloading copyrighted content.
- Use at your own risk. The app is provided "as is" without warranties of any kind.
- By using this app, you agree to the terms above.

### Happy downloading and hacking! 🚀
- LinkedIn: [Rajkumar Khatua](https://www.linkedin.com/in/rajkumarkhatua/)

### Thanks for using this app! If you find it useful, please give it a star on GitHub ⭐
- [GitHub Repository](https://github.com/Rajkumar-Khatua/Video-Downloader)
