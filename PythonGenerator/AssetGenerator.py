import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
import shutil
import tempfile
import asset_packer

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Asset Pack Generator")
        self.selected_path = tk.StringVar()
        self.temp_dir = None
        self.pack_name = tk.StringVar()
        self.animation_name = tk.StringVar()
        self.min_butthurt = tk.StringVar(value="0")
        self.max_butthurt = tk.StringVar(value="18")
        self.min_level = tk.StringVar(value="1")
        self.max_level = tk.StringVar(value="30")
        self.weight = tk.StringVar(value="3")
        self.width = tk.StringVar(value="128")
        self.height = tk.StringVar(value="64")
        self.frame_rate = tk.StringVar(value="8")
        self.duration = tk.StringVar(value="3600")
        tk.Label(root, text="Select input:").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(root, text="Select directory", command=self.select_directory).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="Select zip file", command=self.select_zip).grid(row=0, column=2, padx=5, pady=5)
        tk.Label(root, textvariable=self.selected_path).grid(row=0, column=3, padx=5, pady=5, columnspan=2)
        params = [
            ("Pack name:", self.pack_name, 1),
            ("Animation name:", self.animation_name, 2),
            ("Min butthurt:", self.min_butthurt, 3),
            ("Max butthurt:", self.max_butthurt, 4),
            ("Min level:", self.min_level, 5),
            ("Max level:", self.max_level, 6),
            ("Weight:", self.weight, 7),
            ("Width:", self.width, 8),
            ("Height:", self.height, 9),
            ("Frame rate:", self.frame_rate, 10),
            ("Duration:", self.duration, 11),
        ]
        for label_text, var, row in params:
            tk.Label(root, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky="e")
            tk.Entry(root, textvariable=var).grid(row=row, column=1, padx=5, pady=5, columnspan=2)
        tk.Button(root, text="Generate", command=self.generate).grid(row=12, column=1, padx=5, pady=10)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_path.set(directory)
            if self.temp_dir:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                self.temp_dir = None

    def select_zip(self):
        zip_file = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])
        if zip_file:
            if self.temp_dir:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.temp_dir = tempfile.mkdtemp()
            shutil.unpack_archive(zip_file, self.temp_dir)
            self.selected_path.set(self.temp_dir)

    def generate(self):
        if not self.selected_path.get():
            messagebox.showerror("Error", "Please select a directory or zip file")
            return
        directory = self.selected_path.get()
        files = [f for f in os.listdir(directory) if re.match(r'^frame_\d+_delay-.*\.png$', f)]
        if not files:
            messagebox.showerror("Error", "No PNG files to rename in the selected directory")
            return
        files.sort()
        for i, file in enumerate(files):
            new_name = f"frame_{i}.png"
            os.rename(os.path.join(directory, file), os.path.join(directory, new_name))
        num_frames = len(files)
        try:
            pack_name = self.pack_name.get().strip()
            animation_name = self.animation_name.get().strip()
            if not pack_name or not animation_name:
                raise ValueError("Pack name and animation name must be entered")
            min_butthurt = int(self.min_butthurt.get())
            max_butthurt = int(self.max_butthurt.get())
            min_level = int(self.min_level.get())
            max_level = int(self.max_level.get())
            weight = int(self.weight.get())
            width = int(self.width.get())
            height = int(self.height.get())
            frame_rate = int(self.frame_rate.get())
            duration = int(self.duration.get())
        except ValueError as e:
            messagebox.showerror("Error", str(e) if str(e).startswith("Pack name") else "All parameters must be numbers except for names")
            return
        asset_packs_dir = os.path.join(directory, "AssetPacks")
        os.makedirs(asset_packs_dir, exist_ok=True)
        pack_dir = os.path.join(asset_packs_dir, pack_name)
        os.makedirs(pack_dir, exist_ok=True)
        anims_dir = os.path.join(pack_dir, "Anims")
        os.makedirs(anims_dir, exist_ok=True)
        animation_dir = os.path.join(anims_dir, animation_name)
        os.makedirs(animation_dir, exist_ok=True)
        for i in range(num_frames):
            shutil.move(os.path.join(directory, f"frame_{i}.png"), os.path.join(animation_dir, f"frame_{i}.png"))
        with open(os.path.join(animation_dir, "meta.txt"), "w") as f:
            f.write("Filetype: Flipper Animation\n")
            f.write("Version: 1\n\n")
            f.write(f"Width: {width}\n")
            f.write(f"Height: {height}\n")
            f.write(f"Passive frames: {num_frames}\n")
            f.write("Active frames: 0\n")
            f.write(f"Frames order: {' '.join(map(str, range(num_frames)))}\n")
            f.write("Active cycles: 0\n")
            f.write(f"Frame rate: {frame_rate}\n")
            f.write(f"Duration: {duration}\n")
            f.write("Active cooldown: 0\n\n")
            f.write("Bubble slots: 0\n")
        with open(os.path.join(anims_dir, "manifest.txt"), "w") as f:
            f.write("Filetype: Flipper Animation Manifest\n")
            f.write("Version: 1\n\n")
            f.write(f"Name: {animation_name}\n")
            f.write(f"Min butthurt: {min_butthurt}\n")
            f.write(f"Max butthurt: {max_butthurt}\n")
            f.write(f"Min level: {min_level}\n")
            f.write(f"Max level: {max_level}\n")
            f.write(f"Weight: {weight}\n")
        output_dir = os.path.join(directory, "asset_packs")
        asset_packer.pack(asset_packs_dir, output_dir, logger=print)
        save_dir = filedialog.askdirectory(title="Select directory to save asset_packs")
        if save_dir:
            dest_dir = os.path.join(save_dir, "asset_packs")
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir, ignore_errors=True)
            shutil.copytree(output_dir, dest_dir)
            messagebox.showinfo("Success", "Asset pack successfully saved")
        else:
            messagebox.showwarning("Warning", "Asset pack will be deleted")
            shutil.rmtree(output_dir, ignore_errors=True)
        if self.temp_dir:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.temp_dir = None
            self.selected_path.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
