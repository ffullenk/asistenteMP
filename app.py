import streamlit as st
from judini.codegpt import CodeGPTPlus
import time
import os 
import boto3

#Connect with codegpt
# Extrayendo valores
api_key = os.getenv('CODEGPT_API_KEY')
agent_id = os.getenv('CODEGPT_AGENT_ID')
org_id = os.getenv('CODEGPT_ORG_ID')

st.set_page_config(layout="centered")

st.title("Asistente virtual Lizilib")
st.header("Bienvenido/a a nuestra IA para conocer como licitar en Mercado Público")
st.markdown("---")

# init chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("¿Cómo te puedo ayudar hoy?"):
    # user message history
    st.session_state.messages.append({"role":"user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Obteniendo resultados..."):
            message_placeholder = st.empty()
            full_response = ""


            # connect CodeGPT SDK
            codegpt = CodeGPTPlus(api_key=api_key, org_id=org_id)
            messages = st.session_state.messages

            response_completion = codegpt.chat_completion(agent_id=agent_id, messages=messages, stream=True)

            for response in response_completion:
                time.sleep(0.05)
                full_response += (response or "")
                message_placeholder.markdown(full_response + "|")

            message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role":"assistant", "content": full_response})
