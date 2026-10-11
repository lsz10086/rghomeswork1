# main.py
import streamlit as st
from agent import CodeExplainerAgent

# 设置网页标题和图标
st.set_page_config(page_title="代码解释 Agent", page_icon="🤖", layout="wide")

st.title("🤖 代码解释 Agent")
st.markdown(
    "欢迎使用！你可以直接输入本地代码文件的路径（例如 `test_code.py`），或者直接粘贴一段代码，我会自动帮你解释逻辑并生成注释。")

# 初始化 Agent
# 利用 streamlit 的 session_state 保持对话上下文，刷新网页也不会丢失记忆
if "agent" not in st.session_state:
    st.session_state.agent = CodeExplainerAgent()

# 显示历史聊天记录
# 遍历 Agent 内部保存的 messages，把它们展示在网页上
for message in st.session_state.agent.messages:
    # 跳过 system 提示词不显示
    if message["role"] == "system":
        continue

    # 对用户消息进行展示
    if message["role"] == "user":
        # 如果这条消息是工具的执行结果，不显示在聊天框里，保持界面整洁
        if "工具执行结果如下" in message["content"]:
            continue
        with st.chat_message("user"):
            st.markdown(message["content"])

    # 对 Agent 消息进行展示
    elif message["role"] == "assistant":
        # 如果 Agent 的回复是个 JSON（工具调用指令），也不显示在界面上
        if message["content"].strip().startswith("{"):
            continue
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# 接收用户输入
if prompt := st.chat_input("请输入代码文件路径（如 test_code.py），或直接粘贴代码..."):
    # 1. 在界面上显示用户输入
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 调用 Agent 并显示回复
    with st.chat_message("assistant"):
        with st.spinner("Agent 正在阅读代码并思考中..."):
            response = st.session_state.agent.chat(prompt)
            st.markdown(response)