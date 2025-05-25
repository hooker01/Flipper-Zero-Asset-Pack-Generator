import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.scrolled import ScrolledFrame
import os
import re
import shutil
import tempfile
import asset_packer
import tkinter.simpledialog as simpledialog

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Asset Pack Generator")
        self.style = ttkb.Style(theme="darkly")
        self.root.geometry("800x700")
        self.root.minsize(600, 650)
        self.selected_path = tk.StringVar()
        self.temp_dir = None
        self.pack_name = tk.StringVar()
        self.min_butthurt = tk.StringVar(value="0")
        self.max_butthurt = tk.StringVar(value="18")
        self.min_level = tk.StringVar(value="1")
        self.max_level = tk.StringVar(value="30")
        self.weight = tk.StringVar(value="3")
        self.width = tk.StringVar(value="128")
        self.height = tk.StringVar(value="64")
        self.frame_rate = tk.StringVar(value="8")
        self.duration = tk.StringVar(value="3600")
        self.status_var = tk.StringVar(value="No files selected")
        self.progress_var = tk.DoubleVar(value=0)
        self.create_gui()

    def create_gui(self):
        main_container = ttkb.Frame(self.root)
        main_container.pack(fill=BOTH, expand=True)
        scrolled_frame = ScrolledFrame(main_container, autohide=True, height=300)
        scrolled_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        main_frame = ttkb.Frame(scrolled_frame)
        main_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        header_frame = ttkb.Frame(main_frame)
        header_frame.pack(fill=X, pady=(0, 5))
        ttkb.Label(header_frame, text="Asset Pack Generator", font=("Helvetica", 20, "bold")).pack(side=LEFT)
        footer_frame = ttkb.Frame(main_container)
        footer_frame.pack(side=BOTTOM, fill=X, pady=5)
        credit_container = ttkb.Frame(footer_frame)
        credit_container.pack(expand=True, pady=2)
        ttkb.Label(credit_container, text="Created by ").pack(side=LEFT)
        hooker_link = ttkb.Label(
            credit_container, 
            text="hooker01", 
            foreground="#007BFF",  
            cursor="hand2",        
            font="-underline 1"    
        )
        hooker_link.pack(side=LEFT)
        hooker_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/hooker01"))
        theme_button = ttkb.Button(header_frame, text="Toggle Theme", style="outline.TButton", command=self.toggle_theme)
        theme_button.pack(side=RIGHT)
        ToolTip(theme_button, text="Switch between dark and light theme")
        input_frame = ttkb.LabelFrame(main_frame, text="Input Selection", padding=8)
        input_frame.pack(fill=X, pady=2)
        ttkb.Button(input_frame, text="📁 Select Directory", style="primary.TButton", command=self.select_directory).grid(row=0, column=0, padx=5, pady=2, sticky=W)
        ttkb.Button(input_frame, text="📦 Select ZIP Files", style="primary.TButton", command=self.select_zips).grid(row=0, column=1, padx=5, pady=2, sticky=W)
        ttkb.Label(input_frame, textvariable=self.selected_path, wraplength=350).grid(row=0, column=2, padx=5, pady=2, sticky=W)
        params_frame = ttkb.LabelFrame(main_frame, text="Animation Parameters", padding=8)
        params_frame.pack(fill=X, pady=2)
        params = [
            ("Pack Name:", self.pack_name, "Enter the name for your asset pack", 0),
            ("Min Butthurt:", self.min_butthurt, "Minimum butthurt value (0-18)", 1),
            ("Max Butthurt:", self.max_butthurt, "Maximum butthurt value (0-18)", 2),
            ("Min Level:", self.min_level, "Minimum level for animation (1-30)", 3),
            ("Max Level:", self.max_level, "Maximum level for animation (1-30)", 4),
            ("Weight:", self.weight, "Animation weight (1-100)", 5),
            ("Width:", self.width, "Frame width in pixels", 6),
            ("Height:", self.height, "Frame height in pixels", 7),
            ("Frame Rate:", self.frame_rate, "Frames per second (1-60)", 8),
            ("Duration:", self.duration, "Total duration in milliseconds", 9),
        ]
        for label_text, var, tooltip, row in params:
            ttkb.Label(params_frame, text=label_text).grid(row=row, column=0, padx=5, pady=2, sticky=E)
            entry = ttkb.Entry(params_frame, textvariable=var)
            entry.grid(row=row, column=1, padx=5, pady=2, sticky=EW)
            ToolTip(entry, text=tooltip)
        params_frame.columnconfigure(1, weight=1)
        action_frame = ttkb.Frame(main_frame)
        action_frame.pack(fill=X, pady=2)
        ttkb.Button(action_frame, text="🚀 Generate Pack", style="success.TButton", command=self.generate).pack(pady=2)
        status_frame = ttkb.LabelFrame(main_frame, text="Status", padding=8)
        status_frame.pack(fill=X, pady=2)
        ttkb.Label(status_frame, textvariable=self.status_var, wraplength=450).pack(pady=2)
        self.progress_bar = ttkb.Progressbar(status_frame, variable=self.progress_var, maximum=100, mode="determinate")
        self.progress_bar.pack(fill=X, pady=2)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(0, weight=1)

    def toggle_theme(self):
        current_theme = self.style.theme.name
        new_theme = "flatly" if current_theme == "darkly" else "darkly"
        self.style.theme_use(new_theme)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_path.set(directory)
            self.status_var.set(f"Selected directory: {directory}")
            if self.temp_dir:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                self.temp_dir = None

    def select_zips(self):
        zip_files = filedialog.askopenfilenames(filetypes=[("Zip files", "*.zip")])
        if zip_files:
            if self.temp_dir:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.temp_dir = tempfile.mkdtemp()
            for i, zip_file in enumerate(zip_files):
                try:
                    shutil.unpack_archive(zip_file, os.path.join(self.temp_dir, f"zip_{i}"))
                    self.status_var.set(f"Unpacked ZIP {i + 1}/{len(zip_files)}: {zip_file}")
                    self.root.update()
                except Exception as e:
                    self.status_var.set(f"Error unpacking ZIP {zip_file}: {e}")
            self.selected_path.set(self.temp_dir)
            self.status_var.set(f"Selected {len(zip_files)} ZIP files")

    def generate(self):
        if not self.selected_path.get():
            messagebox.showerror("Error", "Please select a directory or zip files")
            return
        input_directory = self.selected_path.get()
        try:
            pack_name = self.pack_name.get().strip()
            if not pack_name:
                raise ValueError("Pack name must be entered")
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

        self.progress_var.set(0)
        self.status_var.set("Starting generation...")
        self.root.update()

        temp_work_dir = tempfile.mkdtemp()
        asset_packs_dir = os.path.join(temp_work_dir, "AssetPacks")
        os.makedirs(asset_packs_dir, exist_ok=True)

        pack_dir = os.path.join(asset_packs_dir, pack_name)
        os.makedirs(pack_dir, exist_ok=True)
        anims_dir = os.path.join(pack_dir, "Anims")
        os.makedirs(anims_dir, exist_ok=True)

        anim_dirs = []

        if self.temp_dir:
            for zip_dir in os.listdir(self.temp_dir):
                zip_path = os.path.join(self.temp_dir, zip_dir)
                if os.path.isdir(zip_path):
                    anims_path = os.path.join(zip_path, "Anims")
                    if os.path.exists(anims_path):
                        for d in os.listdir(anims_path):
                            anim_source = os.path.join(anims_path, d)
                            if os.path.isdir(anim_source):
                                anim_dirs.append((d, anim_source))
                                self.status_var.set(f"Found animation: {d} in {zip_dir}")
                                self.root.update()
                    else:
                        files = [f for f in os.listdir(zip_path) if re.match(r'^frame_\d+_delay-.*\.png$', f)]
                        if files:
                            animation_name = f"Animation_{zip_dir}"
                            anim_dir = os.path.join(anims_dir, animation_name)
                            os.makedirs(anim_dir, exist_ok=True)
                            files.sort()
                            for i, file in enumerate(files):
                                shutil.copy(os.path.join(zip_path, file), os.path.join(anim_dir, f"frame_{i}.png"))
                            anim_dirs.append((animation_name, anim_dir))
                            self.status_var.set(f"Created animation: {animation_name} from {zip_dir}")
                            self.root.update()
        elif os.path.exists(os.path.join(input_directory, "Anims")):
            for d in os.listdir(os.path.join(input_directory, "Anims")):
                anim_source = os.path.join(input_directory, "Anims", d)
                if os.path.isdir(anim_source):
                    anim_dirs.append((d, anim_source))
                    self.status_var.set(f"Found animation: {d} in directory")
                    self.root.update()
        else:
            subdirs = [d for d in os.listdir(input_directory) if os.path.isdir(os.path.join(input_directory, d)) and not d.startswith(".")]
            for subdir in subdirs:
                subdir_path = os.path.join(input_directory, subdir)
                files = [f for f in os.listdir(subdir_path) if re.match(r'^frame_\d+_delay-.*\.png$', f)]
                if files:
                    animation_name = f"Animation_{subdir}"
                    anim_dir = os.path.join(anims_dir, animation_name)
                    os.makedirs(anim_dir, exist_ok=True)
                    files.sort()
                    for i, file in enumerate(files):
                        shutil.copy(os.path.join(subdir_path, file), os.path.join(anim_dir, f"frame_{i}.png"))
                    anim_dirs.append((animation_name, anim_dir))
                    self.status_var.set(f"Created animation: {animation_name} from {subdir}")
                    self.root.update()

        if not anim_dirs:
            files = [f for f in os.listdir(input_directory) if re.match(r'^frame_\d+_delay-.*\.png$', f)]
            if not files:
                messagebox.showerror("Error", "No PNG files to process in the selected directory")
                return
            files.sort()
            animation_name = "DefaultAnimation"
            anim_dir = os.path.join(anims_dir, animation_name)
            os.makedirs(anim_dir, exist_ok=True)
            for i, file in enumerate(files):
                shutil.copy(os.path.join(input_directory, file), os.path.join(anim_dir, f"frame_{i}.png"))
            anim_dirs.append((animation_name, anim_dir))
            self.status_var.set(f"Created default animation: {animation_name}")
            self.root.update()

        self.progress_var.set(30)
        self.root.update()

        for anim_name, anim_path in anim_dirs:
            target_anim_dir = os.path.join(anims_dir, anim_name)
            if not os.path.exists(target_anim_dir):
                shutil.copytree(anim_path, target_anim_dir)
            num_frames = len([f for f in os.listdir(target_anim_dir) if f.startswith("frame_") and f.endswith(".png")])
            meta_path = os.path.join(target_anim_dir, "meta.txt")
            if not os.path.exists(meta_path):
                with open(meta_path, "w") as f:
                    f.write("Filetype: Flipper Animation\n")
                    f.write("Version: 1\n")
                    f.write(f"Width: {width}\n")
                    f.write(f"Height: {height}\n")
                    f.write(f"Passive frames: {num_frames}\n")
                    f.write("Active frames: 0\n")
                    f.write(f"Frames order: {' '.join(map(str, range(num_frames)))}\n")
                    f.write("Active cycles: 0\n")
                    f.write(f"Frame rate: {frame_rate}\n")
                    f.write(f"Duration: {duration}\n")
                    f.write("Active cooldown: 0\n")
                    f.write("Bubble slots: 0\n")
            self.progress_var.set(self.progress_var.get() + (50 / len(anim_dirs)))
            self.status_var.set(f"Processed animation: {anim_name}")
            self.root.update()

        manifest_path = os.path.join(anims_dir, "manifest.txt")
        if not os.path.exists(manifest_path):
            with open(manifest_path, "w") as f:
                f.write("Filetype: Flipper Animation Manifest\n")
                f.write("Version: 1\n")
                for anim_name, _ in anim_dirs:
                    f.write(f"Name: {anim_name}\n")
                    f.write(f"Min butthurt: {min_butthurt}\n")
                    f.write(f"Max butthurt: {max_butthurt}\n")
                    f.write(f"Min level: {min_level}\n")
                    f.write(f"Max level: {max_level}\n")
                    f.write(f"Weight: {weight}\n")

        self.progress_var.set(80)
        self.status_var.set("Converting to .bm format...")
        self.root.update()

        output_dir = os.path.join(temp_work_dir, "asset_packs")
        asset_packer.pack(asset_packs_dir, output_dir, logger=lambda x: self.status_var.set(x))

        self.progress_var.set(90)
        self.root.update()

        save_dir = filedialog.askdirectory(title="Select directory to save asset_packs")
        if save_dir:
            dest_dir = os.path.join(save_dir, "asset_packs")
            os.makedirs(dest_dir, exist_ok=True)
            for item in os.listdir(output_dir):
                src_item = os.path.join(output_dir, item)
                dst_item = os.path.join(dest_dir, item)
                if os.path.exists(dst_item):
                    response = messagebox.askyesno("Conflict", f"A pack named '{item}' already exists. Replace it?")
                    if not response:
                        continue
                    if os.path.isdir(dst_item):
                        shutil.rmtree(dst_item, ignore_errors=True)
                    else:
                        os.remove(dst_item)
                if os.path.isdir(src_item):
                    shutil.copytree(src_item, dst_item)
                else:
                    shutil.copy2(src_item, dst_item)
            self.progress_var.set(100)
            self.status_var.set("Asset pack successfully saved")
            messagebox.showinfo("Success", "Asset pack successfully saved")
        else:
            self.status_var.set("Asset pack generation cancelled")
            messagebox.showwarning("Warning", "Asset pack will be deleted")
            shutil.rmtree(output_dir, ignore_errors=True)

        shutil.rmtree(temp_work_dir, ignore_errors=True)
        if self.temp_dir:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.temp_dir = None
            self.selected_path.set("")
        self.progress_var.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
