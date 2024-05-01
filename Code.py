import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Generative AI
genai.configure(
    api_key=API_KEY
)

# Initialize Generative Model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
instruction = "In this chat explain as if you are explaining it to a five-year-old child."


# Function to check syntax based on language
def check_syntax(code, language):
    if language.lower() == "python":
        # Placeholder syntax analysis for Python
        # Check if the code contains at least one print statement
        if "print(" in code:
            return True
        else:
            return False
    elif language.lower() == "java":
        # Placeholder syntax analysis for Java
        # Check if the code contains at least one System.out.println statement
        if "System.out.println(" in code:
            return True
        else:
            return False
    elif language.lower() == "c":
        # Placeholder syntax analysis for C
        # Check if the code contains at least one printf statement
        if "printf(" in code:
            return True
        else:
            return False
    else:
        return False


# Streamlit App
st.title("Generative AI Chat")

# Password input
password = st.text_input("Enter Password:", type="password")

if password == "123456":
    st.success("Password correct. You may proceed.")
    # User input after correct password
    language = st.selectbox("Select Language", ["Java", "Python", "C"])

    prompt = st.text_input(f"{language} Prompt:", key=f"{language}_prompt")

    if st.button("Ask"):
        if prompt.strip() != '':
            if check_syntax(prompt, language):
                try:
                    # Send user's prompt to the model
                    response = chat.send_message(prompt)

                    # Display model's response
                    st.write("Bot:", response.text)
                except genai.generation_types.StopCandidateException:
                    st.write("Sorry, I didn't understand that. Can you try asking in a different way?")
            else:
                st.write("Invalid Syntax for the selected language.")
else:
    st.error("Incorrect Password. Please try again.")
