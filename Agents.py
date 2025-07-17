import os
import time
import requests
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

def fetch_github_data(github_url):
    """Fetch real data from GitHub profile"""
    try:
        # Extract username from GitHub URL
        username = github_url.split('/')[-1]
        
        # GitHub API endpoints
        user_url = f"https://api.github.com/users/{username}"
        repos_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10"
        
        # Fetch user profile
        user_response = requests.get(user_url)
        repos_response = requests.get(repos_url)
        
        if user_response.status_code == 200 and repos_response.status_code == 200:
            user_data = user_response.json()
            repos_data = repos_response.json()
            
            # Extract relevant information
            github_info = {
                'name': user_data.get('name', 'Not provided'),
                'bio': user_data.get('bio', 'No bio available'),
                'public_repos': user_data.get('public_repos', 0),
                'followers': user_data.get('followers', 0),
                'following': user_data.get('following', 0),
                'company': user_data.get('company', 'Not specified'),
                'location': user_data.get('location', 'Not specified'),
                'blog': user_data.get('blog', 'No blog'),
                'created_at': user_data.get('created_at', ''),
                'updated_at': user_data.get('updated_at', ''),
                'top_repositories': []
            }
            
            # Extract top repositories info
            for repo in repos_data[:5]:  # Top 5 repos
                repo_info = {
                    'name': repo.get('name', ''),
                    'description': repo.get('description', 'No description'),
                    'language': repo.get('language', 'Not specified'),
                    'stars': repo.get('stargazers_count', 0),
                    'forks': repo.get('forks_count', 0),
                    'updated_at': repo.get('updated_at', ''),
                    'topics': repo.get('topics', [])
                }
                github_info['top_repositories'].append(repo_info)
            
            return github_info
        else:
            return {'error': f"Failed to fetch GitHub data. Status codes: User={user_response.status_code}, Repos={repos_response.status_code}"}
            
    except Exception as e:
        return {'error': f"Error fetching GitHub data: {str(e)}"}

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

# 🔍 Fetch real GitHub data
print("🔍 Fetching GitHub profile data...")
github_data = fetch_github_data(github_url)
if 'error' in github_data:
    print(f"⚠️ Warning: {github_data['error']}")
    github_info_text = f"GitHub URL: {github_url} (Could not fetch live data)"
else:
    print("✅ GitHub data fetched successfully!")
    github_info_text = f"""
REAL GITHUB PROFILE DATA for {github_url}:

Personal Info:
- Name: {github_data['name']}
- Bio: {github_data['bio']}
- Company: {github_data['company']}
- Location: {github_data['location']}
- Blog: {github_data['blog']}
- Public Repositories: {github_data['public_repos']}
- Followers: {github_data['followers']}
- Following: {github_data['following']}
- Account Created: {github_data['created_at']}

Top 5 Recent Repositories:
"""
    for i, repo in enumerate(github_data['top_repositories'], 1):
        github_info_text += f"""
{i}. {repo['name']} ({repo['language']})
   - Description: {repo['description']}
   - Stars: {repo['stars']}, Forks: {repo['forks']}
   - Topics: {', '.join(repo['topics']) if repo['topics'] else 'None'}
   - Last Updated: {repo['updated_at']}
"""

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
    and REAL GitHub profile data:\n{github_info_text}\n\n
    
    Analyze the candidate's technical skills, programming languages, project experience, and coding patterns based on their actual GitHub repositories and activity.
    Pay attention to:
    - Programming languages used in repositories
    - Project complexity and diversity
    - Repository descriptions and topics
    - Community engagement (stars, forks)
    - Recent activity and consistency
    
    Generate a comprehensive candidate profile.
    """,
    expected_output="Detailed candidate profile based on resume and REAL GitHub data including technical skills, project analysis, and communication style.",
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
