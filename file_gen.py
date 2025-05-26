import os

# Define where to create the test folder
test_dir = r"C:\\Users\\LENOVO\\Desktop\\py_test"
os.makedirs(test_dir, exist_ok=True)

# Expanded categories with various file types
sample_files = [
    # Documents
    "report.docx", "whitepaper.pdf", "notes.txt", "contract.doc",
    "table.xlsx", "schedule.xls", "presentation.pptx", "slides.ppt",
    
    # Images          
    "photo.jpg", "diagram.jpeg", "icon.png", "banner.gif", "scan.bmp", "vector.svg", "image.webp",
    
    # Videos
    "movie.mp4", "clip.mov", "recording.avi", "show.mkv", "stream.flv", "reel.wmv",
    
    # Audio
    "song.mp3", "recording.wav", "tune.aac", "sound.ogg", "voice.m4a", "track.flac",
    
    # Archives
    "backup.zip", "project.rar", "data.7z", "installer.tar.gz",
    
    # Code files
    "script.py", "program.c", "app.java", "web.html", "style.css", "main.js", "config.json", "data.xml",
    
    # Executables / Binaries
    "setup.exe", "launcher.bat", "run.sh", "binary.bin", "machine.iso", "module.dll",
    
    # Fonts
    "font.ttf", "heading.otf", "webfont.woff", "webfont2.woff2",
    
    # Others
    "unknown.xyz", "misc.tmp", "readme.md", "license.rtf", "dataset.csv"
]

# Create each file with dummy content
for file_name in sample_files:
    file_path = os.path.join(test_dir, file_name)
    with open(file_path, "w") as f:
        f.write(f"This is a test file named: {file_name}")

print(f" Test files created in:\n{test_dir}")
