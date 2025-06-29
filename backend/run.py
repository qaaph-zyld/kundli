"""
Run Script
This script serves as a convenient entry point for running the FastAPI application.
"""
import os
import sys
import subprocess

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

if __name__ == "__main__":
    # Run the application using the main.py script
    subprocess.run([sys.executable, os.path.join("src", "main.py")])
