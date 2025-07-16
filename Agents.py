import os
import time
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# Load Gemini API Key from environment
load_dotenv()

def create_llm_with_retry():
    """Create LLM with retry logic for service unavailable errors"""
    for attempt in range(3):
        try:
            llm = LLM(
                model="gemini/gemini-1.5-flash",
                api_key=os.getenv("GOOGLE_API_KEY")
            )
            print("✅ LLM connection successful!")
            return llm
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
            if attempt < 2:
                print(f"Retrying in {5 * (attempt + 1)} seconds...")
                time.sleep(5 * (attempt + 1))
            else:
                print("All attempts failed. Using simplified configuration...")
                return LLM(model="gemini/gemini-1.5-flash")

# 🔐 Gemini LLM with retry logic
print("🔄 Setting up LLM connection...")
llm = create_llm_with_retry()

# 🔍 Inputs
recruiter_text = "Recruiter from tech startup, values innovation and technical depth, prefers direct communication and looks for candidates with strong problem-solving skills."
resumetext = """
Amaar Khan is a Full Stack Developer and AI enthusiast with expertise in Python, JavaScript, React, Node.js, and machine learning. 
He has extensive experience building web applications, working with APIs, and creating innovative solutions. 
Active contributor to open-source projects with a passion for emerging technologies and automation.
"""
github_url = "https://github.com/amaarkhan"
job_description = """
Senior Full Stack Developer Position
We are seeking a talented Full Stack Developer to join our dynamic team. The ideal candidate will have:

- Strong proficiency in Python and JavaScript
- Experience with React, Node.js, and modern web frameworks
- Knowledge of API development and integration
- Familiarity with machine learning and AI technologies
- Experience with version control (Git) and collaborative development
- Strong problem-solving skills and ability to work in agile environments
- Excellent communication skills and team collaboration abilities

Responsibilities:
- Develop and maintain web applications using modern technologies
- Design and implement RESTful APIs
- Collaborate with cross-functional teams on product development
- Contribute to architectural decisions and code reviews
- Stay updated with latest technology trends and best practices
"""

# 🧠 AGENTS

recruiter_agent = Agent(
    role="Recruiter Research Analyst",
    goal="Analyze recruiter input and generate a recruiter personality profile",
    backstory="Expert at profiling recruiters to simulate their interview style.",
    llm=llm,
    verbose=True,
)

recruiter_task = Task(
    description=f"Create a personality profile for the recruiter based on: {recruiter_text}",
    expected_output="A detailed recruiter character profile based on traits, style, and values.",
    agent=recruiter_agent
)

candidate_agent = Agent(
    role="Candidate Research Analyst",
    goal="Analyze GitHub and resume to generate a candidate profile",
    backstory="Expert in analyzing resumes and GitHub profiles to identify strengths and skills.",
    llm=llm,
    verbose=True,
)

candidate_task = Task(
    description=f"""
    Given the following resume:\n{resumetext}\n\n
    and GitHub URL: {github_url}\n\n
    generate a candidate profile with technical skills, project strengths, and communication style.
    """,
    expected_output="Candidate profile highlighting technical stack, interests, and communication tone.",
    agent=candidate_agent
)

interviewer_agent = Agent(
    role="Mock Interviewer",
    goal="Generate a list of questions based on the recruiter and candidate profiles",
    backstory="Simulates the recruiter and prepares technical interview questions tailored to the job.",
    llm=llm,
    verbose=True,
)

interview_task = Task(
    description=f"""
    Generate at least 10 technical interview questions for a Senior Full Stack Developer job.
    Use the job description:\n{job_description}\n\n
    Tailor the tone to match the recruiter's style and the candidate's strengths.
    """,
    expected_output="List of 10+ job-relevant interview questions.",
    agent=interviewer_agent,
    context=[recruiter_task, candidate_task]
)

candidate_mock_agent = Agent(
    role="Mock Candidate",
    goal="Answer interview questions in the tone of the candidate",
    backstory="Simulates the candidate and answers interview questions accurately and concisely.",
    llm=llm,
    verbose=True,
)

answer_task = Task(
    description="Answer the interview questions generated above in the tone and style of the candidate.",
    expected_output="Thoughtful, well-structured answers matching candidate's profile.",
    agent=candidate_mock_agent,
    context=[interview_task, candidate_task]
)

# 🧪 Run the Crew
print("🚀 Starting interview automation...")
try:
    crew = Crew(
        agents=[recruiter_agent, candidate_agent, interviewer_agent, candidate_mock_agent],
        tasks=[recruiter_task, candidate_task, interview_task, answer_task],
        verbose=True
    )

    # 👇 Execute
    result = crew.kickoff()
    print("\n🧠 FINAL OUTPUT:\n")
    print(result)
except Exception as e:
    print(f"❌ Error during execution: {e}")
    import traceback
    print("Full error traceback:")
    traceback.print_exc()
    print("\nThis might be due to:")
    print("1. API rate limits or service availability")
    print("2. Invalid API key in .env file")
    print("3. Network connectivity issues")
    print("Please check your .env file and try again in a few minutes.")
