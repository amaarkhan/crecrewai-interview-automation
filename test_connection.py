import os
from dotenv import load_dotenv
from crewai import LLM

# Load environment variables
load_dotenv()

def test_api():
    """Test the Gemini API connection"""
    try:
        # Check if API key is loaded
        api_key = os.getenv("GOOGLE_API_KEY")
        print(f"API Key loaded: {'Yes' if api_key else 'No'}")
        
        if not api_key:
            print("❌ No API key found in .env file")
            return False
            
        print(f"API Key length: {len(api_key)}")
        
        # Test the LLM
        llm = LLM(
            model="gemini/gemini-1.5-flash",
            api_key=api_key
        )
        
        print("✅ LLM initialization successful!")
        return True
        
    except Exception as e:
        print("❌ API Test failed!")
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Gemini API connection...")
    success = test_api()
    
    if success:
        print("\n✅ API connection is working! You can now run Agents.py")
    else:
        print("\n❌ Please check your .env file and ensure GOOGLE_API_KEY is set correctly")
        print("Example .env file content:")
        print("GOOGLE_API_KEY=your_actual_api_key_here")
