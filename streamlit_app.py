import streamlit as st
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from zhipuai_embedding import ZhipuAIEmbeddings
from langchain_community.vectorstores import Chroma
from zhipuai_llm import ZhipuaiLLM

ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY")
if not ZHIPUAI_API_KEY:
    raise ValueError("缺少 ZHIPUAI_API_KEY 环境变量，请在 Codespaces Secrets 中设置")

def get_retriever():
    # 定义 Embeddings
    embedding = ZhipuAIEmbeddings()
    # 向量数据库持久化路径
    persist_directory = 'data_base/vector_db/chroma'
    # 加载数据库
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding
    )
    return vectordb.as_retriever()

def combine_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs["context"])

def get_qa_history_chain():
    retriever = get_retriever()
    llm = ZhipuaiLLM(api_key=ZHIPUAI_API_KEY,temperature=0.1,model_name='glm-4-plus')
    condense_question_system_template = (
        "请根据聊天记录总结用户最近的问题，"
        "如果没有多余的聊天记录则返回用户的问题。"
    )
    condense_question_prompt = ChatPromptTemplate([
            ("system", condense_question_system_template),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ])

    retrieve_docs = RunnableBranch(
        (lambda x: not x.get("chat_history", False), (lambda x: x["input"]) | retriever, ),
        condense_question_prompt | llm | StrOutputParser() | retriever,
    )

    system_prompt = (
        "你是一个问答任务的助手。 "
        "请使用检索到的上下文片段回答这个问题。 "
        "如果你不知道答案就说不知道。 "
        "请使用简洁的话语回答用户。"
        "\n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )
    qa_chain = (
        RunnablePassthrough().assign(context=combine_docs)
        | qa_prompt
        | llm
        | StrOutputParser()
    )

    qa_history_chain = RunnablePassthrough().assign(
        context = retrieve_docs, 
        ).assign(answer=qa_chain)
    return qa_history_chain

def gen_response(chain, input, chat_history):
    response = chain.stream({
        "input": input,
        "chat_history": chat_history
    })
    for res in response:
        if "answer" in res.keys():
            yield res["answer"]

# Streamlit 应用程序界面
def main():
    st.markdown('### 🦜🔗 动手学大模型应用开发')

    # 初始化对话历史
    if "messages" not in st.session_state:
        st.session_state.messages = [
            ("ai", "我是一个问答任务的助手，专门帮助用户解答问题。请问有什么问题我可以帮您解答？")
        ]
    if "qa_history_chain" not in st.session_state:
        st.session_state.qa_history_chain = get_qa_history_chain()

    # 改成不固定高度，让内容自然增长
    messages = st.container()

    # 显示历史消息
    for role, text in st.session_state.messages:
        display_role = "user" if role == "human" else "assistant"
        with messages.chat_message(display_role):
            st.write(text)

    # 处理用户输入
    if prompt := st.chat_input("Say something"):
        st.session_state.messages.append(("human", prompt))
        with messages.chat_message("user"):
            st.write(prompt)

        answer_gen = gen_response(
            chain=st.session_state.qa_history_chain,
            input=prompt,
            chat_history=st.session_state.messages
        )

        assistant_text = ""
        with messages.chat_message("assistant"):
            placeholder = st.empty()
            for chunk in answer_gen:
                assistant_text += str(chunk)
                placeholder.write(assistant_text)

        st.session_state.messages.append(("ai", assistant_text))

    # 滚动到页面底部，确保显示最新消息
    st.markdown(
        """
        <script>
        window.scrollTo(0, document.body.scrollHeight);
        </script>
        """,
        unsafe_allow_html=True
    )



if __name__ == "__main__":
    main()
