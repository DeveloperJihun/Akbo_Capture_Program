import pyautogui
import pytesseract
from PIL import Image
import state

# Windows 환경에서는 설치 경로 지정 필요
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def capture_and_read_text():
    """지정된 영역을 캡처 후 OCR로 글자 인식"""
    if not state.capture_region:
        print("⚠️ 먼저 캡처 영역을 지정하세요!")
        return

    # 스크린샷 찍기
    img = pyautogui.screenshot(region=state.capture_region)

    # OCR 실행 (영어 기준, 한국어는 lang="kor" 사용)
    text = pytesseract.image_to_string(img, lang="eng")
    print("📖 OCR 인식 결과:")
    print(text.strip())
