import tkinter as tk
import keyboard
from capture import ask_song_title, select_area, capture_area, toggle_overlay
from folder_selector import show_folders
from ocr_reader import capture_and_read_text
from capture_overlay import open_resizable_overlay
root = tk.Tk()
root.title("노래별 자동 캡처 도구")

keyboard.add_hotkey("F9", capture_area)

btn_title = tk.Button(root, text="곡 제목 입력", command=ask_song_title, height=2, width=20)
btn_title.pack(padx=20, pady=5)

btn_select = tk.Button(root, text="캡처 영역 지정", command=lambda: select_area(root), height=2, width=20)
btn_select.pack(padx=20, pady=5)

btn_overlay_box = tk.Button(root, text="OCam 스타일 영역 조절", command=open_resizable_overlay, height=2, width=25)
btn_overlay_box.pack(padx=20, pady=5)

btn_capture = tk.Button(root, text="캡처 실행 (또는 F9)", command=capture_area, height=2, width=20)
btn_capture.pack(padx=20, pady=5)

btn_overlay = tk.Button(root, text="캡처 영역 미리보기 토글", command=toggle_overlay, height=2, width=20)
btn_overlay.pack(padx=20, pady=5)

btn_show_folders = tk.Button(root, text="폴더 목록 → PDF 생성", command=lambda: show_folders(root), height=2, width=25)
btn_show_folders.pack(padx=20, pady=5)

btn_ocr = tk.Button(root, text="캡처 영역 OCR 실행", command=capture_and_read_text, height=2, width=25)
btn_ocr.pack(padx=20, pady=5)

root.mainloop()
