


import os
from dotenv import load_dotenv

# Load .env file from the current directory
load_dotenv()

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

