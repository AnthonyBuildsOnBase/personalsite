import logging
import os
from datetime import datetime
import feedparser
from flask import Flask, render_template, abort
import markdown
from time import mktime
import yaml
from database import db
from models import BucketListItem

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = "a secret key"  # In production, use environment variable

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///site.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

def calculate_reading_time(content):
    """Calculate reading time in minutes based on word count."""
    words = len(content.split())
    minutes = round(words / 200)  # Assuming 200 words per minute reading speed
    return max(1, minutes)  # Minimum 1 minute reading time


def load_substack_posts(substack_url):
    """Load posts from Substack RSS feed."""
    try:
        feed = feedparser.parse(f"{substack_url}/feed")
        posts = []
        for entry in feed.entries[:5]:  # Get latest 5 posts
            posts.append({
                'title': entry.title,
                'link': entry.link,
                'date': datetime.fromtimestamp(
                    mktime(entry.published_parsed)) if hasattr(
                        entry, 'published_parsed') else datetime.now(),
            })
        return posts
    except Exception as e:
        logging.error(f"Error fetching Substack posts: {e}")
        return []


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
                # Parse content
                content = f.read()

                # Split metadata and content
                if content.startswith('---'):
                    parts = content.split('---', 2)[1:]
                    if len(parts) >= 2:
                        metadata = yaml.safe_load(parts[0])
                        content = parts[1]
                    else:
                        metadata = {}
                        content = parts[0]
                else:
                    metadata = {}

                # Convert content from markdown to HTML
                html_content = markdown.markdown(content)

                # Create slug from filename
                slug = filename[:-3]  # Remove .md extension

                # Store post data
                posts[slug] = {
                    'title': metadata.get('title', 'Untitled'),
                    'date': datetime.strptime(
                        str(metadata.get('date', '2000-01-01')), '%Y-%m-%d'),
                    'tags': metadata.get('tags', []),
                    'content': html_content,
                    'reading_time': calculate_reading_time(content)
                }

    return posts


# Load posts at startup
POSTS = load_posts()


@app.route('/')
def index():
    # Get Substack posts
    substack_posts = load_substack_posts('https://newontheblock.substack.com')

    writings_content = []

    # Add Substack posts if available
    if substack_posts:
        for post in substack_posts:
            writings_content.append(
                f'• <a href="{post["link"]}">{post["title"]}</a> ({post["date"].strftime("%Y")})'
            )

    return render_template(
        'index.html',
        name="Anthonyk.base.eth",
        current={
            "location": "Manhattan, NY",
            "role": "DeFi Ecosystem Analyst at Base",
            "focus":
            "Passionate about political and economic tools that empower individuals to realize the full value of the internet",
            "links": [{
                "label": "GitHub",
                "url": "https://github.com/AnthonyBuildsOnBase"
            }, {
                "label": "LinkedIn",
                "url": "https://www.linkedin.com/in/anthony-katwan-566675175/"
            }, {
                "label": "Twitter",
                "url": "https://x.com/0xblockboy"
            }]
        },
        sections=[{
            "title":
            "Now",
            "content":
            """
                Working at <a href="https://www.base.org/about?utm_source=dotorg&utm_medium=nav">Base</a> to bring the worlds financial markets onchain.
                """
        }, {
            "title":
            "Previously",
            "content":
            """
                • Web3 research and consulting for enterprises
                • Business ops and strategy for GTM organizations
                • DAO contributor and open source development
                """
        }, {
            "title":
            "Favorite Readings",
            "content":
            """
                • <a href="https://writings.stephenwolfram.com/2019/06/testifying-at-the-senate-about-a-i-selected-content-on-the-internet/">Testifying at the Senate about A.I.-Selected Content on the Internet</a>
                • <a href="https://www.ribbonfarm.com/2018/11/28/the-digital-maginot-line/">The Digital Maginot Line</a>
                • <a href="https://kk.org/thetechnium/1000-true-fans/">1,000 True Fans</a>
                • <a href="https://slatestarcodex.com/2014/07/30/meditations-on-moloch/">Meditations on Moloch</a>
                • <a href="https://alexdanco.com/2019/09/07/positional-scarcity/">Positional Scarcity</a>
                • <a href="https://www.jofreeman.com/joreen/tyranny.htm">The Tyranny of Structurelessness</a>
                • <a href="https://nickbostrom.com/fable/dragon">The Fable of the Dragon-Tyrant</a>
                • <a href="https://meaningness.com/geeks-mops-sociopaths">Geeks, MOPs, and sociopaths in subculture evolution</a>
                """
        }, {
            "title": "My Writings",
            "content": "\n".join(writings_content)
        }],
        current_date=datetime.now())


@app.route('/posts/<slug>')
def post(slug):
    post_data = POSTS.get(slug)
    if not post_data:
        abort(404)
    return render_template('post.html', post=post_data)


@app.route('/bucketlist')
def bucketlist():
    current_year = datetime.now().year

    # Get all items ordered by year and priority
    items = BucketListItem.query.order_by(
        BucketListItem.target_year.asc(),
        BucketListItem.priority.desc(),
        BucketListItem.created_at.desc()
    ).all()

    # Organize items by year and category
    years_data = {}
    for item in items:
        year = item.target_year
        if year not in years_data:
            years_data[year] = {'categories': {}, 'total': 0, 'completed': 0}

        category = item.category or 'Uncategorized'
        if category not in years_data[year]['categories']:
            years_data[year]['categories'][category] = []

        years_data[year]['categories'][category].append(item)
        years_data[year]['total'] += 1
        if item.completed:
            years_data[year]['completed'] += 1

    # Organize years into past, present, and future
    organized_years = {
        'past': {year: data for year, data in years_data.items() if year < current_year},
        'current': {year: data for year, data in years_data.items() if year == current_year},
        'future': {year: data for year, data in years_data.items() if year > current_year}
    }

    # Add debug logging
    app.logger.debug(f"Found {len(items)} total items")
    app.logger.debug(f"Organized years data: {organized_years}")

    return render_template(
        'bucketlist.html',
        organized_years=organized_years,
        current_year=current_year,
        current_date=datetime.now()
    )


@app.route('/bucketlist/toggle/<int:item_id>', methods=['POST'])
def toggle_item(item_id):
    item = BucketListItem.query.get_or_404(item_id)
    item.completed = not item.completed
    item.completion_date = datetime.utcnow() if item.completed else None
    db.session.commit()
    return {'success': True, 'completed': item.completed}


def create_sample_bucketlist_items():
    """Create sample bucket list items if none exist."""
    if BucketListItem.query.first() is None:
        current_year = datetime.utcnow().year
        items = [
            {
                'title': 'Learn to Play Piano',
                'description': 'Master at least one classical piece',
                'category': 'Skills',
                'priority': 2,
                'target_year': current_year
            },
            {
                'title': 'Visit Northern Lights',
                'description': 'See the Aurora Borealis in person',
                'category': 'Travel',
                'priority': 3,
                'target_year': current_year + 1
            },
            {
                'title': 'Run a Marathon',
                'description': 'Complete a full 26.2 mile marathon',
                'category': 'Fitness',
                'priority': 1,
                'target_year': current_year
            },
            {
                'title': 'Write a Book',
                'description': 'Complete and publish a novel',
                'category': 'Creative',
                'priority': 2,
                'target_year': current_year + 2
            },
            {
                'title': 'Learn Photography',
                'description': 'Master manual camera settings',
                'category': 'Skills',
                'priority': 1,
                'target_year': current_year - 1,
                'completed': True,
                'completion_date': datetime(current_year - 1, 12, 1)
            }
        ]

        for item in items:
            bucket_item = BucketListItem(**item)
            db.session.add(bucket_item)

        db.session.commit()


with app.app_context():
    db.create_all()
    create_sample_bucketlist_items()