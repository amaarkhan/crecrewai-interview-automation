# CrewAI Interview Automation

An AI-powered interview automation system with a Flask web interface that generates personalized interview questions and responses using CrewAI and Google's Gemini AI.

## Features

- **Web Interface**: Modern, responsive Flask web application
- **Recruiter Profiling**: Analyzes recruiter characteristics to tailor interview style
- **Candidate Analysis**: Reviews resume and GitHub profile to understand candidate strengths
- **Question Generation**: Creates relevant technical interview questions
- **Mock Responses**: Generates realistic candidate answers in their communication style
- **Templates**: Pre-built templates for different company types (Startup, Enterprise, Remote)
- **Export Options**: Download results as text files or copy to clipboard

## Screenshots

### Main Interface
The application provides an intuitive web interface for inputting candidate and job information.

### Results Page
View generated interview questions and answers with options to download or copy the results.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/amaarkhan/crecrewai-interview-automation.git
cd crecrewai-interview-automation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
GOOGLE_API_KEY=your_gemini_api_key_here
SECRET_KEY=your-secret-key-for-flask-sessions
```

4. Run the Flask application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

### Web Interface
1. Open the application in your browser
2. Fill in the recruiter characteristics
3. Add candidate resume and GitHub profile information
4. Paste the job description
5. Click "Generate Interview Simulation"
6. View, download, or copy the results

### Command Line (Original)
You can still use the original command-line version:
```bash
python Agents.py
```

### API Endpoints
The application also provides REST API endpoints:

- `POST /api/generate` - Generate interview simulation
- `GET /health` - Health check

## Templates

The application includes pre-built templates for:
- **Tech Startup**: Fast-paced environment focused on innovation
- **Enterprise**: Large company with structured processes
- **Remote-First**: Distributed team collaboration

## How it Works

The system uses four AI agents:
1. **Recruiter Research Analyst** - Creates recruiter personality profile
2. **Candidate Research Analyst** - Analyzes candidate background
3. **Mock Interviewer** - Generates tailored interview questions
4. **Mock Candidate** - Provides realistic responses

## File Structure

```
crecrewai-interview-automation/
├── app.py                 # Flask web application
├── Agents.py             # Original command-line version
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   └── result.html
├── static/             # Static assets
│   └── css/
│       └── custom.css
└── results/           # Generated results (auto-created)
```

## Configuration

Edit the input variables in `app.py` or use the web interface to customize:
- `recruiter_text`: Recruiter characteristics
- `resumetext`: Candidate resume information
- `github_url`: Candidate's GitHub profile
- `job_description`: Target job requirements

## API Usage

### Generate Interview (POST /api/generate)

```json
{
  "recruiter_text": "Tech startup recruiter...",
  "resume_text": "Candidate background...",
  "github_url": "https://github.com/username",
  "job_description": "Job requirements..."
}
```

Response:
```json
{
  "success": true,
  "result": "Generated interview content...",
  "timestamp": "2025-01-17T10:30:00"
}
```

## Troubleshooting

1. **API Key Issues**: Ensure your Google API key is valid and has Gemini API access
2. **Rate Limits**: The application includes retry logic for API rate limits
3. **Long Processing**: Interview generation may take 2-5 minutes depending on complexity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.