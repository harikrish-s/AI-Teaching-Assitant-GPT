import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import streamlit as st
st.title("AI Teaching Assistant GPT")
flag = 0
api_key = st.text_input("Enter your OpenAI API Key: ")
text = st.text_input("Enter YouTube Video URL: ")
final = ""
if len(text)>0:
    st.video(text)
    yt = YouTubeTranscriptApi.get_transcript(text.split(sep='/')[-1], languages=['en'])
    if len(yt) > 0:
        for i in yt:
            final += i['text'] + ' '
        # st.header('Translated Transcript: ')
        # st.write(final)
        flag = 1
if(flag==1):
    first_prompt = "I will give you a transcription of a video lecture, you have to understand it and answer the questions I ask from that.Here is the transcription: " + final

def show_messages(text):
    messages_str = [
        f"{_['role']}: {_['content']}" for _ in st.session_state["messages"][1:]
    ]
    text.text_area("Messages", value=str("\n".join(messages_str)), height=400)
try:
    openai.api_key = api_key
    BASE_PROMPT = [{"role": "system", "content": first_prompt}]

    if "messages" not in st.session_state:
        st.session_state["messages"] = BASE_PROMPT

    text = st.empty()
    show_messages(text)

    prompt = st.text_input("Prompt")
    col1, col2 = st.columns((1,5))
    if col1.button("Send"):
        with st.spinner("Generating response..."):
            st.session_state["messages"] += [{"role": "user", "content": prompt}]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=st.session_state["messages"]
            )
            message_response = response["choices"][0]["message"]["content"]
            st.session_state["messages"] += [
                {"role": "system", "content": message_response}
            ]
            show_messages(text)

    if col2.button("Clear"):
        st.session_state["messages"] = BASE_PROMPT
        show_messages(text)
except:
    pass