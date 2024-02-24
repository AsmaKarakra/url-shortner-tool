from extensions import db
from datetime import datetime

class ShortURL(db.Model):
    """
    Database model for short URLs.
    
    Attributes:
        id (int): Primary key.
        long_url (str): The original long URL.
        short_code (str): The unique short code for the URL.
        created_at (datetime): Timestamp of URL creation.
        accesses (relationship): Relationship to access records.
    """
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    accesses = db.relationship('Access', backref='shorturl', lazy='dynamic')

class Access(db.Model):
    """
    Database model for access records of short URLs.
    
    Attributes:
        id (int): Primary key.
        short_url_id (int): Foreign key to the short URL.
        accessed_at (datetime): Timestamp of access.
    """
    id = db.Column(db.Integer, primary_key=True)
    short_url_id = db.Column(db.Integer, db.ForeignKey('short_url.id'), nullable=False)
    accessed_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class SequenceID(db.Model):
    """
    A model representing a sequence ID used for generating unique identifiers.
    
    This model tracks the last sequence ID issued to ensure that each generated
    identifier is unique and sequential. It is particularly useful in scenarios
    where unique, incrementing identifiers are required across the application.
    
    Attributes:
        id (int): The primary key for the model. Not directly related to the sequence ID but necessary for database operations.
        last_sequence_id (int): Stores the last sequence ID issued. This value is incremented with each new identifier request.
    """

    __tablename__ = 'sequence_id'  # Defines the table name in the database

    # Primary key for the model, standard practice for an ORM model
    id = db.Column(db.Integer, primary_key=True)

    # The last issued sequence ID. Defaults to 0 and increments as new IDs are generated.
    last_sequence_id = db.Column(db.Integer, default=0)
