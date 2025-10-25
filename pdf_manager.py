from tkinter import messagebox
from PIL import Image
import os, glob, re

def make_pdf_a4(folder_path):
    """선택한 폴더 안 이미지를 A4 PDF로 변환"""
    song_title = os.path.basename(folder_path)
    files = glob.glob(os.path.join(folder_path, "*.png"))
    if not files:
        messagebox.showwarning("경고", f"{song_title} 폴더에 PNG 파일이 없습니다!")
        return

    def extract_number(filename):
        match = re.search(r"_(\d+)\.png$", filename)
        return int(match.group(1)) if match else 0

    files = sorted(files, key=extract_number)

    A4_WIDTH, A4_HEIGHT = 2480, 3508
    pages, current_page, y_offset = [], Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white"), 0

    for f in files:
        img = Image.open(f).convert("RGB")
        ratio = A4_WIDTH / img.width
        new_h = int(img.height * ratio)
        img = img.resize((A4_WIDTH, new_h), Image.LANCZOS)

        if y_offset + new_h > A4_HEIGHT:
            pages.append(current_page)
            current_page = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
            y_offset = 0

        current_page.paste(img, (0, y_offset))
        y_offset += new_h

    pages.append(current_page)
    pdf_path = os.path.join(folder_path, f"{song_title}_A4.pdf")
    pages[0].save(pdf_path, save_all=True, append_images=pages[1:])
    messagebox.showinfo("완료", f"A4 PDF 생성됨: {pdf_path}")
