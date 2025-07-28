from dotenv import load_dotenv
import os

load_dotenv()

print("Environment variable loaded:", os.getenv('OPENAI_API_KEY'))