# tools.py
import os


def read_code_file(file_path: str) -> str:
    """
    读取指定路径的代码文件内容，并返回字符串。
    如果文件不存在或读取失败，会返回错误提示。
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return f"错误：找不到文件 {file_path}，请确认路径是否正确。"

        # 以 UTF-8 格式读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

            # 防止文件太大超出大模型上下文限制（这里限制大约 8000 字符）
            if len(content) > 8000:
                return content[:8000] + "\n\n...[注意：文件内容过长，已截断，仅分析前 8000 个字符]"

            return content

    except Exception as e:
        return f"读取文件失败，错误信息：{str(e)}"


# 这是写给大模型看的“工具说明书”
# 后续在 Prompt 中会用到它，告诉大模型有哪些工具可以调用
TOOLS_DEFINITION = """
你可以使用以下工具：
1. read_code_file(file_path: str): 读取指定路径的代码文件内容。如果用户提供了文件路径，请优先调用此工具获取代码。
"""