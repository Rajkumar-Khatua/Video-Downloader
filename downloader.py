import streamlit as st
import yt_dlp
import os
import tempfile
import glob
import matplotlib.pyplot as plt
import datetime

# ----------------- Helper Functions -----------------
def format_filesize(size):
    if size and isinstance(size, int):
        if size > 1024 * 1024:
            return f"{size/1024/1024:.1f} MB"
        else:
            return f"{size/1024:.0f} KB"
    elif isinstance(size, str):
        return size
    return "Unknown size"

def format_duration(seconds):
    if not seconds:
        return "Unknown"
    m, s = divmod(int(seconds), 60)
    return f"{m} min {s} sec" if m else f"{s} sec"

def format_views(val):
    try:
        return f"{int(val):,}"
    except Exception:
        return "Unknown"

def format_upload_date(raw_date):
    try:
        if not raw_date or len(str(raw_date)) != 8:
            return "Unknown"
        y = str(raw_date)[:4]
        m = str(raw_date)[4:6]
        d = str(raw_date)[6:8]
        import calendar
        month_abbr = calendar.month_abbr[int(m)]
        return f"{int(d)} {month_abbr} {y}"
    except Exception:
        return str(raw_date)

def file_pretty_date(file_path):
    ts = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(ts).strftime("%d %b %Y, %I:%M %p")

# ----------------- Setup Temp Directory -----------------
DOWNLOAD_DIR = os.path.join(tempfile.gettempdir(), "video_downloader_files")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ----------------- Streamlit Page Config -----------------
st.set_page_config(page_title="📥 Video/Audio Downloader", layout="centered")

# ----------------- App Header -----------------
st.markdown("""
<div style="text-align:center; max-width:700px; margin:auto;">
    <h1 style="color:#2389fe; font-size:2.4em; font-weight:900; margin-bottom:0.1em; letter-spacing:-1px;">
        Video/Audio Downloader & Preview
    </h1>
    <div style="color:#aaa; font-size:1.08em; margin-bottom:1.1em; font-weight:400;">
        Paste any YouTube, Facebook, or public video link.<br>
        Instantly preview, then download <b>video with audio</b> or <b>audio only</b>—all in one place.<br>
        <span style="color:#e57373; font-weight:bold;">
            No more silent videos. Always get the format you want—even for HD!
        </span>
    </div>
</div>
""", unsafe_allow_html=True)
import subprocess
import streamlit as st

def check_ffmpeg():
    try:
        result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            st.sidebar.success("✅ ffmpeg is installed!")
            st.sidebar.code(result.stdout.split('\n')[0])  # Shows the version
        else:
            st.sidebar.error("❌ ffmpeg is NOT installed.")
    except Exception as e:
        st.sidebar.error(f"❌ Error checking ffmpeg: {e}")

check_ffmpeg()

# Main Input
st.markdown("### 🔗 Paste your video/audio link below:")
col1, col2 = st.columns([4,1])
with col1:
    url = st.text_input("", placeholder="https://...", key="video_url")
with col2:
    fetch_btn = st.button("🔄 Fetch Info")

# Run preview code only if link changes or button pressed
if url and (fetch_btn or "last_url" not in st.session_state or st.session_state.last_url != url):
    st.session_state.last_url = url
# ----------------- Preview Section -----------------
if url:
    with st.spinner("Fetching video info..."):
        try:
            ydl = yt_dlp.YoutubeDL({'quiet': True})
            info = ydl.extract_info(url, download=False)
            st.markdown(f"<h4 style='margin-bottom:0.4em'>{info.get('title', 'No title')}</h4>", unsafe_allow_html=True)
            if info.get('uploader'):
                st.caption(f"Video by {info['uploader']}")
            if info.get('thumbnail'):
                st.image(info['thumbnail'], caption="Thumbnail", width=240)
            meta1 = f"**Channel:** {info.get('uploader', 'Unknown')}"
            meta2 = f"**Duration:** {format_duration(info.get('duration', 0))}"
            meta3 = f"**Views:** {format_views(info.get('view_count', 'Unknown'))}"
            meta4 = f"**Upload Date:** {format_upload_date(info.get('upload_date', 'Unknown'))}"
            st.markdown(f"{meta1}<br>{meta2}<br>{meta3}<br>{meta4}", unsafe_allow_html=True)
            # Only show video preview for public platforms
            if (
                "youtube.com" in url
                or "youtu.be" in url
                or "vimeo.com" in url
                or url.endswith(('.mp4', '.webm', '.ogg'))
            ):
                st.video(info.get('webpage_url', url))
            else:
                st.info("🔒 Video preview is not available for this platform. (But download will work!)")
        except Exception as e:
            st.error(f"Could not fetch preview: {e}")

# ----------------- Download Buttons -----------------
col_download_vid, col_download_aud = st.columns(2)
with col_download_vid:
    vid_btn = st.button("🎵 Download Video with Audio (Recommended)", key="video")
with col_download_aud:
    aud_btn = st.button("🎧 Download Audio Only", key="audio")

if vid_btn or aud_btn:
    try:
        if not url:
            st.warning("Please enter a valid video/audio link.")
            st.stop()
        # Set download options per button
        if vid_btn:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                'outtmpl': os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
                'quiet': True,
                'merge_output_format': 'mp4'
            }
            nice_label = "video with audio"
        else:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
                'quiet': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }
            nice_label = "audio only"

        progress_bar = st.progress(0, text="Starting download...")
        status_text = st.empty()

        def progress_hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                percent = int((downloaded / total * 100) if total else 0)
                progress_bar.progress(percent/100, text=f"Downloading... {percent}%")
                status_text.info(f"{format_filesize(downloaded)} / {format_filesize(total)}")
            elif d['status'] == 'finished':
                progress_bar.progress(1.0, text="Finishing up...")

        ydl_opts['progress_hooks'] = [progress_hook]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if vid_btn:
                file_name = ydl.prepare_filename(info)
            else:
                file_name = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp3"

        progress_bar.progress(1.0, text="Ready!")
        status_text.success("Ready to download!")
        with open(file_name, "rb") as f:
            st.download_button("⬇️ Get the file!", f, os.path.basename(file_name), use_container_width=True)
    except Exception as e:
        st.error(f"Download failed: {e}")

# ----------------- Sidebar: Donut, Delete All, Categorized Files -----------------
with st.sidebar:
    # ---- Donut + Target Selector ----
    unit = st.radio("Show downloaded size in:", options=["MB", "GB"], horizontal=True)
    if unit == "MB":
        target_val = 2048
        min_target = 100
        max_target = 50000
        step_target = 100
        target = st.number_input(
            f"Set download target ({unit}):",
            min_value=min_target,
            max_value=max_target,
            value=target_val,
            step=step_target,
            help=f"Set your quota/goal in {unit} for the donut ring."
        )
    else:  # GB
        target_val = 2.0
        min_target = 0.1
        max_target = 50.0
        step_target = 0.1
        target = st.number_input(
            f"Set download target ({unit}):",
            min_value=min_target,
            max_value=max_target,
            value=target_val,
            step=step_target,
            format="%.1f",
            help=f"Set your quota/goal in {unit} for the donut ring."
        )

    files = glob.glob(os.path.join(DOWNLOAD_DIR, '*'))
    total_bytes = sum(os.path.getsize(f) for f in files)

    # Convert size
    if unit == "MB":
        total = total_bytes / (1024*1024)
    else:
        total = total_bytes / (1024*1024*1024)

    percent = min(total/target, 1.0) if target else 0
    display_amount = f"{total:.2f} {unit}"
    display_percent = f"{(percent*100):.0f}%"
    center_text = f"{display_amount}\n({display_percent})"

    # Donut Chart
    fig, ax = plt.subplots(figsize=(1.0,1.0), subplot_kw={'aspect': 'equal'}, facecolor='none')
    used = min(total, target)
    sizes = [used, max(target - used, 0.01)]
    colors = ['#2389fe', '#e0e0e0']
    wedges, _ = ax.pie(
        sizes, colors=colors, startangle=90,
        wedgeprops=dict(width=0.16, edgecolor='none')
    )
    ax.text(0,0, center_text, ha='center', va='center', fontsize=7, fontweight='bold', color='#2389fe')
    plt.tight_layout()
    ax.axis('off')
    st.markdown("#### 📦 Total Downloaded")
    st.pyplot(fig)

    # ---- Delete All Downloads Button ----
    if files:
        if st.button("🧹 Delete All Downloads"):
            for f in files:
                try:
                    os.remove(f)
                except Exception as e:
                    st.error(f"Could not delete: {os.path.basename(f)} ({e})")
            st.success("All downloads deleted!")
            st.rerun()

    # ---- Categorized File Listing ----
    video_exts = ('.mp4', '.webm', '.mkv', '.mov')
    audio_exts = ('.mp3', '.m4a', '.aac', '.wav', '.ogg')

    video_files, audio_files = [], []
    for file_path in files:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in video_exts:
            video_files.append(file_path)
        elif ext in audio_exts:
            audio_files.append(file_path)

    def file_card(file_path, filetype):
        file_name = os.path.basename(file_path)
        ext = os.path.splitext(file_name)[1].lower()
        size_str = format_filesize(os.path.getsize(file_path))
        date_str = file_pretty_date(file_path)
        st.markdown(
            f"""
            <div style="padding: 0.2em 0.7em 0.3em 0.7em; margin-bottom:0.15em; border-radius: 8px; background:rgba(230,240,250,0.16); border:1px solid #e5e7eb;">
                <span style="font-weight:bold;font-size:1em;">{file_name}</span><br>
                <span style="color:#aaa; font-size:0.92em;">{size_str} &nbsp; | &nbsp; <span style="color:#53b0f7;">{date_str}</span></span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Preview
        if filetype == "video":
            with st.expander("▶️ Preview Video", expanded=False):
                st.video(file_path)
        else:
            with st.expander("🎧 Preview Audio", expanded=False):
                st.audio(file_path)
        # Download and Delete
        with open(file_path, "rb") as f:
            st.download_button(
                "⬇️ Get the file",
                f,
                file_name,
                key=f"download_{file_name}_{filetype}",
                use_container_width=True,
            )
        if st.button("🗑️ Delete", key=f"delete_{file_name}_{filetype}"):
            try:
                os.remove(file_path)
                st.success(f"Deleted {file_name}")
                st.rerun()
            except Exception as e:
                st.error(f"Could not delete: {e}")
        st.markdown("---", unsafe_allow_html=True)

    # Videos
    if video_files:
        st.markdown(
            f"<h5 style='color:#2389fe; margin-bottom:0.6em'>🎬 Videos ({len(video_files)})</h5>",
            unsafe_allow_html=True,
        )
        for fp in sorted(video_files, key=os.path.getmtime, reverse=True):
            file_card(fp, "video")

    # Audios
    if audio_files:
        st.markdown(
            f"<h5 style='color:#15c298; margin-bottom:0.6em'>🎧 Audio ({len(audio_files)})</h5>",
            unsafe_allow_html=True,
        )
        for fp in sorted(audio_files, key=os.path.getmtime, reverse=True):
            file_card(fp, "audio")

    if not video_files and not audio_files:
        st.info("No files yet. Download something first!")
