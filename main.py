import streamlit as st 
import time 

st.write("Hello World!")
st.button("click me plz")
st.text_input("Write your API KEY", max_chars=20)
st.feedback("faces")

with st.sidebar:
    st.badge("Badge 1")

tab1, tab2, tab3 = st.tabs(["Agent","Chat","Output"])

with tab1:
    st.header("Agent 1")
with tab2:
    st.header("Agent 2")
with tab3:
    st.header("Agent 3")


with st.chat_message("ai"):  #해당 괄호안에 뭘 넣냐에 따라 누가 말하는것같은지가 아이콘이 달라짐 
    st.text("Hello")
    with st.status("Agent is using tool") as status: # 생각하고 있는것처럼 표시해줌
        time.sleep(1) 
        status.update(label="Agent is searching the web.....")
        time.sleep(2)
        status.update(label="Agnet is reading the page.....")
        time.sleep(3)
        status.update(state="complete")

with st.chat_message("user"):  
    st.text("Hello")

st.chat_input("Write a message for the assistant.", accept_file=True)