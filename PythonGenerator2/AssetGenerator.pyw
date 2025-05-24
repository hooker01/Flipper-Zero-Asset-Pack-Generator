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

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Asset Pack Generator")
        self.style = ttkb.Style(theme="darkly")
        self.root.geometry("800x600")
        self.root.minsize(600, 350)
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

    def check_pack_name(self, pack_name, asset_packs_dir):
        pack_dir = os.path.join(asset_packs_dir, pack_name)
        if os.path.exists(pack_dir):
            dialog = ttkb.Toplevel(self.root)
            dialog.title("Name Conflict")
            dialog.transient(self.root)
            dialog.grab_set()
            ttkb.Label(dialog, text=f"Pack '{pack_name}' already exists. Do you want to replace it or choose a new name?", wraplength=300).pack(padx=20, pady=10)
            replace_button = ttkb.Button(dialog, text="Replace", style="warning.TButton", command=lambda: dialog.destroy() or self.confirm_replace(pack_name, asset_packs_dir))
            replace_button.pack(side=LEFT, padx=5, pady=5)
            new_name_button = ttkb.Button(dialog, text="New Name", style="primary.TButton", command=lambda: dialog.destroy() or self.prompt_new_name(asset_packs_dir))
            new_name_button.pack(side=RIGHT, padx=5, pady=5)
            dialog.geometry("350x150")
            dialog.resizable(False, False)
            self.root.eval(f'tk::PlaceWindow {dialog} center')
            self.root.wait_window(dialog)
            return False
        return True

    def confirm_replace(self, pack_name, asset_packs_dir):
        pack_dir = os.path.join(asset_packs_dir, pack_name)
        shutil.rmtree(pack_dir, ignore_errors=True)
        self.continue_generate(pack_name, asset_packs_dir)

    def prompt_new_name(self, asset_packs_dir):
        dialog = ttkb.Toplevel(self.root)
        dialog.title("Enter New Pack Name")
        dialog.transient(self.root)
        dialog.grab_set()
        ttkb.Label(dialog, text="Enter a new pack name:").pack(padx=20, pady=5)
        new_name_var = tk.StringVar()
        entry = ttkb.Entry(dialog, textvariable=new_name_var)
        entry.pack(padx=20, pady=5)
        entry.focus_set()
        def submit():
            new_name = new_name_var.get().strip()
            if not new_name:
                messagebox.showerror("Error", "Pack name cannot be empty", parent=dialog)
                return
            if self.check_pack_name(new_name, asset_packs_dir):
                dialog.destroy()
                self.continue_generate(new_name, asset_packs_dir)
        ttkb.Button(dialog, text="Submit", style="primary.TButton", command=submit).pack(pady=5)
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        self.root.eval(f'tk::PlaceWindow {dialog} center')
        self.root.wait_window(dialog)

    def continue_generate(self, pack_name, asset_packs_dir):
        directory = self.selected_path.get()
        pack_dir = os.path.join(asset_packs_dir, pack_name)
        os.makedirs(pack_dir, exist_ok=True)
        anims_dir = os.path.join(pack_dir, "Anims")
        os.makedirs(anims_dir, exist_ok=True)
        anim_dirs = []
        self.progress_var.set(10)
        self.root.update()
        if self.temp_dir:
            for zip_dir in os.listdir(directory):
                zip_path = os.path.join(directory, zip_dir)
                if os.path.isdir(zip_path):
                    anims_path = os.path.join(zip_path, "Anims")
                    if os.path.exists(anims_path):
                        for d in os.listdir(anims_path):
                            if os.path.isdir(os.path.join(anims_path, d)):
                                anim_dirs.append((d, os.path.join(anims_path, d)))
                                self.status_var.set(f"Found animation: {d} in {zip_dir}")
                                self.root.update()
                    else:
                        files = [f for f in os.listdir(zip_path) if re.match(r'^frame_\d+_delay-.*\.png$', f)]
                        if files:
                            animation_name = f"Animation_{zip_dir}"
                            anim_dir = os.path.join(zip_path, "Anims", animation_name)
                            os.makedirs(anim_dir, exist_ok=True)
                            files.sort()
                            for i, file in enumerate(files):
                                new_name = f"frame_{i}.png"
                                os.rename(os.path.join(zip_path, file), os.path.join(anim_dir, new_name))
                            anim_dirs.append((animation_name, anim_dir))
                            self.status_var.set(f"Created animation: {animation_name} from {zip_dir}")
                            self.root.update()
        elif os.path.exists(os.path.join(directory, "Anims")):
            for d in os.listdir(os.path.join(directory, "Anims")):
                if os.path.isdir(os.path.join(directory, "Anims", d)):
                    anim_dirs.append((d, os.path.join(directory, "Anims", d)))
                    self.status_var.set(f"Found animation: {d} in directory")
                    self.root.update()
        else:
            files = [f for f in os.listdir(directory) if re.match(r'^frame_\d+_delay-.*\.png$', f)]
            if not files:
                messagebox.showerror("Error", "No PNG files to process in the selected directory")
                return
            files.sort()
            for i, file in enumerate(files):
                new_name = f"frame_{i}.png"
                os.rename(os.path.join(directory, file), os.path.join(directory, new_name))
            animation_name = "DefaultAnimation"
            animation_dir = os.path.join(anims_dir, animation_name)
            os.makedirs(animation_dir, exist_ok=True)
            for i in range(len(files)):
                shutil.move(os.path.join(directory, f"frame_{i}.png"), os.path.join(animation_dir, f"frame_{i}.png"))
            anim_dirs.append((animation_name, animation_dir))
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
                    f.write("Version: 1\n\n")
                    f.write(f"Width: {self.width.get()}\n")
                    f.write(f"Height: {self.height.get()}\n")
                    f.write(f"Passive frames: {num_frames}\n")
                    f.write("Active frames: 0\n")
                    f.write(f"Frames order: {' '.join(map(str, range(num_frames)))}\n")
                    f.write("Active cycles: 0\n")
                    f.write(f"Frame rate: {self.frame_rate.get()}\n")
                    f.write(f"Duration: {self.duration.get()}\n")
                    f.write("Active cooldown: 0\n\n")
                    f.write("Bubble slots: 0\n")
            self.progress_var.set(self.progress_var.get() + (50 / len(anim_dirs)))
            self.status_var.set(f"Processed animation: {anim_name}")
            self.root.update()
        manifest_path = os.path.join(anims_dir, "manifest.txt")
        source_manifest = os.path.join(directory, "Anims", "manifest.txt") if not self.temp_dir else None
        if not os.path.exists(manifest_path) and (not source_manifest or not os.path.exists(source_manifest)):
            with open(manifest_path, "w") as f:
                f.write("Filetype: Flipper Animation Manifest\n")
                f.write("Version: 1\n\n")
                for anim_name, _ in anim_dirs:
                    f.write(f"Name: {anim_name}\n")
                    f.write(f"Min butthurt: {self.min_butthurt.get()}\n")
                    f.write(f"Max butthurt: {self.max_butthurt.get()}\n")
                    f.write(f"Min level: {self.min_level.get()}\n")
                    f.write(f"Max level: {self.max_level.get()}\n")
                    f.write(f"Weight: {self.weight.get()}\n\n")
        elif source_manifest and os.path.exists(source_manifest):
            shutil.copy(source_manifest, manifest_path)
        self.progress_var.set(80)
        self.status_var.set("Converting to .bm format...")
        self.root.update()
        output_dir = os.path.join(directory, "asset_packs")
        os.makedirs(output_dir, exist_ok=True)
        asset_packer.pack(asset_packs_dir, output_dir, logger=lambda x: self.status_var.set(x))
        self.progress_var.set(90)
        self.root.update()
        save_dir = filedialog.askdirectory(title="Select directory to save asset_packs")
        if save_dir:
            dest_dir = os.path.join(save_dir, "asset_packs")
            os.makedirs(dest_dir, exist_ok=True)
            dest_pack_dir = os.path.join(dest_dir, pack_name)
            if os.path.exists(dest_pack_dir):
                shutil.rmtree(dest_pack_dir, ignore_errors=True)
            shutil.copytree(pack_dir, dest_pack_dir)
            self.progress_var.set(100)
            self.status_var.set("Asset pack successfully saved")
            messagebox.showinfo("Success", "Asset pack successfully saved")
        else:
            self.status_var.set("Asset pack generation cancelled")
            messagebox.showwarning("Warning", "Asset pack will not be saved")
        if self.temp_dir:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.temp_dir = None
            self.selected_path.set("")
        self.progress_var.set(0)

    def generate(self):
        if not self.selected_path.get():
            messagebox.showerror("Error", "Please select a directory or zip files")
            return
        directory = self.selected_path.get()
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
        asset_packs_dir = os.path.join(directory, "AssetPacks")
        os.makedirs(asset_packs_dir, exist_ok=True)
        if self.check_pack_name(pack_name, asset_packs_dir):
            self.continue_generate(pack_name, asset_packs_dir)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
