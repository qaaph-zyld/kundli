"""
Main Entry Point
This module serves as the entry point for the FastAPI application.
"""
import os
import uvicorn
from dotenv import load_dotenv

from api.app import create_app
from infrastructure.database import init_db

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Initialize the database
    init_db()
    
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "False").lower() == "true"
    
    # Run the application
    uvicorn.run(
        "api.app:app",
        host=host,
        port=port,
        reload=reload,
    )
