from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import time
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
import json
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

def create_llm_with_retry():
    """Create LLM with retry logic for service unavailable errors"""
    for attempt in range(3):
        try:
            llm = LLM(
                model="gemini/gemini-1.5-flash",
                api_key=os.getenv("GOOGLE_API_KEY")
            )
            return llm
        except Exception as e:
            if attempt < 2:
                time.sleep(5 * (attempt + 1))
            else:
                return LLM(model="gemini/gemini-1.5-flash")

def format_interview_result(result_text):
    """Format the interview result for better readability"""
    formatted_result = f"""
INTERVIEW SIMULATION RESULTS
{'='*50}

This simulation contains both interview questions and candidate responses.
The format shows: Q: [Question] followed by A: [Answer]

{'='*50}

{result_text}

{'='*50}
SIMULATION COMPLETE
"""
    return formatted_result

def run_interview_automation(recruiter_text, resume_text, github_url, job_description):
    """Run the interview automation process"""
    try:
        # Create LLM
        llm = create_llm_with_retry()
        
        # Create agents
        recruiter_agent = Agent(
            role="Recruiter Research Analyst",
            goal="Analyze recruiter input and generate a recruiter personality profile",
            backstory="Expert at profiling recruiters to simulate their interview style.",
            llm=llm,
            verbose=False,
        )

        candidate_agent = Agent(
            role="Candidate Research Analyst",
            goal="Analyze GitHub and resume to generate a candidate profile",
            backstory="Expert in analyzing resumes and GitHub profiles to identify strengths and skills.",
            llm=llm,
            verbose=False,
        )

        interviewer_agent = Agent(
            role="Mock Interviewer",
            goal="Generate a list of questions based on the recruiter and candidate profiles",
            backstory="Simulates the recruiter and prepares technical interview questions tailored to the job.",
            llm=llm,
            verbose=False,
        )

        candidate_mock_agent = Agent(
            role="Mock Candidate",
            goal="Answer interview questions in the tone of the candidate",
            backstory="Simulates the candidate and answers interview questions accurately and concisely.",
            llm=llm,
            verbose=False,
        )

        # Create tasks
        recruiter_task = Task(
            description=f"Create a personality profile for the recruiter based on: {recruiter_text}",
            expected_output="A detailed recruiter character profile based on traits, style, and values.",
            agent=recruiter_agent
        )

        candidate_task = Task(
            description=f"""
            Given the following resume:\n{resume_text}\n\n
            and GitHub URL: {github_url}\n\n
            generate a candidate profile with technical skills, project strengths, and communication style.
            """,
            expected_output="Candidate profile highlighting technical stack, interests, and communication tone.",
            agent=candidate_agent
        )

        interview_task = Task(
            description=f"""
            Generate 15-20 comprehensive interview questions for this job position:
            
            Job Description: {job_description}
            
            Create questions in these categories:
            1. Technical Skills (5-6 questions)
            2. Problem Solving & System Design (3-4 questions)  
            3. Experience & Projects (3-4 questions)
            4. Behavioral & Cultural Fit (2-3 questions)
            5. Role-Specific Scenarios (2-3 questions)
            
            Format each question clearly and number them. Tailor the difficulty and style to match the recruiter's approach and the candidate's experience level.
            """,
            expected_output="A numbered list of 15-20 well-structured interview questions organized by category.",
            agent=interviewer_agent,
            context=[recruiter_task, candidate_task]
        )

        answer_task = Task(
            description="""
            For each interview question generated above, provide both the QUESTION and the ANSWER in this format:
            
            **Q: [Question number]. [Full question text]**
            
            **A:** [Detailed answer in the candidate's style]
            
            Make sure to include both the original questions and the candidate's responses for a complete interview simulation.
            """,
            expected_output="Complete interview Q&A pairs with questions clearly stated followed by detailed candidate responses.",
            agent=candidate_mock_agent,
            context=[interview_task, candidate_task]
        )

        # Create and run crew
        crew = Crew(
            agents=[recruiter_agent, candidate_agent, interviewer_agent, candidate_mock_agent],
            tasks=[recruiter_task, candidate_task, interview_task, answer_task],
            verbose=False
        )

        result = crew.kickoff()
        formatted_result = format_interview_result(str(result))
        return {"success": True, "result": formatted_result}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_interview():
    try:
        # Get form data
        recruiter_text = request.form.get('recruiter_text', '')
        resume_text = request.form.get('resume_text', '')
        github_url = request.form.get('github_url', '')
        job_description = request.form.get('job_description', '')
        
        # Validate inputs
        if not all([recruiter_text, resume_text, github_url, job_description]):
            flash('Please fill in all fields', 'error')
            return redirect(url_for('index'))
        
        # Run the automation
        result = run_interview_automation(recruiter_text, resume_text, github_url, job_description)
        
        if result['success']:
            # Save result with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"interview_result_{timestamp}.txt"
            filepath = os.path.join('results', filename)
            
            # Create results directory if it doesn't exist
            os.makedirs('results', exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Interview Automation Result\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                f.write(result['result'])
            
            return render_template('result.html', 
                                 result=result['result'], 
                                 filename=filename,
                                 timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            flash(f'Error generating interview: {result["error"]}', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/generate', methods=['POST'])
def api_generate_interview():
    """API endpoint for generating interviews"""
    try:
        data = request.get_json()
        
        recruiter_text = data.get('recruiter_text', '')
        resume_text = data.get('resume_text', '')
        github_url = data.get('github_url', '')
        job_description = data.get('job_description', '')
        
        if not all([recruiter_text, resume_text, github_url, job_description]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        result = run_interview_automation(recruiter_text, resume_text, github_url, job_description)
        
        if result['success']:
            return jsonify({
                'success': True,
                'result': result['result'],
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'success': False, 'error': result['error']}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
