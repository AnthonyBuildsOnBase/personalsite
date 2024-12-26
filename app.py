import logging
from flask import Flask, render_template
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = "a secret key"  # In production, use environment variable

@app.route('/')
def index():
    return render_template('index.html', 
        name="John Doe",
        current={
            "location": "San Francisco, CA",
            "role": "Software Engineer",
            "focus": "Building minimalist web applications"
        },
        sections=[
            {
                "title": "Now",
                "content": """
                I'm currently focused on building web applications with Python and Flask.
                Learning about system design and distributed systems.
                Reading "Designing Data-Intensive Applications".
                """
            },
            {
                "title": "Previously",
                "content": """
                • Led backend development for a startup's core product
                • Worked on scalable microservices architecture
                • Contributed to open-source Python libraries
                • Taught programming workshops at local meetups
                """
            },
            {
                "title": "Projects",
                "content": """
                • Personal website - A minimalist approach to personal presence
                • Task Manager - Simple CLI tool for managing daily tasks
                • Weather App - Minimalist weather forecasting
                """
            },
            {
                "title": "Reading",
                "content": """
                • Designing Data-Intensive Applications by Martin Kleppmann
                • The Pragmatic Programmer by Dave Thomas
                • Clean Code by Robert C. Martin
                """
            },
            {
                "title": "Writings",
                "content": """
                • Why Minimalism Matters in Software Design
                • Building a Personal Website with Flask
                • Thoughts on Technical Writing
                • Notes on System Design Principles
                """
            }
        ],
        current_date=datetime.now())