#!/usr/bin/env python3
"""
Virtual AI Office - Main Entry Point
Starts the FastAPI server with autonomous agents
"""

import uvicorn
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import settings

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║         🤖 Virtual AI Office - Agent Dashboard 🤖            ║
    ║                                                              ║
    ║  Your autonomous AI agents are starting...                  ║
    ║                                                              ║
    ║  Dashboard: http://localhost:8000/dashboard                 ║
    ║  API Docs:  http://localhost:8000/docs                      ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level="info"
    )
