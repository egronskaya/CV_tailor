import streamlit as st
import os
from dotenv import load_dotenv
from src.cv_processor import CVProcessor
from src.letter_generator import LetterGenerator
from src.document_maker import DocumentMaker

# Load environment variables
load_dotenv()

# Configure Streamlit
st.set_page_config(
    page_title="CV & Cover Letter Tailor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

if os.getenv('DEBUG_MODE', 'false').lower() == 'true':
    st.write("Debug mode enabled")

# Initialize session state
if 'generated_cv' not in st.session_state:
    st.session_state.generated_cv = None
if 'cover_letters' not in st.session_state:
    st.session_state.cover_letters = None
if 'job_ad' not in st.session_state:
    st.session_state.job_ad = None
if 'skills' not in st.session_state:
    st.session_state.skills = None

# Initialize processors
cv_processor = CVProcessor()
letter_generator = LetterGenerator()
doc_maker = DocumentMaker()

def view_and_edit_documents():
    if not st.session_state.generated_cv or not st.session_state.cover_letters:
        st.warning("No documents have been generated yet. Please generate documents first.")
        return

    st.subheader("Review and Edit Documents")
    
    # CV Review
    st.write("### CV Content")
    cv_content = st.session_state.generated_cv['content']
    edited_cv = st.text_area("Edit CV", cv_content, height=400)
    
    if edited_cv != cv_content:
        if st.button("Update CV"):
            with st.spinner("Updating CV..."):
                # Update CV with edited content
                st.session_state.generated_cv['content'] = edited_cv
                cv_docx, cv_pdf = doc_maker.create_cv_documents(st.session_state.generated_cv)
                st.success("CV updated successfully!")
                
                # Show download buttons for updated CV
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "Download Updated CV (DOCX)",
                        cv_docx,
                        "updated_cv.docx",
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                with col2:
                    st.download_button(
                        "Download Updated CV (PDF)",
                        cv_pdf,
                        "updated_cv.pdf",
                        "application/pdf"
                    )
    
    # Cover Letters Review
    st.write("### Cover Letters")
    for i, letter in enumerate(st.session_state.cover_letters, 1):
        st.write(f"#### Cover Letter {i}")
        edited_letter = st.text_area(
            f"Edit Cover Letter {i}",
            letter['content'],
            height=300,
            key=f"letter_{i}"
        )
        
        if edited_letter != letter['content']:
            if st.button(f"Update Cover Letter {i}"):
                with st.spinner(f"Updating Cover Letter {i}..."):
                    # Update letter with edited content
                    letter['content'] = edited_letter
                    docx, pdf = doc_maker.create_letter_documents([letter])[0]
                    st.success(f"Cover Letter {i} updated successfully!")
                    
                    # Show download buttons for updated letter
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            f"Download Updated Cover Letter {i} (DOCX)",
                            docx,
                            f"updated_cover_letter_{i}.docx",
                            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    with col2:
                        st.download_button(
                            f"Download Updated Cover Letter {i} (PDF)",
                            pdf,
                            f"updated_cover_letter_{i}.pdf",
                            "application/pdf"
                        )
    
    # Regenerate options
    st.write("### Regenerate Documents")
    
    if st.button("Regenerate CV"):
        with st.spinner("Regenerating CV..."):
            st.session_state.generated_cv = cv_processor.tailor_cv(st.session_state.job_ad)
            st.success("CV regenerated! Check the CV content above.")
            st.experimental_rerun()
    
    if st.button("Regenerate All Cover Letters"):
        with st.spinner("Regenerating cover letters..."):
            st.session_state.cover_letters = letter_generator.generate_letters(st.session_state.job_ad, 3)
            st.success("Cover letters regenerated! Check the content above.")
            st.experimental_rerun()

def main():
    st.title("CV & Cover Letter Tailor")
    
    # Create tabs for different functionalities
    tab1, tab2 = st.tabs(["Generate Documents", "Review & Edit"])
    
    with tab1:
        st.write("Upload your job advertisement and get tailored CV and cover letters")
        
        # Job Advertisement Input
        job_ad = st.text_area(
            "Paste the job advertisement here",
            height=300,
            help="Paste the complete job posting text here",
            value=st.session_state.job_ad if st.session_state.job_ad else ""
        )

    if st.button("Generate Documents") and job_ad:
        with st.spinner("Analyzing job advertisement and generating documents..."):
            try:
                # Store job ad in session state
                st.session_state.job_ad = job_ad
                
                # Process the job ad and generate documents
                st.session_state.skills = cv_processor.extract_skills(job_ad)
                st.session_state.generated_cv = cv_processor.tailor_cv(job_ad)
                st.session_state.cover_letters = letter_generator.generate_letters(job_ad, 3)
                
                # Create documents
                cv_docx, cv_pdf = doc_maker.create_cv_documents(st.session_state.generated_cv)
                letter_docs = doc_maker.create_letter_documents(st.session_state.cover_letters)
                
                # Display results
                st.success("Documents generated successfully!")
                
                # Display extracted skills
                st.subheader("Extracted Skills")
                st.write(", ".join(st.session_state.skills))
                
                # Create download buttons for documents
                st.subheader("Download Documents")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "Download CV (DOCX)",
                        cv_docx,
                        "tailored_cv.docx",
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                with col2:
                    st.download_button(
                        "Download CV (PDF)",
                        cv_pdf,
                        "tailored_cv.pdf",
                        "application/pdf"
                    )
                
                # Cover letter downloads
                st.subheader("Cover Letters")
                for i, (docx, pdf) in enumerate(letter_docs, 1):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            f"Download Cover Letter {i} (DOCX)",
                            docx,
                            f"cover_letter_{i}.docx",
                            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    with col2:
                        st.download_button(
                            f"Download Cover Letter {i} (PDF)",
                            pdf,
                            f"cover_letter_{i}.pdf",
                            "application/pdf"
                        )
                        
                st.success("Switch to the 'Review & Edit' tab to make any changes to the generated documents.")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    with tab2:
        view_and_edit_documents()

if __name__ == "__main__":
    main()