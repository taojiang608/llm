"""
Write a wrapper GPT chatbot application using our Azure openai account and streamlit framework
"""

import os
import streamlit as st
#from openai import OpenAI
from openai import AzureOpenAI
from streamlit_chat import message

# Define a function to generate a response from ChatGPT using the “create” endpoint of OpenAI.
def api_calling(prompt):
    #client = OpenAI(
    client = AzureOpenAI(
        api_key=os.environ['AZURE_OPENAI_API_KEY'], 
        api_version="2023-07-01-preview",
        azure_endpoint="https://pd-dse-ai.openai.azure.com",
    )
    completions = client.completions.create(
        model='gpt4dse',
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    message = completions.choices[0].text
    return message

# create the header for the streamlit application and we are defining the user_input and openai_response in 
# the session_state.
st.title("ChatGPT ChatBot With Streamlit and OpenAI")
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = []
 
if 'openai_response' not in st.session_state:
    st.session_state['openai_response'] = []
 
def get_text():
    input_text = st.text_input("write here", key="input")
    return input_text
 
user_input = get_text()
 
if user_input:
    output = api_calling(user_input)
    output = output.lstrip("\n")
 
    # Store the output
    st.session_state.openai_response.append(user_input)
    st.session_state.user_input.append(output)    

# using the message functions to show the previous chat of the user on the right side and the chatbot response on 
# the left side. It shows the latest chat first. The query input by the user is shown with a different avatar.
message_history = st.empty()

if st.session_state['user_input']:
	for i in range(len(st.session_state['user_input']) - 1, -1, -1):
		# This function displays user input
		message(st.session_state["user_input"][i],
				key=str(i), avatar_style="icons")
		# This function displays OpenAI response
		message(st.session_state['openai_response'][i],
				avatar_style="miniavs", is_user=True
				, key=str(i) + 'data_by_user')
