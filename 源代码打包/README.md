# 代码解释 Agent (Code Explainer Agent)

1. 项目简介
本项目基于大语言模型（LLM）构建了一个代码解释助手 Agent。用户输入本地代码文件路径后，Agent 会自动调用文件读取工具，分析代码逻辑并生成详细解释和修改建议。

2. 核心技术实现
Agent 架构：采用 ReAct（Reasoning + Acting）模式，通过原生 LLM API 实现“思考-工具调用-观察-输出”的循环。
工具集成：实现了 `read_code_file` 工具，能够安全读取本地代码文件。
Prompt 设计：精心设计系统提示词，引导模型在需要读取文件时输出特定 JSON 格式，以此触发工具调用。
上下文记忆：利用 `messages` 列表维护对话历史，支持连续追问。
错误处理：针对 API 调用和文件读取设计了容错机制。

3. 环境安装与使用
1. 安装依赖：`pip install -r requirements.txt`
2. 配置 `.env` 文件（deepseek API Key）。
3. 启动命令：`streamlit run main.py`
4. 在浏览器中打开显示的地址，输入文件路径（如 `test_code.py`）即可体验。

4. 项目结构
- `main.py`：Streamlit Web 界面入口
- `agent.py`：Agent 核心循环逻辑
- `prompts.py`：系统提示词
- `tools.py`：工具函数（文件读取）
- `test_code.py`：测试用例代码

5. 演示截图
![演示截图](./demo.png)