# translate comments from Chinese to English version,
# and remain Chinese version

# -*- coding: utf-8 -*-
# translate Python comments from Chinese to English and keep original Chinese
import os
import re
from googletrans import Translator
import chardet
import time

root_folder = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\python"

translator = Translator()
chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')

def translate_text(text, retries=3, delay=1):
    """Translate Chinese text to English with retries"""
    for i in range(retries):
        try:
            return translator.translate(text, src='zh-cn', dest='en').text
        except Exception as e:
            if i < retries - 1:
                time.sleep(delay)  # wait a bit before retry
                continue
            else:
                print(f"Translation failed for: {text}, error: {e}")
                return text  # return original text if failed

for dirpath, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        if filename.endswith(".py"):
            file_path = os.path.join(dirpath, filename)
            print(f"Processing: {file_path}")

            # 自动检测文件编码  # English: Automatically detect file encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding'] if result['encoding'] else 'utf-8'

            # 读取文件  # English: Read the file
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                new_line = line
                stripped = line.strip()

                # 处理整行注释  # English: Process entire line comments
                if stripped.startswith("#"):
                    if "English:" not in line:
                        match = chinese_pattern.search(line)
                        if match:
                            chinese_text = match.group()
                            translated = translate_text(chinese_text)
                            new_line = line.rstrip('\n') + f"  # English: {translated}\n"

                # 处理行尾注释  # English: Process end-of-line comments
                elif "#" in line:
                    parts = line.split("#", 1)
                    code_part = parts[0]
                    comment_part = parts[1]
                    if "English:" not in comment_part:
                        match = chinese_pattern.search(comment_part)
                        if match:
                            chinese_text = match.group()
                            translated = translate_text(chinese_text)
                            new_line = code_part.rstrip() + f"  # {comment_part.strip()}  # English: {translated}\n"

                new_lines.append(new_line)

            # 保存文件，统一用 UTF-8 编码覆盖  # English: Save the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

print("All files processed successfully!")
