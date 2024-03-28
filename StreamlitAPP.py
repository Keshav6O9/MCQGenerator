import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file
import streamlit as st
from src.mcq_generator.mcq_generator import generate_evaluate_chain
from src.mcq_generator.logger import logging
import datetime

# Get the current date and time
now = datetime.datetime.now()

# Convert the datetime object to a string
date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

#loading json file
with open('E:/ProexeLancers/GenAI_LLMS/MCQGenerator/Response.json','r') as file:
    RESPONSE_JSON = json.load(file)

with st.form("user_inputs"):
    #file upload
    uploaded_file = st.file_uploader("Upload a PDF or txt file")

    #input fields 
    mcq_count = st.number_input("No. of MCQs",min_value=3,max_value=20)

    #Subject
    subject = st.text_input("Insert Subject",max_chars=20)
    tone = st.text_input("Complexity level of Questions",max_chars=20,placeholder="Simple")

    button=st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(uploaded_file)
                response = generate_evaluate_chain(
                    {
                        "text":text,
                        "number":mcq_count,
                        "subject":subject,
                        "tone":tone,
                        "response_json":json.dumps(RESPONSE_JSON)
                    })
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
            else:
                if isinstance(response,dict):
                    quiz = response.get("quiz",None)
                    if quiz is not None:

                        filename = "mcqs"+ now.strftime("%Y-%m-%d-%H-%M")
                        with open(filename, 'w') as f:
                            f.write(response.get('quiz'))  
                        st.text_area(label="Review",value=response["review"])
                        st.text_area(label="Quiz",value=response["quiz"])
                    else:
                        st.error("Error in the data")
                else:
                    st.write(response)

