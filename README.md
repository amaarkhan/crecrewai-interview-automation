# CrewAI Interview Automation

An AI-powered interview automation system that generates personalized interview questions and responses using CrewAI and Google's Gemini AI.

## Features

- **Recruiter Profiling**: Analyzes recruiter characteristics to tailor interview style
- **Candidate Analysis**: Reviews resume and GitHub profile to understand candidate strengths
- **Question Generation**: Creates relevant technical interview questions
- **Mock Responses**: Generates realistic candidate answers in their communication style

## Setup

1. Clone the repository:
```bash
git clone https://github.com/amaarkhan/crecrewai-interview-automation.git
cd crecrewai-interview-automation
```

2. Install dependencies:
```bash
pip install crewai python-dotenv
```

3. Create a `.env` file with your Google API key:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

4. Run the application:
```bash
python Agents.py
```

## How it Works

The system uses four AI agents:
1. **Recruiter Research Analyst** - Creates recruiter personality profile
2. **Candidate Research Analyst** - Analyzes candidate background
3. **Mock Interviewer** - Generates tailored interview questions
4. **Mock Candidate** - Provides realistic responses

## Configuration

Edit the input variables in `Agents.py` to customize:
- `recruiter_text`: Recruiter characteristics
- `resumetext`: Candidate resume information
- `github_url`: Candidate's GitHub profile
- `job_description`: Target job requirements