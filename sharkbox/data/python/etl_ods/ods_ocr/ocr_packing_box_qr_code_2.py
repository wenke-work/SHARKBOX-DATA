from paddleocr import PaddleOCR,draw_ocr

ocr = PaddleOCR(use_angle_cls=True, lang="ch")
img_path = 'C:\\Users\\Administrator\\Desktop\\files\\temp\\tmp\\1.png'
result = ocr.ocr(img_path, cls=True)
print(result)
