import os


class Config:
    """
    Base configuration class. Subclasses include configurations specific
    to development, testing, and production environments.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

class DevelopmentConfig(Config):
    """Development-specific configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:123456789@localhost/postgres')

class TestingConfig(Config):
    """Testing-specific configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:123456789@localhost/postgres')
    TESTING = True

class ProductionConfig(Config):
    """Production-specific configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:123456789@localhost/postgres')


