import re

def get_file_id(data: str):
    pattern = r'src="([^"]+)"'
    match = re.search(pattern, data)
    if match:
        # Получаем содержимое атрибута src
        return match.group(1), True
    else:
        return data, False
