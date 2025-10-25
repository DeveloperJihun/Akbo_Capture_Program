import tkinter as tk
from tkinter import messagebox
import pyautogui
from PIL import Image
import os, glob, re, keyboard
from tkinter import simpledialog   # ⬅️ 추가
from tkinter import filedialog

# 전역 변수
count = 1
capture_region = None
song_title = None
SAVE_DIR = "captures"
overlay_window = None

def ask_song_title():
    """곡 제목 입력받고 폴더 생성"""
    global song_title, SAVE_DIR, count
    song_title = simpledialog.askstring("곡 제목 입력", "곡 제목을 입력하세요:")  # 수정됨
    if not song_title:
        messagebox.showwarning("경고", "곡 제목을 입력해야 합니다!")
        return False

    SAVE_DIR = os.path.join("captures", song_title)
    os.makedirs(SAVE_DIR, exist_ok=True)
    count = 1
    return True

def select_area():
    """캡처 영역 지정"""
    global capture_region
    if not song_title:
        if not ask_song_title():
            return

    root.withdraw()
    messagebox.showinfo("영역 선택", "마우스로 드래그하여 캡처 영역을 지정하세요.")

    sel = tk.Toplevel()
    sel.attributes("-fullscreen", True)
    sel.attributes("-alpha", 0.3)
    sel.configure(bg="gray")

    start = {"x": 0, "y": 0}
    rect = None

    def on_mouse_down(event):
        start["x"], start["y"] = event.x, event.y

    def on_mouse_drag(event):
        nonlocal rect
        if rect:
            canvas.delete(rect)
        rect = canvas.create_rectangle(start["x"], start["y"], event.x, event.y, outline="red", width=2)

    def on_mouse_up(event):
        global capture_region
        x1, y1, x2, y2 = start["x"], start["y"], event.x, event.y
        sel.destroy()

        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        capture_region = (x1, y1, x2 - x1, y2 - y1)
        messagebox.showinfo("완료", f"캡처 영역: {capture_region}")
        root.deiconify()

    canvas = tk.Canvas(sel, bg="gray")
    canvas.pack(fill="both", expand=True)
    canvas.bind("<Button-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)


def capture_area():
    """캡처 실행"""
    global count, capture_region, song_title

    if not capture_region:
        messagebox.showwarning("경고", "먼저 캡처할 영역을 지정하세요!")
        return

    img = pyautogui.screenshot(region=capture_region)
    filename = os.path.join(SAVE_DIR, f"{song_title}_{count}.png")
    img.save(filename)
    print(f"저장됨: {filename}")
    count += 1


def toggle_overlay():
    """캡처 영역 미리보기 토글"""
    global overlay_window, capture_region

    if not capture_region:
        messagebox.showwarning("경고", "먼저 캡처할 영역을 지정하세요!")
        return

    if overlay_window and tk.Toplevel.winfo_exists(overlay_window):
        overlay_window.destroy()
        overlay_window = None
    else:
        overlay_window = tk.Toplevel()
        overlay_window.overrideredirect(True)
        overlay_window.attributes("-alpha", 0.3)
        overlay_window.configure(bg="red")

        x, y, w, h = capture_region
        overlay_window.geometry(f"{w}x{h}+{x}+{y}")


def make_pdf_a4(folder_path):
    """선택한 폴더 안 이미지를 A4 PDF로 변환"""
    song_title = os.path.basename(folder_path)
    files = glob.glob(os.path.join(folder_path, "*.png"))
    if not files:
        messagebox.showwarning("경고", f"{song_title} 폴더에 PNG 파일이 없습니다!")
        return

    # 숫자 기준 정렬
    def extract_number(filename):
        match = re.search(r"_(\d+)\.png$", filename)
        return int(match.group(1)) if match else 0

    files = sorted(files, key=extract_number)

    # A4 사이즈 (픽셀, 300dpi 기준)
    A4_WIDTH, A4_HEIGHT = 2480, 3508

    pages = []
    current_page = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
    y_offset = 0

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


def show_folders():
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


# 단축키 등록 (F9 → 캡처)
keyboard.add_hotkey("F9", capture_area)

# 메인 윈도우
root = tk.Tk()
root.title("노래별 자동 캡처 도구")

btn_title = tk.Button(root, text="곡 제목 입력", command=ask_song_title, height=2, width=20)
btn_title.pack(padx=20, pady=5)

btn_select = tk.Button(root, text="캡처 영역 지정", command=select_area, height=2, width=20)
btn_select.pack(padx=20, pady=5)

btn_capture = tk.Button(root, text="캡처 실행 (또는 F9)", command=capture_area, height=2, width=20)
btn_capture.pack(padx=20, pady=5)

btn_overlay = tk.Button(root, text="캡처 영역 미리보기 토글", command=toggle_overlay, height=2, width=20)
btn_overlay.pack(padx=20, pady=5)

btn_show_folders = tk.Button(root, text="폴더 목록 → PDF 생성", command=show_folders, height=2, width=25)
btn_show_folders.pack(padx=20, pady=5)

root.mainloop()
