"""Aesthetic, single-instance LOLA player game launcher."""

import random
import tkinter as tk
from tkinter import filedialog, ttk
import game_launcher_core as core

BG, PANEL, BTN, HOVER, GOLD, TITLE, TEXT, MUTED = (
    "#0e1326", "#161b33", "#5b3d73", "#764f94",
    "#ffe8a3", "#f2d8ff", "#eee7f5", "#9ea4c2"
)


def load_hero_image(target_w, target_h):
    """Load menu artwork anchored to the LEFT side so Maya is never cropped."""
    try:
        from PIL import Image, ImageEnhance, ImageTk
        pics = sorted((core.GAME_DIR / "images" / "menu_assets").glob("*.jpg"))
        if not pics:
            return None
        orig = Image.open(random.choice(pics))
        ow, oh = orig.size
        # Anchor left: scale height to fit target_h, keep the left target_w pixels
        scale = target_h / oh
        scaled_w = int(ow * scale)
        scaled = orig.resize((scaled_w, target_h), Image.Resampling.LANCZOS)
        # Crop from the left edge: (0, 0, target_w, target_h)
        cropped = scaled.crop((0, 0, min(scaled_w, target_w), target_h))
        return ImageTk.PhotoImage(ImageEnhance.Brightness(cropped).enhance(0.92))
    except Exception:
        return None


class GameLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.cfg = core.load()
        self.title("LOLA")
        self.configure(bg=BG)
        self.resizable(False, False)
        w, h = 760, 460
        self.geometry(f"{w}x{h}+{(self.winfo_screenwidth() - w) // 2}+{(self.winfo_screenheight() - h) // 2}")
        self._hero = load_hero_image(360, h)
        self._build(h)

    def _build(self, h):
        left = tk.Canvas(self, width=360, height=h, bg="#18122b", highlightthickness=0)
        left.pack(side="left", fill="y")
        if self._hero:
            left.create_image(0, 0, anchor="nw", image=self._hero)
        right = tk.Frame(self, bg=BG, padx=32, pady=28)
        right.pack(side="right", fill="both", expand=True)
        tk.Label(right, text="LOLA", font=("Segoe UI", 34, "bold"), fg=TITLE, bg=BG).pack(anchor="w")
        tk.Label(right, text="A New City, A New Beginning", font=("Segoe UI", 11), fg=TEXT, bg=BG).pack(anchor="w")
        tk.Label(right, text=f"v{core.detect_game_version()}", font=("Segoe UI", 9), fg=MUTED, bg=BG).pack(anchor="w", pady=(2, 16))
        self._play_btn(right)
        opts = tk.Frame(right, bg=PANEL, padx=14, pady=12)
        opts.pack(fill="x", pady=(14, 12))
        self.fs = tk.BooleanVar(value=bool(self.cfg.get("fullscreen")))
        tk.Checkbutton(opts, text="Start Fullscreen", variable=self.fs, command=self._save, fg=TEXT, bg=PANEL,
                       selectcolor=BG, activebackground=PANEL, activeforeground=TEXT, font=("Segoe UI", 9)).pack(anchor="w")
        tk.Label(opts, text="Display Renderer", fg=MUTED, bg=PANEL, font=("Segoe UI", 8)).pack(anchor="w", pady=(8, 2))
        self.mode = ttk.Combobox(opts, values=list(core.MODES), state="readonly", width=28)
        self.mode.set(self.cfg["mode"])
        self.mode.pack(fill="x")
        self.mode.bind("<<ComboboxSelected>>", lambda e: self._save())
        foot = tk.Frame(right, bg=BG)
        foot.pack(fill="x", side="bottom")
        tk.Button(foot, text="Exit", command=self.destroy, bg=BG, fg=MUTED, activeforeground=TEXT,
                  activebackground=BG, relief="flat", cursor="hand2", font=("Segoe UI", 9)).pack(side="right")
        if not self.cfg["sdk"]:
            tk.Button(foot, text="Locate Ren'Py SDK…", command=self._pick_sdk, bg=BG, fg=GOLD,
                      activebackground=BG, relief="flat", cursor="hand2", font=("Segoe UI", 9)).pack(side="left")
        self.status = tk.Label(right, text="", fg=GOLD, bg=BG, font=("Segoe UI", 9), wraplength=310, justify="left")
        self.status.pack(anchor="w", pady=(4, 0))

    def _play_btn(self, parent):
        btn = tk.Button(parent, text="Play LOLA", command=self._play, bg=BTN, fg="#ffffff", relief="flat",
                        activebackground=HOVER, activeforeground=GOLD, cursor="hand2", pady=11, font=("Segoe UI", 13, "bold"))
        btn.bind("<Enter>", lambda e: btn.config(bg=HOVER, fg=GOLD))
        btn.bind("<Leave>", lambda e: btn.config(bg=BTN, fg="#ffffff"))
        btn.pack(fill="x")

    def _save(self):
        self.cfg["mode"], self.cfg["fullscreen"] = self.mode.get(), bool(self.fs.get())
        core.save(self.cfg)

    def _pick_sdk(self):
        folder = filedialog.askdirectory(title="Select Ren'Py SDK folder")
        if folder:
            self.cfg["sdk"] = folder.replace("\\", "/")
            core.save(self.cfg)
            self.status.config(text="Ren'Py SDK saved.")

    def _play(self):
        self._save()
        ok, msg = core.launch_game(self.cfg)
        self.status.config(text=msg)
        if ok:
            self.after(350, self.destroy)


if __name__ == "__main__":
    if core.acquire_launcher_mutex():
        GameLauncher().mainloop()
