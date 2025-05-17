# Flipper Zero Asset Pack Generator

This project provides a Python-based tool for creating and packing animation asset packs for the **Flipper Zero** device. It consists of two main scripts:

- **AssetGenerator.py**: A Tkinter-based GUI for selecting PNG frames or ZIP files, configuring animation parameters, and generating asset packs.
- **asset_packer.py**: A script for processing and packing animations, icons, and fonts into a Flipper Zero-compatible format, including PNG-to-BM conversion and Heatshrink compression.

---

## Features

- User-friendly GUI for input selection (directory or ZIP) and parameter configuration.
- Supports renaming and organizing PNG frames for animations.
- Generates `meta.txt` and `manifest.txt` files with customizable parameters (e.g., frame rate, resolution, butthurt, level, weight).
- Converts PNG frames to BM format and applies Heatshrink compression.
- Packs animations, static/animated icons, and fonts into a structured asset pack.
- Saves output to a user-specified directory.

---

## Prerequisites

To run this project, you need:

- Python 3.8+ installed on your system.
- The following Python packages:
  - `tkinter` (usually included with Python; install `python3-tk` on Linux if missing)
  - `Pillow` (for image processing)
  - `heatshrink2` (for compression)

A set of PNG files named in the format `frame_X_delay-*.png` (for animations) or a ZIP file containing such files.

---

## Installation

### Clone the Repository:
```bash
git clone https://github.com/yourusername/flipper-asset-pack-generator.git
cd flipper-asset-pack-generator
````

### Install Dependencies:

Install the required Python packages using pip:

```bash
pip install Pillow heatshrink2
```

### Verify Tkinter:

Ensure Tkinter is available. On Linux, you may need:

```bash
sudo apt-get install python3-tk
```

---

## Usage

### Run the GUI:

Start the asset generator by running:

```bash
python AssetGenerator.py
```

* Select a directory containing PNG frames or a ZIP file with frames.
* Enter animation parameters (e.g., pack name, animation name, frame rate, resolution).
* Click **"Generate"** to process the frames and create an asset pack.
* Choose a directory to save the final `asset_packs` folder.

### Run the Packer Script (Optional):

To manually pack assets in a directory, run:

```bash
python asset_packer.py
```

* The script scans subfolders for assets (animations, icons, fonts) and packs them into an `asset_packs` folder.
* Press Enter to start and exit the script.

---

## File Structure

### Input:

* PNG files should follow the naming convention `frame_X_delay-*.png` (e.g., `frame_0_delay-0.1s.png`).
* ZIP files should contain these PNGs in the root or a subdirectory.
* Optional: Folders for icons (`Icons/`) or fonts (`Fonts/`) in the input directory.

### Output:

The generated `asset_packs` folder has the following structure:

```
asset_packs/
└── <PackName>/
    ├── Anims/
    │   ├── manifest.txt
    │   └── <AnimationName>/
    │       ├── meta.txt
    │       ├── frame_0.png
    │       └── ...
    ├── Icons/ (optional)
    └── Fonts/ (optional)
```

---

## Parameters

When using the GUI, you can configure:

* **Pack Name**: Name of the asset pack (e.g., `MyPack`)
* **Animation Name**: Name of the animation (e.g., `MyAnim`)
* **Min/Max Butthurt**: Range for Flipper Zero's "butthurt" metric (0–18)
* **Min/Max Level**: Level range for the animation (1–30)
* **Weight**: Animation weight (e.g., `3`)
* **Width/Height**: Frame resolution (e.g., `128x64`)
* **Frame Rate**: Frames per second (e.g., `8`)
* **Duration**: Total animation duration in frames (e.g., `3600`)

---

## Notes

* Ensure PNG files are properly formatted and named to avoid processing errors.
* The `asset_packer.py` script supports additional asset types (icons, fonts), but the GUI focuses on animations.
* Temporary files from ZIP extraction are automatically cleaned up.
* If the output directory already contains an `asset_packs` folder, it will be overwritten.

---

## Troubleshooting

* **"No PNG files to rename"**: Ensure the input directory or ZIP contains PNGs with the correct naming convention.
* **"All parameters must be numbers"**: Verify that numeric fields (e.g., frame rate, width) contain valid integers.
* **Tkinter not found**: Install `python3-tk` (Linux) or ensure Python includes Tkinter.
* **Heatshrink2 errors**: Confirm the `heatshrink2` package is installed (`pip install heatshrink2`).

---

## Contributing

Feel free to submit issues or pull requests for bug fixes, new features, or improvements. Ensure any changes are tested and compatible with Python 3.8+.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

```

Let me know if you'd like this saved as a `.md` file or converted into another format (like PDF or HTML).
```
