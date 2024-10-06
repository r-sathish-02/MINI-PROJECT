from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

# Check if the key is loaded properly
if openai_api_key:
    print("OpenAI API key loaded successfully")
    print(openai_api_key)
else:
    print("Error: OpenAI API key not found")
