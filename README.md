## Photo Cutter – Half‑frame splitter

A small app that takes scans from a half‑frame camera (like the Pentax 17) where each JPEG contains two frames side‑by‑side, and automatically splits them into two separate images.

### Quickest way to get started

**You don't need Python or any coding setup.** Just download the ready‑to‑run app for your OS:

1. Go to the [Releases page](https://github.com/JCodes768/photo-cutter/releases) (look for **Releases** in the right sidebar on the repo page).
2. Download **PhotoCutter.exe** (Windows) or **PhotoCutter** (macOS).
3. Run it. That's it.

> **Windows note:** You may see a SmartScreen warning the first time — click **More info → Run anyway**.
>
> **macOS note:** The macOS build is unsigned. Gatekeeper will block it the first time. Right‑click the file → **Open** to bypass the warning.

In the app window:

- Click **Browse** or **drag a folder** onto the window to select your scans folder.
- Leave **"Use auto gap (recommended)"** checked — this detects the dark film strip between frames.
- Adjust **"Border crop (pixels)"** to trim black edges (25 is a good default).
- Click **Run** and watch the progress bar ("3 of 18", etc.).
- Output goes to a `split` subfolder inside your input folder.

---

### Running from source (if you prefer Python)

Everything below is only needed if you want to run the Python scripts directly instead of using the executable.

#### Requirements

- Python 3.9 or newer
- `Pillow` (installed via `pip`)
- `tkinterdnd2` (optional — enables drag‑and‑drop in the GUI)

#### One‑time setup (Windows, very step‑by‑step)

1. **Install Python**
   - Go to `https://www.python.org/downloads/windows/`.
   - Download the latest **Python 3 for Windows**.
   - Run the installer. **Check the box "Add Python to PATH"** at the bottom.
   - Click "Install Now" and let it finish.

2. **Open this project in VS Code**
   - In File Explorer, navigate to the `photo-cutter` folder.
   - Right‑click in some empty space and choose **Open with Code**
     (or open VS Code, then **File → Open Folder…** and pick `photo-cutter`).

3. **Open a terminal**
   - In VS Code's top menu, click **Terminal → New Terminal**.

4. **Install dependencies**
   (if `python` doesn't work, use `py` instead, e.g. `py -m pip ...`)

   ```powershell
   pip install -r requirements.txt
   ```

#### Run the GUI from source

```powershell
python app_gui.py
# or: py app_gui.py
```

#### Command line usage

**Basic split** (cuts each scan exactly in half):

```powershell
python split_half_frame.py "D:\photos\roll1"
```

**Auto‑gap detection** (finds the dark film strip and cuts there — recommended):

```powershell
python split_half_frame.py "D:\photos\roll1" --auto-gap --crop-border 25
```

**Other options:**

```powershell
# Custom output folder
python split_half_frame.py "D:\photos\roll1" -o "D:\photos\roll1\final"

# Overwrite existing output files
python split_half_frame.py "D:\photos\roll1" --auto-gap --crop-border 25 --overwrite
```

If you get "`python` is not recognized", try `py` instead, or close and reopen VS Code to reload PATH.

#### macOS quick start (command line)

1. Install Python 3 via Homebrew (`brew install python`) or from `https://www.python.org/downloads/macos/`.
2. Clone or download this project.
3. Install dependencies:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

4. Run:

   ```bash
   python3 split_half_frame.py "/Users/you/Pictures/roll1" --auto-gap --crop-border 25
   ```

---

### Building the executable yourself

If you want to build the `.exe` / macOS binary locally:

```powershell
py -m pip install pyinstaller
py -m PyInstaller PhotoCutter.spec
```

The output lands in `dist/PhotoCutter.exe` (or `dist/PhotoCutter` on macOS).
