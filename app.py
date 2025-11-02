import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from src.cv_processor import CVProcessor
from src.letter_generator import LetterGenerator
from src.document_maker import DocumentMaker

# Load environment variables
load_dotenv()

# Configure Streamlit
st.set_page_config(
    page_title="CV Tailor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    .stTextArea>div>div>textarea {
        background-color: #f8f9fa;
    }
    .success-message {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .warning-message {
        padding: 1rem;
        border-radius: 5px;
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeeba;
    }
    /* Header styling moved inline */
    .tab-content {
        padding: 2rem 0;
    }
    .section-header {
        color: #2C3E50;
        padding: 1rem 0;
        border-bottom: 2px solid #eee;
        margin-bottom: 1rem;
    }
    .skill-tag {
        background-color: #e9ecef;
        padding: 0.4rem 0.8rem;
        margin: 0.2rem;
        border-radius: 15px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

if os.getenv('DEBUG_MODE', 'false').lower() == 'true':
    st.warning("Debug mode enabled")

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
        st.markdown("""
            <div class='warning-message'>
                <h4>Welcome to the Editor!</h4>
                <p>No documents have been generated yet. To get started:</p>
                <ol>
                    <li>Go to the 'Generate Documents' tab</li>
                    <li>Paste your job advertisement</li>
                    <li>Click 'Generate Documents'</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("<div class='section-header'>Review and Edit Documents</div>", unsafe_allow_html=True)
    
    # CV Review with better organization
    st.markdown("### CV Content")
    st.markdown("Edit your CV content below. Changes will be reflected in both DOCX and PDF versions.")
    
    cv_content = st.session_state.generated_cv['content']
    edited_cv = st.text_area(
        "Your CV Content",
        cv_content,
        height=400,
        help="Make any necessary adjustments to your CV content here."
    )
    
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
    
    # Cover Letters Review with better organization
    st.markdown("### Cover Letters")
    st.markdown("Each version takes a different approach while maintaining your personal style. Edit any version below.")
    
    for i, letter in enumerate(st.session_state.cover_letters, 1):
        with st.expander(f"Cover Letter {i}", expanded=True):
            st.markdown(f"""
                **Version {i}** - Edit this cover letter to perfect its content.
                Any changes will be reflected in both DOCX and PDF versions.
            """)
            edited_letter = st.text_area(
                f"Cover Letter {i} Content",
                letter['content'],
                height=300,
                key=f"letter_{i}",
                help=f"Make any necessary adjustments to cover letter {i} here."
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
    
    # Regenerate options with better organization
    st.markdown("<div class='section-header'>Regenerate Documents</div>", unsafe_allow_html=True)
    st.markdown("""
        Not quite what you're looking for? You can regenerate documents while keeping the same job posting:
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Regenerate CV", help="Generate a new version of your CV using the same job posting"):
            with st.spinner("Creating a new version of your CV..."):
                st.session_state.generated_cv = asyncio.run(
                    cv_processor.tailor_cv(st.session_state.job_ad)
                )
                st.markdown("""
                    <div class='success-message'>
                        <h4>CV Regenerated!</h4>
                        <p>A new version of your CV has been created. Check the content above.</p>
                    </div>
                """, unsafe_allow_html=True)
                st.experimental_rerun()
    
    with col2:
        if st.button("Regenerate Cover Letters", help="Generate new versions of all cover letters"):
            with st.spinner("✨ Creating new versions of your cover letters..."):
                st.session_state.cover_letters = asyncio.run(
                    letter_generator.generate_letters(st.session_state.job_ad, 3)
                )
                st.markdown("""
                    <div class='success-message'>
                        <h4>✨ Cover Letters Regenerated!</h4>
                        <p>New versions of your cover letters have been created. Check the content above.</p>
                    </div>
                """, unsafe_allow_html=True)
                st.experimental_rerun()

def main():
    # Title and logo
    col1, col2 = st.columns([1, 4], gap="small")
    
    with col1:
        st.image("assets/logo.png", width=400, use_container_width=True)
    
    with col2:
        st.markdown("""
            <div style='margin-top: 0px; padding: 0;'>
                <h1 style='margin: 0; padding: 0; font-size: 2.5em;'>CV Tailor</h1>
                <p style='color: #666; font-size: 1.2em; margin-top: 10px; max-width: 500px;'>
                    Transform your CV to fit any job ad and generate personalized cover letters.
                    Keep your data private and secure throughout the process.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Create tabs with icons
    tab1, tab2 = st.tabs(["Generate Documents", "Review & Edit"])
    
    with tab1:
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        
        # Introduction with steps
        st.markdown("""
            ### How it works:
            1. Paste your job advertisement below
            2. AI analyzes the requirements
            3. Get your tailored CV and cover letters
            4. Review and fine-tune the results
        """)
        
        # Job Advertisement Input with better styling
        st.markdown("<div class='section-header'>Job Advertisement</div>", unsafe_allow_html=True)
        job_ad = st.text_area(
            "Paste the complete job posting here",
            height=300,
            help="The more detailed the job posting, the better the results will be.",
            value=st.session_state.job_ad if st.session_state.job_ad else "",
            placeholder="Paste the job advertisement here... Include the full description, requirements, and any other relevant information."
        )

    async def generate_documents(job_ad: str):
        """Asynchronously generate all documents"""
        # Extract skills and generate CV and cover letters in parallel
        skills_task = cv_processor.extract_skills(job_ad)
        cv_task = cv_processor.tailor_cv(job_ad)
        letters_task = letter_generator.generate_letters(job_ad, 3)
        
        # Wait for all tasks to complete
        skills, cv_content, letters = await asyncio.gather(
            skills_task, cv_task, letters_task
        )
        
        return skills, cv_content, letters

    if st.button("Generate Documents") and job_ad:
        with st.spinner("Analyzing job advertisement and generating documents..."):
            try:
                # Store job ad in session state
                st.session_state.job_ad = job_ad
                
                # Process the job ad and generate documents asynchronously
                skills, cv_content, letters = asyncio.run(generate_documents(job_ad))
                
                st.session_state.skills = skills
                st.session_state.generated_cv = cv_content
                st.session_state.cover_letters = letters
                
                # Create documents
                cv_docx, cv_pdf = doc_maker.create_cv_documents(st.session_state.generated_cv)
                letter_docs = doc_maker.create_letter_documents(st.session_state.cover_letters)
                
                # Display results
                st.success("Documents generated successfully!")
                
                # Display extracted skills with tags
                st.markdown("<div class='section-header'>Key Skills Identified</div>", unsafe_allow_html=True)
                skills_html = "".join([f"<span class='skill-tag'>{skill}</span>" for skill in st.session_state.skills])
                st.markdown(f"<div style='line-height: 3;'>{skills_html}</div>", unsafe_allow_html=True)
                
                # Create download buttons for documents with better organization
                st.markdown("<div class='section-header'>Generated Documents</div>", unsafe_allow_html=True)
                
                # CV downloads with icons and better styling
                st.markdown("#### Your Tailored CV")
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "Download CV (DOCX)",
                        cv_docx,
                        "tailored_cv.docx",
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                with col2:
                    st.download_button(
                        "Download CV (PDF)",
                        cv_pdf,
                        "tailored_cv.pdf",
                        "application/pdf",
                        use_container_width=True
                    )
                
                # Cover letter downloads with better organization
                st.markdown("#### Your Cover Letters")
                st.markdown("Each version has a different approach while maintaining your personal style.")
                
                for i, (docx, pdf) in enumerate(letter_docs, 1):
                    st.markdown(f"**Version {i}**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            f"Download Letter {i} (DOCX)",
                            docx,
                            f"cover_letter_{i}.docx",
                            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                    with col2:
                        st.download_button(
                            f"Download Letter {i} (PDF)",
                            pdf,
                            f"cover_letter_{i}.pdf",
                            "application/pdf",
                            use_container_width=True
                        )
                
                # Success message with better styling and clear next steps
                st.markdown("""
                    <div class='success-message'>
                        <h4>Documents Generated Successfully!</h4>
                        <p>Your documents have been tailored to the job description. You can:</p>
                        <ul>
                            <li>Download the documents in your preferred format</li>
                            <li>Switch to the 'Review & Edit' tab to make any adjustments</li>
                            <li>Regenerate individual documents if needed</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    with tab2:
        view_and_edit_documents()

if __name__ == "__main__":
    main()