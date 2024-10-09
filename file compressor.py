import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import mimetypes

class CompressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lossless File Compression and Conversion App")
        self.root.configure(background="#f0f0f0")

        # Create GUI components
        self.file_label = tk.Label(root, text="Select a file:", font=("Helvetica", 12), fg="#00698f", bg="#f0f0f0")
        self.file_label.pack(pady=10)

        self.file_entry = tk.Entry(root, width=50, font=("Helvetica", 12))
        self.file_entry.pack()

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file, font=("Helvetica", 12), fg="#ffffff", bg="#00698f")
        self.browse_button.pack(pady=10)

        self.compress_button = tk.Button(root, text="Compress", command=self.compress_file, font=("Helvetica", 12), fg="#ffffff", bg="#00698f")
        self.compress_button.pack(pady=10)

        self.download_button = tk.Button(root, text="Download Compressed File", command=self.download_file, font=("Helvetica", 12), fg="#ffffff", bg="#00698f")
        self.download_button.pack(pady=10)

        self.convert_label = tk.Label(root, text="Convert to:", font=("Helvetica", 12), fg="#00698f", bg="#f0f0f0")
        self.convert_label.pack(pady=10)

        self.convert_options = tk.StringVar()
        self.convert_options.set("Select a format")
        self.convert_menu = tk.OptionMenu(root, self.convert_options, "Select a format", "JPEG", "PNG", "PDF")
        self.convert_menu.pack(pady=10)

        self.convert_button = tk.Button(root, text="Convert", command=self.convert_file, font=("Helvetica", 12), fg="#ffffff", bg="#00698f")
        self.convert_button.pack(pady=10)

        self.status_label = tk.Label(root, text="", font=("Helvetica", 12), fg="#00698f", bg="#f0f0f0")
        self.status_label.pack(pady=10)

        self.compressed_file_path = None  # Variable to store the path of the compressed file

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)

    def compress_file(self):
        file_path = self.file_entry.get()
        if not file_path:
            self.status_label.config(text="Please select a file")
            return

        try:
            # Compress image
            self.compressed_file_path = file_path.rsplit(".", 1)[0] + "_compressed.jpg"
            self.compress_image(file_path, self.compressed_file_path, quality=85)
            self.status_label.config(text="Image compressed successfully!")
        except Exception as e:
            self.status_label.config(text=f"Error during compression: {e}")

    def compress_image(self, input_file, output_file, quality=85):
        try:
            with Image.open(input_file) as img:
                img = img.convert("RGB")  # For JPEG, RGB format
                img.save(output_file, "JPEG", optimize=True, quality=quality)
            print(f"Image saved as {output_file}")
        except Exception as e:
            print(f"Error compressing image: {e}")

    def convert_file(self):
        file_path = self.file_entry.get()
        if not file_path:
            self.status_label.config(text="Please select a file")
            return

        convert_to = self.convert_options.get()
        if convert_to == "Select a format":
            self.status_label.config(text="Please select a conversion format")
            return

        output_file = file_path.rsplit(".", 1)[0] + f"_converted.{convert_to.lower()}"

        try:
            with Image.open(file_path) as img:
                img.save(output_file, format=convert_to.upper())
            self.status_label.config(text="File converted successfully!")
        except Exception as e:
            self.status_label.config(text=f"Error during conversion: {e}")

    def download_file(self):
        # If the file has been compressed or converted
        if self.compressed_file_path:
            if download_path := filedialog.asksaveasfilename(
                defaultextension=".jpg",
                initialfile=os.path.basename(self.compressed_file_path),
            ):
                os.rename(self.compressed_file_path, download_path)
                self.status_label.config(text="File downloaded successfully!")
                self.compressed_file_path = None  # Reset after download
        else:
            self.status_label.config(text="No file to download. Please compress or convert first.")

root = tk.Tk()
app = CompressionApp(root)
root.mainloop()
