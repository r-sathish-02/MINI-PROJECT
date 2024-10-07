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
    st.write(" ")

# Main App
st.sidebar.title("Knowledge Navigator")
menu = st.sidebar.selectbox(
    "Choose a Feature",
    ["Home", "MCQ Generator", "PDF Q&A System", "CSV Visualization", "Research Bot", "Q&A Evaluator",
     "Study Plan Generator", "Interactive Quiz", "Concept Map Generator", "Topic Summary Generator"]
)

# Home page function
def home_page():
    st.title("Welcome to Knowledge Navigator")
    st.write("""
    Knowledge Navigator is your AI-powered educational assistant! It provides a range of tools for both students and teachers, 
    including MCQ generation, PDF-based Q&A generation, CSV data visualization, and personalized study plans.
    Here’s what you can do with Knowledge Navigator:
    - Generate MCQs from any text for effective revision.
    - Upload PDFs and get automated Q&A.
    - Visualize CSV data files easily.
    - Use the Research Bot to get answers to your academic queries.
    - Create personalized study plans and take interactive quizzes.
    """)
    st.write("Navigate to different features using the sidebar to explore the various functionalities.")

# Function to generate MCQs
def generate_mcqs(text, num_mcqs, subject):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
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
    reader = PyPDF2.PdfReader(pdf_file)
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
    df = pd.read_csv(csv_file)
    st.write(df)
    numeric_columns = df.select_dtypes(include=["float", "int"]).columns.tolist()
    if numeric_columns:
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

# Function to generate personalized study plan
def study_plan_generator():
    st.title("Personalized Study Plan Generator")
    name = st.text_input("Name")
    study_hours = st.slider("How many hours can you study per day?", 1, 12, 3)
    subjects = st.multiselect("Select the subjects you want to study", 
                              ["Math", "Science", "History", "Language", "Arts"])
    deadline = st.date_input("Select the date of your next exam")

    if st.button("Generate Study Plan"):
        if not name or not subjects:
            st.error("Please enter all the details!")
        else:
            st.write(f"Study plan for {name} generated!")
            st.write(f"Study {study_hours} hours every day:")
            for subject in subjects:
                st.write(f"- {subject}: {study_hours / len(subjects):.2f} hours per day")

# Function for interactive quiz
def interactive_quiz():
    st.title("Interactive Quiz")
    questions = [
        {"question": "What is the capital of France?", "options": ["Paris", "Berlin", "Madrid", "Rome"], "correct": "Paris"},
        {"question": "Who wrote 'Hamlet'?", "options": ["Shakespeare", "Hemingway", "Tolkien", "Austen"], "correct": "Shakespeare"}
    ]
    
    score = 0
    for idx, q in enumerate(questions):
        st.subheader(f"Question {idx + 1}: {q['question']}")
        answer = st.radio(f"Options for question {idx + 1}", q["options"])
        if st.button(f"Submit Answer for Question {idx + 1}"):
            if answer == q['correct']:
                st.success("Correct!")
                score += 1
            else:
                st.error(f"Wrong! Correct answer is {q['correct']}")
    st.write(f"Your total score: {score}/{len(questions)}")

# Function for concept map generation
def concept_map_generator():
    import networkx as nx
    st.title("Concept Map Generator")
    concept = st.text_input("Enter a Topic")
    subtopics = st.text_area("Enter Subtopics (comma-separated)")
    if st.button("Generate Concept Map"):
        if not concept or not subtopics:
            st.error("Please enter both topic and subtopics.")
        else:
            G = nx.Graph()
            subtopics_list = subtopics.split(',')
            G.add_node(concept)
            for sub in subtopics_list:
                G.add_edge(concept, sub.strip())
            nx.draw(G, with_labels=True)
            st.pyplot()

# Function to summarize text
def topic_summary_generator():
    st.title("Topic Summary Generator")
    text = st.text_area("Enter text for summary")
    if st.button("Generate Summary"):
        if text:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an expert summarizer."},
                        {"role": "user", "content": f"Summarize the following text: {text}"}
                    ]
                )
                st.write(response.choices[0].message['content'])
            except Exception as e:
                st.error(f"Error: {e}")

# Choose feature based on sidebar menu
if menu == "Home":
    home_page()
elif menu == "MCQ Generator":
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
elif menu == "Study Plan Generator":
    study_plan_generator()
elif menu == "Interactive Quiz":
    interactive_quiz()
elif menu == "Concept Map Generator":
    concept_map_generator()
elif menu == "Topic Summary Generator":
    topic_summary_generator()
