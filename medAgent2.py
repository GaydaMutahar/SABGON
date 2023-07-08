
import cohere
import streamlit as st
from serpapi import GoogleSearch
import requests
from PIL import Image
from io import BytesIO
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain.tools import DuckDuckGoSearchRun 

from typing import List, Union
#from langchain.schema import AgentAction, AgentFinish
import re
import langchain


#st.set_page_config(layout="wide") 
col1, col2, col3 = st.columns(3 , gap="large")
with col1:
    st.title(":blue[Medical  Advisor ]")
with col2:
    image = Image.open('im.jpeg')
    st.image(
        image,
        width=120,
    )

co = cohere.Client('GGM7uhPK5DTgPtMweS0IbHK2rkxLBmAJ2cmoGA57')
prompt1 = st.text_input('What are the symptoms of the patient?  (*Please type the correct spelling of the symptom**)')
with open('symptoms_list.txt', 'r') as file:
    symptoms = [line.strip().lower() for line in file]
    print("symptoms", symptoms)
if prompt1:
    if any(symptom in prompt1.lower() for symptom in symptoms):
        response = co.generate(
            model = 'command-nightly', #xlarge #medium #small
            prompt = f"user: Suggest prescription medications for these symptoms: {prompt1}\nTLDR:", # 
            max_tokens=200,
            temperature=0.9,
            k=0,
            p=0.75,
            frequency_penalty=0,
            presence_penalty=0,
            stop_sequences=[],
            return_likelihoods='NONE'
        )

        text = format(response.generations[0].text)
        if st.button('Find a medicine'):
             st.write('Prescription medications: %s' %text)


prompt2 = st.text_input('What are the heatlh conditions that conflict with this medicine ? (*Please type the correct spelling of the medicine**) ')
if prompt2:
                     response = co.generate(
                            model = 'command-nightly', 
                            prompt = f"user: Suggest possible health conditions conflict these midications: {prompt2}\nTLDR:", # 
                            max_tokens=200,
                            temperature=0.9,
                            k=0,
                            p=0.75,
                            frequency_penalty=0,
                            presence_penalty=0,
                            stop_sequences=[],
                            return_likelihoods='NONE'
                        )
                     text2 = format(response.generations[0].text)
                     st.write('List of health conditions: %s' %text2)
                     print("Seconed prompt is done")


prompt3 = st.text_input('Ask me, if you have any general heatlh questions:')


if  prompt3:
    search2 = DuckDuckGoSearchRun()
    search_results = search2.run(f"site:webmd.com {prompt3}")
    st.write(search_results)

