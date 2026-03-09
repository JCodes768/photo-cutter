from __future__ import annotations

import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from photo_splitter_core import process_folder


class PhotoCutterApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Photo Cutter – Pentax 17")
        self.resizable(False, False)

        self.input_dir_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.auto_gap_var = tk.BooleanVar(value=True)
        self.crop_border_var = tk.StringVar(value="25")
        self.overwrite_var = tk.BooleanVar(value=False)

        self._build_widgets()
        self._worker_thread: threading.Thread | None = None

    def _build_widgets(self) -> None:
        padding = {"padx": 10, "pady": 5}

        main = ttk.Frame(self)
        main.grid(row=0, column=0, sticky="nsew")

        # Input folder
        ttk.Label(main, text="Input folder with scans:").grid(row=0, column=0, sticky="w", **padding)
        input_row = ttk.Frame(main)
        input_row.grid(row=1, column=0, sticky="ew", **padding)
        input_entry = ttk.Entry(input_row, textvariable=self.input_dir_var, width=50)
        input_entry.grid(row=0, column=0, sticky="ew")
        ttk.Button(input_row, text="Browse…", command=self.browse_input).grid(row=0, column=1, padx=(5, 0))

        # Output folder
        ttk.Label(main, text="Output folder (optional):").grid(row=2, column=0, sticky="w", **padding)
        output_row = ttk.Frame(main)
        output_row.grid(row=3, column=0, sticky="ew", **padding)
        output_entry = ttk.Entry(output_row, textvariable=self.output_dir_var, width=50)
        output_entry.grid(row=0, column=0, sticky="ew")
        ttk.Button(output_row, text="Browse…", command=self.browse_output).grid(row=0, column=1, padx=(5, 0))

        # Options
        options = ttk.LabelFrame(main, text="Options")
        options.grid(row=4, column=0, sticky="ew", **padding)

        ttk.Checkbutton(
            options,
            text="Use auto gap (recommended for Pentax 17)",
            variable=self.auto_gap_var,
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=8, pady=4)

        ttk.Label(options, text="Border crop (pixels):").grid(row=1, column=0, sticky="w", padx=8, pady=4)
        ttk.Entry(options, textvariable=self.crop_border_var, width=6).grid(
            row=1, column=1, sticky="w", padx=8, pady=4
        )

        ttk.Checkbutton(
            options,
            text="Overwrite existing files",
            variable=self.overwrite_var,
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=8, pady=(0, 8))

        # Run button
        self.run_button = ttk.Button(main, text="Run", command=self.on_run_clicked)
        self.run_button.grid(row=5, column=0, sticky="e", **padding)

        # Log output
        log_frame = ttk.LabelFrame(main, text="Log")
        log_frame.grid(row=6, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.log_text = tk.Text(log_frame, width=70, height=12, state="disabled")
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

    def browse_input(self) -> None:
        folder = filedialog.askdirectory(title="Select folder with scans")
        if folder:
            self.input_dir_var.set(folder)

    def browse_output(self) -> None:
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_dir_var.set(folder)

    def append_log(self, text: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def on_run_clicked(self) -> None:
        if self._worker_thread and self._worker_thread.is_alive():
            messagebox.showinfo("Photo Cutter", "Already running. Please wait for it to finish.")
            return

        input_dir_str = self.input_dir_var.get().strip()
        if not input_dir_str:
            messagebox.showerror("Photo Cutter", "Please choose an input folder with your scans.")
            return

        input_dir = Path(input_dir_str)
        if not input_dir.exists():
            messagebox.showerror("Photo Cutter", f"Input folder does not exist:\n{input_dir}")
            return

        output_dir_str = self.output_dir_var.get().strip()
        output_dir = Path(output_dir_str) if output_dir_str else input_dir / "split"

        try:
            crop_border = int(self.crop_border_var.get() or "0")
        except ValueError:
            messagebox.showerror("Photo Cutter", "Border crop must be a whole number of pixels.")
            return

        auto_gap = self.auto_gap_var.get()
        overwrite = self.overwrite_var.get()

        self.run_button.config(state="disabled")
        self.append_log(
            f"Starting…\nInput: {input_dir}\nOutput: {output_dir}\n"
            f"Auto gap: {auto_gap}, crop_border: {crop_border}, overwrite: {overwrite}"
        )

        def worker() -> None:
            try:
                process_folder(
                    input_dir=input_dir,
                    output_dir=output_dir,
                    crop_border=crop_border,
                    overwrite=overwrite,
                    auto_gap=auto_gap,
                )
                self.after(0, lambda: self.append_log("Done."))
                self.after(
                    0,
                    lambda: messagebox.showinfo(
                        "Photo Cutter",
                        f"Finished splitting images.\n\nOutput folder:\n{output_dir}",
                    ),
                )
            except Exception as exc:  # noqa: BLE001
                self.after(0, lambda: self.append_log(f"Error: {exc}"))
                self.after(
                    0,
                    lambda: messagebox.showerror(
                        "Photo Cutter",
                        f"An error occurred:\n{exc}",
                    ),
                )
            finally:
                self.after(0, lambda: self.run_button.config(state="normal"))

        self._worker_thread = threading.Thread(target=worker, daemon=True)
        self._worker_thread.start()


def main() -> None:
    app = PhotoCutterApp()
    app.mainloop()


if __name__ == "__main__":
    main()

