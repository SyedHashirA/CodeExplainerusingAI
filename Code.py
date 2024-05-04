import os
import re
import streamlit as st
import matplotlib.pyplot as plt
import google.generativeai as genai
from dotenv import load_dotenv

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
instruction = "In this chat explain the given code or the line of code in detail, explain it as a five year old "


# Function to check syntax based on language
def check_syntax(code, language):
    if language.lower() == "python":
        # Placeholder syntax analysis for Python
        # Check if the code contains 'def' indicating a function definition
        if 'def ' in code:
            return True
        # Check if the code contains 'import' indicating module imports
        elif 'import ' in code:
            return True
        elif 'print(' in code:
            return True
        # Check for a main function call if it's a script
        elif '__name__ == "__main__"' in code and 'def main():' in code:
            return True
        else:
            return False
    elif language.lower() == "java":
        # Placeholder syntax analysis for Java
        # Check if the code contains 'class ' indicating a class definition
        if 'class ' in code:
            return True
        # Check if the code contains 'public static void main' indicating a main method
        elif 'public static void main' in code:
            return True
        elif 'System.out.println(' in code:
            return True
        elif 'System.out.print(' in code:
            return True
        else:
            return False
    elif language.lower() == "c":
        # Placeholder syntax analysis for C
        # Check if the code contains '#include' indicating header file inclusion
        if '#include' in code:
            return True
        # Check if the code contains 'int main()' indicating the main function
        elif 'int main()' in code:
            return True
        elif 'printf(' in code:
            return True
        else:
            return False
    else:
        return False


# Function to explain code in tabular format
def explain_tabular(code):
    # Define regular expressions for different components of code
    method_call_regex = r'\b[a-zA-Z_]\w*\([^()]*\)'
    variable_regex = r'\b[a-zA-Z_]\w*\b'
    string_literal_regex = r'"[^"]*"'
    numeric_literal_regex = r'\b\d+\b'
    comment_regex = r'\/\/.*|\/\*[\s\S]*?\*\/'

    # Find all occurrences of different components in the code
    method_calls = re.findall(method_call_regex, code)
    variables = re.findall(variable_regex, code)
    string_literals = re.findall(string_literal_regex, code)
    numeric_literals = re.findall(numeric_literal_regex, code)
    comments = re.findall(comment_regex, code)

    # Count occurrences
    counts = {
        'Variables': len(variables),
        'Method Calls': len(method_calls),
        'String Literals': len(string_literals),
        'Numeric Literals': len(numeric_literals),
        'Comments': len(comments)
    }

    # Remove items with 0 occurrences to avoid label overlap
    counts = {k: v for k, v in counts.items() if v != 0}

    # Create lists to hold the words and their explanations
    word_list = method_calls + variables + string_literals + numeric_literals + comments
    explanation_list = ["Method Call" for _ in method_calls] + ["Variable" for _ in variables] + ["String Literal" for _
                                                                                                  in
                                                                                                  string_literals] + [
                           "Numeric Literal" for _ in numeric_literals] + ["Comment" for _ in comments]

    # Create a dictionary to hold the data
    table_data = {
        'Word': word_list,
        'Explanation': explanation_list
    }

    return counts, table_data


# Function to explain code and create a pie chart
def explain_and_plot(code):
    counts, table_data = explain_tabular(code)

    # Plotting the pie chart
    labels = counts.keys()
    sizes = counts.values()

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_facecolor('black')  # Set background color to black

    # Add comma between labels with more than one item and remove it for single item
    labels = [f"{label}," if size != 1 else label for label, size in zip(labels, sizes)]

    st.table(table_data)
    st.pyplot(fig)


# Streamlit App
st.title("Code Explainer Chatbot")

# Password input
password = st.text_input("Enter Password:", type="password")

if password == "123456":
    st.success("Password correct. You may proceed.")
    # User input after correct password
    language = st.selectbox("Select Language", ["Java", "Python", "C"])
    answer_type = st.selectbox("Select Answer Type", ["Elaborated Answer", "Tabular Answer"])

    prompt = st.text_input(f"{language} Prompt:", key=f"{language}_prompt")

    if st.button("Ask"):
        if prompt.strip() != '':
            if check_syntax(prompt, language):
                try:
                    # Send user's prompt to the model
                    response = chat.send_message(prompt)

                    # Display response based on selected answer type
                    if answer_type == "Elaborated Answer":
                        st.write("Bot:", response.text)
                    else:
                        explain_and_plot(prompt)
                except genai.generation_types.StopCandidateException:
                    st.write("Sorry, I didn't understand that. Can you try asking in a different way?")
            else:
                st.write("Invalid Syntax for the selected language.")
else:
    st.error("Incorrect Password. Please try again.")
