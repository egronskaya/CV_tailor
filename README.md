# CV Tailor

A Streamlit application that tailors CVs and cover letters to specific job advertisements using GPT-4. The application automatically adapts your CV and generates customized cover letters to maximize your chances of success with automated CV screening systems.

## Privacy & Security Features

**Enhanced Privacy Protection**

- All interactions with AI models are configured for maximum privacy:
  - Requests that data not be stored or used for training
  - Anonymous session handling
  - Private inference mode
  - Secure headers implementation
  - No user data association
  - Proper resource cleanup

- Personal data protection:
  - User CV and examples stored locally in `user_data/` (not committed to git)
  - Secure async processing
  - No data persistence in the application
  - Privacy-first API interactions

## Features

- Job advertisement analysis
- CV tailoring based on job requirements
- Generation of both PDF and DOCX formats
- Extraction of job-specific skills
- Generation of three unique cover letter variants
- Customizable CV and cover letter styling
- LaTeX-based CV templating
- Secure and private data handling

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your configuration:
   ```bash
   # Copy the example configuration
   cp .env.example .env
   
   # Edit the .env file with your settings
   nano .env
   ```

   Required environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `GPT_MODEL`: The GPT model to use (default: gpt-4.1-mini)

   Security and privacy settings:
   - `SAVE_INTERMEDIATE`: Control data persistence (default: false)
   - `DEBUG_MODE`: Toggle detailed logging (default: false)
   - All API calls automatically use privacy-preserving headers
   - Anonymous sessions for enhanced security

   Optional configuration:
   - Model parameters (temperature, tokens, etc.)
   - Document generation settings
   - Output and formatting preferences
   - Debug and development options

   See `.env.example` for all available options and their descriptions.

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Input the job advertisement text
3. The application will generate:
   - Tailored CV (PDF & DOCX)
   - Three versions of cover letters (PDF & DOCX)
   - List of job-specific skills

## Project Structure

```
.
├── app.py                  # Main Streamlit application
├── user_data/             # User-specific files (not committed to git)
│   ├── cv/               # Your personal CV content
│   ├── cover_letters/    # Your example cover letters
│   ├── style/           # Your style preferences
│   ├── templates/       # Document templates and guides
│   └── outputs/         # Generated documents
├── src/
│   ├── cv_processor.py     # CV processing logic
│   ├── letter_generator.py # Cover letter generation
│   └── document_maker.py   # PDF/DOCX document creation
├── figures/               # Icons and graphics for CV generation

└── requirements.txt        # Project dependencies
```

### User Data Setup

Before using the application, you need to set up your personal data in the `user_data` directory:

1. In `user_data/cv/`:
   - Copy `example_cv.tex` to `user_cv.tex`
   - Edit `user_cv.tex` with your CV content

2. In `user_data/cover_letters/`:
   - Create at least 3 example cover letters that reflect your writing style
   - These will be used to maintain your tone in generated letters

3. In `user_data/style/`:
   - Copy `user_style_example.yaml` to `user_style.yaml`
   - Edit with your preferred styling options

The `user_data` directory is not committed to git to protect your personal information. The application will read these files based on the paths specified in your `.env` file.

## Contributing

Feel free to submit issues and enhancement requests.

## License

MIT License