## Photo Cutter – Half‑frame splitter

This is a small Python script that takes scans from a half‑frame camera (like the Pentax 17) where each JPEG contains two frames side‑by‑side, and automatically splits them into two separate images.

### Requirements

- Python 3.9 or newer
- `Pillow` (installed via `pip`)
- `tkinterdnd2` (optional – enables drag-and-drop in the GUI)

### One‑time setup (Windows, very step‑by‑step)

1. **Install Python**
   - Open your browser and go to the official Python website: `https://www.python.org/downloads/windows/`.
   - Download the latest **Python 3 for Windows**.
   - Run the installer.
   - On the first screen, **check the box “Add Python to PATH”** at the bottom.
   - Click “Install Now” and let it finish.

2. **Open this project in VS Code**
   - In File Explorer, go to `D:\OneDrive\Documents\Coding\photo-cutter`.
   - Right‑click in some empty space and choose **Open with Code**  
     (or open VS Code, then **File → Open Folder…** and pick `photo-cutter`).

3. **Open a terminal in the right folder**
   - In VS Code’s top menu, click **Terminal → New Terminal**.
   - Look at the prompt. If it already shows something like:
     - `PS D:\OneDrive\Documents\Coding\photo-cutter>`
       then you are in the right place.
   - If it shows a different path, type this and press Enter:

     ```powershell
     cd "D:\OneDrive\Documents\Coding\photo-cutter"
     ```

4. **Install the required Python packages**  
   (if `python` doesn’t work, use `py` instead, e.g. `py -m pip ...`)
   - In that same VS Code terminal, run:

     ```powershell
     pip install -r requirements.txt
     ```

   - This downloads and installs `Pillow`. You only need to do this once (or when you change `requirements.txt`).

### Basic usage – split a roll (Windows, command line)

1. Put all your scanned images (each with two frames per JPEG) in a folder, e.g. `D:\photos\roll1`.
2. Make sure your VS Code terminal is still in the `photo-cutter` folder (see step 3 above).
3. Run (pick the version that works on your machine):

   ```powershell
   python split_half_frame.py "D:\photos\roll1"
   # or, if you normally use `py`:
   py split_half_frame.py "D:\photos\roll1"
   ```

By default this will:

- Look for common image types (`.jpg`, `.jpeg`, `.png`, `.tif`, `.tiff`) in the input folder.
- Assume each file is a landscape image with two portrait frames side‑by‑side.
- Split each file exactly down the middle.
- Save the results to a new folder `D:\photos\roll1\split` as `<originalname>_a.jpg` and `<originalname>_b.jpg`.

### Smarter split for Pentax 17 scans (command line)

If your lab scans show a **dark black strip between the two frames** (typical for Pentax 17 half‑frame scans), use the automatic gap detection:

```powershell
python split_half_frame.py "D:\photos\roll1" --auto-gap --crop-border 25
# or, if you normally use `py`:
py split_half_frame.py "D:\photos\roll1" --auto-gap --crop-border 25
```

This:

- Converts the scan to grayscale.
- Looks in the middle of the image for the **darkest vertical band** (the film gap).
- Uses that as the cut between the two frames instead of “exactly half”.

You can tweak `--crop-border` up or down (e.g. 20, 30, 40) until the outer black edges disappear without cutting too much of the frame.

### Other useful options (Windows)

- **Custom output folder**

  ```powershell
  python split_half_frame.py "D:\photos\roll1" -o "D:\photos\roll1\final"
  ```

- **Crop borders only**

  ```powershell
  python split_half_frame.py "D:\photos\roll1" --crop-border 20
  ```

- **Allow overwriting existing output files**

  ```powershell
  python split_half_frame.py "D:\photos\roll1" --auto-gap --crop-border 25 --overwrite
  ```

If you ever get an error like “`python` is not recognized…”, close VS Code completely, reopen it, open the `photo-cutter` folder again, and open a fresh terminal. That reloads the PATH changes from installing Python. On some Windows setups you may need to use `py` instead of `python`.

### Desktop app (Windows GUI)

If you prefer a small window you can click on instead of the command line, you can run the GUI app.

#### Run the GUI from source

1. Follow the **One‑time setup (Windows)** steps above (Python + `pip install -r requirements.txt`).
2. In VS Code’s terminal, make sure you are in the project folder:

   ```powershell
   cd "D:\OneDrive\Documents\Coding\photo-cutter"
   ```

3. Start the app:

   ```powershell
   python app_gui.py
   # or, if you normally use `py`:
   py app_gui.py
   ```

4. In the window that opens:
   - Click **“Browse…”** next to **“Input folder with scans”** and pick a folder with your lab scans.
   - Optionally set an **Output folder** (otherwise it will create `<input>\split`).
   - Or **drag a folder** directly onto the window to set the input path (requires `tkinterdnd2`).
   - Leave **”Use auto gap (recommended)”** checked.
   - Adjust **”Border crop (pixels)”** if you want to trim more/less border (25 is a good default).
   - Click **Run** and watch the **progress bar** advance (“3 of 18”, etc.). Each filename also appears in the **Log** box.

#### Download a pre‑built executable

Pre‑built executables for **Windows** and **macOS** are available on the [Releases page](https://github.com/JCodes768/photo-cutter/releases). Just download the one for your OS and run it — no Python install needed.

> **macOS note:** The macOS build is unsigned. The first time you open it, macOS Gatekeeper will block it. Right‑click the file → **Open** to bypass the warning.

#### Build a standalone `.exe` locally with PyInstaller

If you want to build it yourself:

1. Make sure PyInstaller is installed (it is already listed in `requirements.txt`, but you can also run):

   ```powershell
   py -m pip install pyinstaller
   ```

2. From the project folder, run:

   ```powershell
   py -m PyInstaller PhotoCutter.spec
   ```

3. When it finishes, you will get `dist/PhotoCutter.exe`. You can:
   - Double‑click `PhotoCutter.exe` to run the app.
   - Right‑click it → **Send to → Desktop (create shortcut)** to make an icon you can click.
   - Right‑click the running app’s icon and choose **Pin to taskbar** if you want it there.

### macOS quick start (command line)

1. **Install Python 3** (if you don’t already have it)
   - Easiest is via Homebrew:

     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     brew install python
     ```

   - Or download an installer from the official site: `https://www.python.org/downloads/macos/`.

2. **Download or clone this project**
   - Put it somewhere like `~/code/photo-cutter`.

3. **Open the folder in VS Code (or Terminal)**
   - In VS Code: **File → Open Folder…** and pick `photo-cutter`.
   - Then **Terminal → New Terminal**, and run:

     ```bash
     cd ~/code/photo-cutter
     ```

4. **Install dependencies**

   ```bash
   python3 -m pip install -r requirements.txt
   ```

5. **Run the splitter on a roll**
   - Suppose your scans live in `/Users/you/Pictures/roll1`:

   ```bash
   python3 split_half_frame.py "/Users/you/Pictures/roll1" --auto-gap --crop-border 25
   ```

   - Output will go to `/Users/you/Pictures/roll1/split` with `_a` and `_b` images.