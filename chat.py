from openai import OpenAI
import streamlit as st
import time

#file_id = "file-MHkw0ufVp5RoEP5afk2P7F4x"
assistant_id = "asst_WollgsaCkywwYXr08HRU8pd1"


with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", value="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", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    
    client = OpenAI(api_key=openai_api_key)
    thread_id = st.text_input("Thread ID")
    thread_btn = st.button("Create a new thread")
    
    if thread_btn:
        thread = client.beta.threads.create()
        thread_id = thread.id
        
        st.subheader(f"{thread_id}", divider="rainbow")
        st.info("thread가 생성되었습니다.")
    
st.title("🎈 2024 축제 Chatbot")
#st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "원하시는 축제 유형/이름을 입력해주세요"}]
    #메세지가 없을때 띄우는 텍스트
    
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    
    if not thread_id:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()    

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    response = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=prompt,
        )
    print(response)
    
    run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id
    )
    print(run)
    
    run_id = run.id
    
    while True:
        run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,       run_id = run_id
        )
        if run.status == "completed":
            break
        else:
            time.sleep(2)
        print(run)
        
    thread_messages = client.beta.threads.messages.list(thread_id)
    print(thread_messages.data)
    
    msg = thread_messages.data[0].content[0].text.value
    print(msg)
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    
    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # msg = response.choices[0].message.content
    # st.session_state.messages.append({"role": "assistant", "content": msg})
    # st.chat_message("assistant").write(msg)