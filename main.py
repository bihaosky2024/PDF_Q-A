import streamlit as st

from RAG import init_graph_rag_pdf
from utils import separate_think_answer, save_temp_file


st.title("📑 AI智能PDF问答工具")

with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")

uploaded_file = st.file_uploader("上传你的PDF文件：", type="pdf")
if not uploaded_file:
    st.stop()

temp_file_path = "temp.pdf"
save_temp_file(temp_file_path, uploaded_file)

# Specify an ID for the thread
config = {"configurable": {"thread_id": "abc123"}}

if "messages_interact" not in st.session_state:
    st.session_state["messages_interact"] = []

if "graph" not in st.session_state:
    st.session_state["graph"] = init_graph_rag_pdf(temp_file_path, openai_api_key)

st.session_state["messages_welcome"] = [{"role": "ai",
                                "content": "你好，我是你的AI助手，我可以根据上传的PDF文件，为你解答相关的问题。\n\n请问有什么可以帮到你吗？"}]
for message in st.session_state["messages_welcome"]:
    st.chat_message(message["role"]).write(message["content"])

question = st.chat_input()

if question and uploaded_file:
    if not openai_api_key:
        st.info("请先输入OpenAI API密钥")
        st.stop()
    else:
        with st.spinner("AI正在思考中，请稍等..."):
            result = st.session_state["graph"].invoke({"messages": [{"role": "user", "content": question}]},
                                                       config=config)
            context_ls = result["messages"][-2].content.split("\n\n")
            context_ls = [context.split('Content:')[-1] for context in context_ls]
            response = result["messages"][-1].content

            with st.expander("PDF的相关内容如下 📄"):
                for i, context in enumerate(context_ls):
                    st.write(f"相关内容[{i+1}]: {context}\n\n")            
            if "</think>" in response:
                think, response = separate_think_answer(response)
                with st.expander("AI的思考过程如下 👀"):
                        st.write(think)

        st.session_state["messages_interact"].append({"role": "user", "content": question})
        st.session_state["messages_interact"].append({"role": "ai", "content": response})
        for message in st.session_state["messages_interact"]:
            st.chat_message(message["role"]).write(message["content"])

st.divider()

clear = st.button("清空对话历史")
if clear:
    st.session_state.clear()
