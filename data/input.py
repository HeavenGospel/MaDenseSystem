def input(file_path):
    lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # 去掉每行末尾的换行符并忽略空行
        lines = [line.strip() for line in lines if line.strip()]
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
    return lines
