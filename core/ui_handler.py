import fitz  # PyMuPDF
import tkinter as tk
from tkinter import Toplevel, Button
from PIL import Image, ImageTk
from utils.config import project_config as pjcf


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2) - 30
    window.geometry("{}x{}+{}+{}".format(width, height, x, y))


class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.pdf_ui = Toplevel(root)
        self.pdf_ui.geometry("720x720")
        self.pdf_ui.title("Information PDF")
        self.pdf_ui.iconbitmap(pjcf.INFO_ICON_PATH)
        self.pdf_ui.resizable(False, False)
        center_window(self.pdf_ui)

        self.pdf_path = pjcf.INFO_PDF_PATH
        if not self.pdf_path:
            self.pdf_ui.destroy()
            return

        self.document = fitz.open(self.pdf_path)
        self.page_number = 0
        self.total_pages = len(self.document)

        nav_frame = tk.Frame(self.pdf_ui, bg="lightgrey")
        nav_frame.pack(side=tk.TOP, fill=tk.X)

        self.prev_button = Button(
            nav_frame, text="Previous", width=30, command=self.prev_page
        )
        self.prev_button.pack(side=tk.LEFT, ipadx=15, ipady=7)

        self.next_button = Button(
            nav_frame, text="Next", width=30, command=self.next_page
        )
        self.next_button.pack(side=tk.RIGHT, ipadx=15, ipady=7)

        label_frame = tk.Frame(self.pdf_ui, bg="white")
        label_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.label = tk.Label(label_frame, bg="white")
        self.label.pack(side=tk.TOP)

        self.display_page(self.page_number)

    def display_page(self, page_number):
        page = self.document.load_page(page_number)
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        photo = ImageTk.PhotoImage(image)

        self.label.config(image=photo)
        self.label.image = photo

    def next_page(self):
        if self.page_number < self.total_pages - 1:
            self.page_number += 1
            self.display_page(self.page_number)

    def prev_page(self):
        if self.page_number > 0:
            self.page_number -= 1
            self.display_page(self.page_number)


def open_info():
    PDFViewer(root)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x200")
    root.title("Main Window")

    frame_button_1 = tk.Frame(root)
    frame_button_1.pack(side=tk.RIGHT, padx=5, pady=5, ipadx=5, ipady=5)

    info_btn = tk.Button(frame_button_1, text="INFO", command=open_info)
    info_btn.pack(side=tk.BOTTOM, padx=5, pady=5, ipadx=20, ipady=10)

    root.mainloop()
