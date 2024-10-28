"""
需求方:VAT
功能 :
    1.该脚本用于将本地的txt/csv文件转换成为excel格式 , 执行完程序后会在原路径生成同名的excel文件
    2.该脚本用于将本地的pdf文件转换成为jpg图片 , 执行完程序后会在原路径生成同名_页码(0开始)的.jpg图片
参数 : sys.argv[1]-->指本地文件路径
"""
import pandas as pd
import sys
import chardet
from pdf2image import convert_from_path
# 文件路径
source_data = sys.argv[1]

def detect_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    return chardet.detect(raw_data)['encoding']

if __name__ == "__main__":
    # 判断文件的编码格式
    file_encoding = detect_file_encoding(source_data)
    # 判断文件的后缀再分别进行处理
    if source_data.endswith('.txt'):
        data = pd.read_csv(source_data,sep='\t',encoding=file_encoding,index_col=0)
        target_data = source_data.replace('.txt', '.xlsx')
        data.to_excel(target_data,encoding='UTF-8')
    elif source_data.endswith('.csv'):
        data = pd.read_csv(source_data, encoding=file_encoding, index_col=0)
        target_data = source_data.replace('.csv', '.xlsx')
        data.to_excel(target_data,encoding='UTF-8')
    elif source_data.endswith('.pdf'):
        images = convert_from_path(source_data)
        source_name = source_data[:-4]
        for i, image in enumerate(images):
            image.save(f'{source_name}_{i}.jpg', 'JPEG')