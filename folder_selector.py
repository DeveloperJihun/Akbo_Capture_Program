import tkinter as tk
from tkinter import messagebox
import os, glob
from pdf_manager import make_pdf_a4

def show_folders(root):
    """captures 폴더 내의 곡제목 폴더 버튼 나열"""
    folder_window = tk.Toplevel(root)
    folder_window.title("PDF 생성할 폴더 선택")

    if not os.path.exists("captures"):
        messagebox.showwarning("경고", "captures 폴더가 존재하지 않습니다!")
        return

    subfolders = [f.path for f in os.scandir("captures") if f.is_dir()]
    if not subfolders:
        messagebox.showwarning("경고", "captures 폴더 안에 하위 폴더가 없습니다!")
        return

    for folder in subfolders:
        song_title = os.path.basename(folder)
        file_count = len(glob.glob(os.path.join(folder, "*.png")))
        btn = tk.Button(
            folder_window,
            text=f"{song_title} ({file_count}장)",
            command=lambda f=folder: make_pdf_a4(f),
            height=2, width=30
        )
        btn.pack(padx=10, pady=5)
