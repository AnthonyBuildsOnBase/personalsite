import logging
from flask import Flask, render_template, abort
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = "a secret key"  # In production, use environment variable

# Blog posts data
POSTS = {
    'minimalism-in-software': {
        'title': 'Why Minimalism Matters in Software Design',
        'date': datetime(2024, 12, 1),
        'content': """
        Minimalism in software design isn't just about aesthetics—it's about clarity, maintainability, and user experience.

        Here are three key principles I follow:

        1. Remove everything that isn't absolutely necessary
        2. Make what remains as simple as possible
        3. Focus on the core functionality that users actually need

        These principles have guided my recent projects and significantly improved their maintainability.
        """
    },
    'flask-website': {
        'title': 'Building a Personal Website with Flask',
        'date': datetime(2024, 11, 15),
        'content': """
        Flask's simplicity makes it perfect for personal websites. Here's how I built mine:

        • Started with a minimal setup
        • Used Jinja2 templates for clean HTML
        • Kept the design simple and focused
        • Deployed with minimal configuration

        The result? A fast, maintainable site that puts content first.
        """
    },
    'technical-writing': {
        'title': 'Thoughts on Technical Writing',
        'date': datetime(2024, 10, 30),
        'content': """
        Good technical writing is about clarity and precision. Through my experience, I've learned:

        • Write for your reader, not yourself
        • Use simple, direct language
        • Include relevant examples
        • Structure content logically

        These principles help make complex topics accessible.
        """
    },
    'system-design': {
        'title': 'Notes on System Design Principles',
        'date': datetime(2024, 10, 15),
        'content': """
        Key principles I've learned about system design:

        • Start simple, add complexity only when needed
        • Design for failure
        • Make it observable
        • Consider scalability from day one

        These principles have guided my approach to building robust systems.
        """
    }
}

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
                • <a href="/posts/minimalism-in-software">Why Minimalism Matters in Software Design</a>
                • <a href="/posts/flask-website">Building a Personal Website with Flask</a>
                • <a href="/posts/technical-writing">Thoughts on Technical Writing</a>
                • <a href="/posts/system-design">Notes on System Design Principles</a>
                """
            }
        ],
        current_date=datetime.now())

@app.route('/posts/<slug>')
def post(slug):
    post_data = POSTS.get(slug)
    if not post_data:
        abort(404)
    return render_template('post.html', post=post_data)