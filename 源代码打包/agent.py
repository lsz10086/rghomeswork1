# agent.py
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT
from tools import read_code_file

# 加载 .env 文件中的环境变量（API Key 和 Base URL）
load_dotenv()

# 初始化 OpenAI 客户端（兼容 DeepSeek 等平台）
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL") if os.getenv("OPENAI_BASE_URL") else None
)


class CodeExplainerAgent:
    def __init__(self):
        # 维护对话上下文记忆：messages 列表会保存所有的历史对话
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def execute_tool(self, tool_name, tool_input):
        """根据模型要求执行具体的工具函数"""
        if tool_name == "read_code_file":
            return read_code_file(tool_input)
        return f"错误：未知的工具 {tool_name}"

    def chat(self, user_input: str):
        """Agent 的主循环：接收用户输入，推理，调用工具，直到得出最终答案"""
        # 1. 记录用户的输入
        self.messages.append({"role": "user", "content": user_input})

        # 开启循环（最多循环 5 次，防止死循环）
        for _ in range(5):
            # 2. 调用大模型进行推理
            try:
                response = client.chat.completions.create(
                    model="deepseek-chat",  # 如果你用 OpenAI，改成 "gpt-4o-mini"
                    messages=self.messages,
                    temperature=0.2,  # 代码任务温度调低，保证输出的严谨性
                )
                reply = response.choices[0].message.content.strip()
            except Exception as e:
                return f"API 调用失败，错误信息：{e}"

            # 3. 记录大模型的回复
            self.messages.append({"role": "assistant", "content": reply})

            # 4. 判断大模型是否想调用工具（检查回复是否为 JSON 格式）
            if reply.startswith("{") and "action" in reply:
                try:
                    action_data = json.loads(reply)
                    action_name = action_data.get("action")
                    action_input = action_data.get("action_input")

                    if action_name == "read_code_file":
                        print(f"\n[🤖 Agent 思考中] 检测到需要读取文件：{action_input}...")

                        # 5. 执行工具，获取文件内容
                        tool_result = self.execute_tool(action_name, action_input)

                        # 6. 把工具执行结果作为新的 user 消息喂回给大模型，让它继续处理
                        self.messages.append({
                            "role": "user",
                            "content": f"工具执行结果如下：\n{tool_result}\n\n请根据上述代码给出详细的解释和注释。"
                        })
                        continue  # 继续循环，让大模型读取内容后给出真正的解释
                except json.JSONDecodeError:
                    pass  # 如果不是合法的 JSON，按普通文本处理

            # 7. 如果大模型没有调用工具，直接返回最终解释结果
            return reply

        return "Agent 处理超时，请重新输入。"