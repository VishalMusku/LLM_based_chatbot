from PDFExtractor import extract_text_save_to_file
from TextProcessor import read_entire_text, estimate_token_count, split_text_into_chunks_at_page_breaks, erase_file_content
from OpenAIHelper import generate_response
import re
from openai import OpenAI
import streamlit as st
import tempfile
from dotenv import load_dotenv
import os
import time
import glob





def main():
    
    st.set_page_config(
    page_title="PDF Search Chatbot",
    page_icon=":books:",
    layout="centered",
    initial_sidebar_state="expanded",)

    with st.sidebar:
        st.title("Menu")
        
        uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type="pdf")

        if uploaded_files:
            # Create source folder if it doesn't exist
            source_folder = os.path.join(os.getcwd(), "source")
            os.makedirs(source_folder, exist_ok=True)

            # Copy uploaded files to source folder
            for file in uploaded_files:
                file_path = os.path.join(source_folder, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getvalue())
            

    st.title("📚 Chat with your PDF")

    user_question = st.text_input("Enter your question :")

    if user_question:
        for filename in os.listdir(source_folder):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(source_folder, filename)
                pdf_text = extract_text_save_to_file(pdf_path, "context.txt")
                
                time.sleep(50)
                
                entire_text = read_entire_text("context.txt")

                token_count = estimate_token_count(entire_text)
                
                # Only chunk the text if the token count exceeds 92,000, based on OpenAI documentation suggestions
                if token_count > 92000:
                    # Split the text into chunks at page breaks if over the token limit
                    text_chunks = split_text_into_chunks_at_page_breaks(entire_text, 4)
                else:
                    # Use the entire text as a single chunk if under the token limit
                    text_chunks = [entire_text]
                    
                # Initialize a list to collect responses for each chunk
                responses = []
                # Generate and collect a response for each text chunk
                for chunk in text_chunks:
                    response = generate_response(chunk, user_question)
                    responses.append(response)
                
                # Combine and print the collected responses
                st.write(f'Response from {filename}\n : ')

                st.write( ' '.join(responses))        
                
                erase_file_content("context.txt")     
                                
                st.write("******************************")
        
        pdf_files_to_remove = glob.glob(os.path.join(source_folder, "*.pdf"))
        
        for pdf_file in pdf_files_to_remove:
            os.remove(pdf_file)
        

if __name__ == "__main__":
    main()
