import streamlit as st
import openai
from dotenv import load_dotenv
import os
import PyPDF2
import pandas as pd
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.error("OpenAI API key not found. Please check the .env file.")
else:
    st.write("OpenAI API key loaded successfully")

# Main App
st.sidebar.title("Knowledge Navigator")
menu = st.sidebar.selectbox(
    "Choose a Feature",
    ["MCQ Generator", "PDF Q&A System", "CSV Visualization", "Research Bot", "Q&A Evaluator"]
)

# Function to generate MCQs
def generate_mcqs(text, num_mcqs, subject):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert MCQ maker."},
                {"role": "user", "content": f"Generate {num_mcqs} MCQs on {subject} based on the following text: {text}"}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to handle PDF Q&A
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)  # Updated to PdfReader
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text


def generate_qa_from_pdf(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert question generator."},
                {"role": "user", "content": f"Generate Q&A based on the following text: {text}"}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to handle CSV Visualization
def visualize_csv(csv_file):
    # Load the CSV into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Display the DataFrame
    st.write(df)

    # Select only the numerical columns for visualization
    numeric_columns = df.select_dtypes(include=["float", "int"]).columns.tolist()

    if numeric_columns:
        # Let the user select which numerical columns they want to plot
        selected_columns = st.multiselect("Select columns to visualize", numeric_columns, default=numeric_columns)

        if selected_columns:
            st.line_chart(df[selected_columns])
        else:
            st.warning("Please select at least one numerical column.")
    else:
        st.error("No numerical columns found for visualization.")

# Function to simulate Research Bot
def research_bot_query(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a research assistant."},
                {"role": "user", "content": f"Answer this research question: {query}"}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function for Q&A Evaluator (Placeholder)
def qa_evaluator(file):
    st.write("Q&A Evaluator is under construction.")

# Choose feature based on sidebar menu
if menu == "MCQ Generator":
    st.header("Generate MCQs")
    text_input = st.text_area("Enter text for MCQ generation:")
    num_mcqs = st.slider("Number of MCQs", 1, 10, 5)
    subject = st.text_input("Subject")

    if st.button("Generate MCQs"):
        if text_input and subject:
            mcqs = generate_mcqs(text_input, num_mcqs, subject)
            st.subheader("Generated MCQs")
            st.write(mcqs)
        else:
            st.warning("Please enter text and subject.")

elif menu == "PDF Q&A System":
    st.header("Upload PDF for Q&A Generation")
    pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])

    if pdf_file:
        text = extract_text_from_pdf(pdf_file)
        st.subheader("Generated Questions and Answers")
        qa = generate_qa_from_pdf(text)
        st.write(qa)

elif menu == "CSV Visualization":
    st.header("Upload CSV for Data Visualization")
    csv_file = st.file_uploader("Upload CSV file", type=["csv"])

    if csv_file:
        st.subheader("Data Visualization")
        visualize_csv(csv_file)

elif menu == "Research Bot":
    st.header("Research Bot")
    query = st.text_input("Enter your research question:")

    if st.button("Get Research Answer"):
        if query:
            answer = research_bot_query(query)
            st.subheader("Research Bot Answer")
            st.write(answer)

elif menu == "Q&A Evaluator":
    st.header("Upload a file for Q&A Evaluation (PDF or Image)")
    file = st.file_uploader("Upload PDF or Image", type=["pdf", "jpg", "png"])

    if file:
        st.subheader("Evaluation Results")
        qa_evaluator(file)
