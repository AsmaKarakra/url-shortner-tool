from datetime import datetime, timedelta
import os
import time
import random
import string
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, request
from flask_caching import Cache
from flask import current_app
from waitress import serve
from extensions import db
from config import DevelopmentConfig, ProductionConfig
from models import Access, SequenceID, ShortURL
from flask_migrate import Migrate

# Load environment variables for configuration from a .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Configure the Flask app based on the FLASK_ENV environment variable
# This determines whether the app runs in development or production mode
if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object(ProductionConfig())
else:
    app.config.from_object(DevelopmentConfig())

# Initialize the database with the app instance
db.init_app(app)

# Initialize the caching mechanism with the app instance
cache = Cache(app)

# Create database tables if they don't exist upon first request
with app.app_context():
    db.create_all()

def base62_encode(num, alphabet=string.digits + string.ascii_letters):
    """
    Converts a numerical ID to a Base62 encoded string.
    
    Args:
        num (int): The numerical ID to encode.
        alphabet (str): The character set to use for encoding, defaults to alphanumeric characters.
    
    Returns:
        str: A Base62 encoded string.
    """
    if num == 0:
        return alphabet[0]
    base62 = []
    base = len(alphabet)
    while num:
        num, i = divmod(num, base)
        base62.append(alphabet[i])
    return ''.join(reversed(base62))

def generate_unique_identifier():
    """
    Generates a unique identifier using the current time, a random component, and a sequence ID.
    
    Returns:
        int: A unique identifier.
    """
    timestamp = int(time.time() * 1000)
    random_component = random.randint(0, 999)
    sequence_id = get_next_sequence_id()
    unique_id = (timestamp * 1000) + random_component + (sequence_id % 1000)
    return unique_id

def generate_short_code(long_url):
    """
    Creates a short code for a given URL by generating a unique identifier and encoding it in Base62.
    
    Args:
        long_url (str): The original URL to shorten.
    
    Returns:
        str: A short code for the URL.
    """
    unique_id = generate_unique_identifier()
    short_code = base62_encode(unique_id)
    return short_code

def get_next_sequence_id():
    """
    Retrieves the next sequence ID to be used in generating a unique identifier.
    This method ensures uniqueness across all generated IDs by using a database-driven approach.
    
    Returns:
        int: The next sequence ID.
    """
    # Retrieve the single SequenceID instance or create it if it doesn't exist
    sequence_id_instance = SequenceID.query.first()
    if not sequence_id_instance:
        sequence_id_instance = SequenceID(last_sequence_id=0)
        db.session.add(sequence_id_instance)
        db.session.commit()
    
    # Increment the sequence ID safely
    sequence_id_instance.last_sequence_id += 1
    db.session.commit()
    
    return sequence_id_instance.last_sequence_id


@app.route('/shorten', methods=['POST'])
def shorten_url():
    """
    Endpoint to create a short URL from a given long URL.
    
    Expects JSON payload with a 'long_url' key.
    """
    data = request.get_json()
    long_url = data.get('long_url')
    if not long_url:
        return jsonify({'error': 'Missing long URL'}), 400

    short_code = generate_short_code(long_url)
    short_url = ShortURL(long_url=long_url, short_code=short_code)
    db.session.add(short_url)
    db.session.commit()

    # Use BASE_URL if specified, otherwise default to request.host_url
    base_url = os.getenv('BASE_URL', request.host_url)
    return jsonify({'short_url': base_url + short_code}), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_to_long_url(short_code):
    """
    Redirects the request to the original URL based on the short code provided.
    
    Args:
        short_code (str): The short code for the URL to redirect to.
    """
    # Attempt to fetch the long URL from cache first
    long_url = cache.get(short_code)
    if long_url is None:
        short_url = ShortURL.query.filter_by(short_code=short_code).first_or_404()
        long_url = short_url.long_url
        cache.set(short_code, long_url)
        # Record access for statistics
        access = Access(short_url_id=short_url.id)
        db.session.add(access)
        db.session.commit()
    return redirect(long_url, code=302)

@app.route('/stats/<short_code>', methods=['GET'])
def url_stats(short_code):
    """
    Provides statistics for a short URL: accesses in the last 24 hours, past week, and all time.
    
    Args:
        short_code (str): The short code to gather stats for.
    """
    short_url = ShortURL.query.filter_by(short_code=short_code).first_or_404()
    stats = {
        'last_24_hours': Access.query.filter(Access.short_url_id == short_url.id, Access.accessed_at > datetime.utcnow() - timedelta(days=1)).count(),
        'past_week': Access.query.filter(Access.short_url_id == short_url.id, Access.accessed_at > datetime.utcnow() - timedelta(weeks=1)).count(),
        'all_time': Access.query.filter_by(short_url_id=short_url.id).count(),
    }
    return jsonify(stats)

if __name__ == '__main__':
    if os.getenv('FLASK_ENV') == 'production':
        serve(app, host='0.0.0.0', port=5000)
    else:
        app.run(debug=True)