import logging
import os
from datetime import datetime
from flask import Flask, render_template, abort
import frontmatter
import markdown

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = "a secret key"  # In production, use environment variable


def calculate_reading_time(content):
    """Calculate reading time in minutes based on word count."""
    words = len(content.split())
    minutes = round(words / 200)  # Assuming 200 words per minute reading speed
    return max(1, minutes)  # Minimum 1 minute reading time


def load_posts():
    """Load all posts from markdown files."""
    posts = {}
    posts_dir = os.path.join('content', 'posts')

    # Create posts directory if it doesn't exist
    os.makedirs(posts_dir, exist_ok=True)

    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(posts_dir, filename)
            with open(file_path, 'r') as f:
                # Parse front matter and content
                post = frontmatter.load(f)

                # Convert content from markdown to HTML
                html_content = markdown.markdown(post.content)

                # Create slug from filename
                slug = filename[:-3]  # Remove .md extension

                # Store post data
                posts[slug] = {
                    'title': post.metadata.get('title', 'Untitled'),
                    'date': datetime.strptime(
                        str(post.metadata.get('date', '2000-01-01')),
                        '%Y-%m-%d'),
                    'tags': post.metadata.get('tags', []),
                    'content': html_content,
                    'reading_time': calculate_reading_time(post.content)
                }

    return posts


# Load posts at startup
POSTS = load_posts()


@app.route('/')
def index():
    writings_content = []
    for slug, post in POSTS.items():
        tags_html = ' '.join(f'<span class="tag">{tag}</span>'
                          for tag in post['tags'])
        writings_content.append(
            f'• <a href="/posts/{slug}">{post["title"]}</a> ({post["date"].strftime("%Y")}) {tags_html}'
        )

    return render_template(
        'index.html',
        name="Anthonyk.base.eth",
        current={
            "location": "Manhattan, NY",
            "role": "DeFi Ecosystem Analyst at Base",
            "focus":
            "Passionate about political and economic tools that empower individuals to realize the full value of the internet",
            "links": [
                {"label": "GitHub", "url": "https://github.com/AnthonyBuildsOnBase"},
                {"label": "LinkedIn", "url": "https://www.linkedin.com/in/anthony-katwan-566675175/"},
                {"label": "Twitter", "url": "https://x.com/0xblockboy"}
            ]
        },
        sections=[{
            "title": "Now",
            "content": """
                Working at <a href="https://www.base.org/about?utm_source=dotorg&utm_medium=nav">Base</a> to bring the worlds financial markets onchain.
                """
        }, {
            "title": "Previously",
            "content": """
                • Led backend development for a startup's core product
                • Worked on scalable microservices architecture
                • Contributed to open-source Python libraries
                • Taught programming workshops at local meetups
                """
        }, {
            "title": "Reading",
            "content": """
                • Designing Data-Intensive Applications by Martin Kleppmann
                • The Pragmatic Programmer by Dave Thomas
                • Clean Code by Robert C. Martin
                """
        }, {
            "title": "Writings",
            "content": "\n".join(writings_content)
        }],
        current_date=datetime.now())


@app.route('/posts/<slug>')
def post(slug):
    post_data = POSTS.get(slug)
    if not post_data:
        abort(404)
    return render_template('post.html', post=post_data)