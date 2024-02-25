# Flask-Based URL Shortener Service

## Introduction

A Flask-based URL shortener service designed to offer functionalities for shortening URLs, redirecting to original URLs via short links, and tracking URL access statistics.

## System Overview

Developed with Flask and utilizing extensions like Flask-Migrate and Flask-Caching, this application supports both development and production environments, configurable via a `.env` file.

## Features

- **URL Shortening**: Generate a short, unique alias for a given URL.
- **Redirection**: Redirect users from a short link to the original URL.
- **Access Tracking**: Track how many times a short link has been accessed.

## Non-Functional Requirements

- **Scalability**: Handles a high volume of requests efficiently.
- **Performance**: Ensures low latency in redirection and short link generation.
- **Reliability**: Maintains high availability for critical redirection functionality.
- **Security**: Implements measures to protect against common vulnerabilities.

## Architecture

### Components

- **Web Server**: Uses Waitress for serving the Flask application in production.
- **Flask Application**: Manages web routing, requests, and responses.
- **Database**: Employs SQLAlchemy with PostgreSQL for ORM and data persistence.
- **Caching**: Utilizes Flask-Caching for performance optimization.
- **Environment Configuration**: Managed through a `.env` file for security.

### Database Models

- **ShortURL**: Stores original URLs, their short codes, and creation timestamps.
- **Access**: Records each access to the short URLs.
- **SequenceID**: Generates unique identifiers for short links.

### Key Endpoints

- `/shorten`: Accepts long URLs and returns short versions.
- `/<short_code>`: Redirects to the original URLs.
- `/stats/<short_code>`: Provides access statistics for short links.

## Technical Details

### URL Encoding

- Uses Base62 encoding to transform unique identifiers into short, URL-friendly strings.

### Redirection

- Resolves short links from cache first, then database, optimizing performance and reducing load.

### Caching

- Implements strategic caching of frequently accessed short links to improve response times.

### Security

- Securely manages sensitive configurations and sanitizes inputs to prevent vulnerabilities.

## Deployment

- Configurable for different environments (`FLASK_ENV`), supporting both development and production setups.
- Utilizes Flask-Migrate for database migrations, ensuring schema consistency across environments.
- Deployed with Waitress in production environments for enhanced performance.

## Assumptions:

1. **Environment Configuration**: The code assumes that environment variables are set correctly in a `.env` file for different environments (development, production), including `FLASK_ENV` and `BASE_URL`. This is critical for configuring the app and its database connections appropriately.

2. **Database Schema**: It is assumed that the database schema, particularly for `Access`, `SequenceID`, and `ShortURL` models, is already defined and aligns with the operations performed in the code. This affects how sequence IDs are generated, how URLs are shortened, and how accesses are logged.

3. **Unique Identifier Generation**: The approach to generate unique identifiers for short URLs combines timestamp, a random component, and a sequence ID. This assumes that this method produces sufficiently unique values to avoid collisions.

4. **Cache Efficiency**: The code assumes that caching short URL lookups will significantly reduce database load by avoiding repetitive fetches for popular URLs.

5. **Sequential ID Integrity**: There's an implicit assumption that the mechanism to increment and retrieve the next sequence ID from the database is atomic and thread-safe, ensuring unique identifiers are consistently generated even under concurrent access.

## Design Decisions:

1. **Base62 Encoding for Short URLs**: Choosing Base62 encoding (using digits and ASCII letters) for the short codes is a deliberate design choice to keep URLs short and user-friendly, while ensuring a vast space of unique identifiers.

2. **Environment-Specific Configuration**: The decision to configure the application differently based on the `FLASK_ENV` variable allows for flexibility and security, ensuring that development and production environments can be managed separately with appropriate settings.

3. **Use of Flask Extensions**: Leveraging Flask extensions like Flask-Migrate for database migrations, Flask-Caching for caching, and Waitress as a production server indicates a choice for robustness and scalability.

4. **Database-Driven Sequence ID Generation**: Opting for a database-driven approach to generate sequence IDs for unique identifier creation adds a layer of reliability in maintaining uniqueness across generated IDs.

5. **Caching Strategy**: Implementing caching for short URL redirection operations is a strategic decision aimed at optimizing response times and reducing database queries.

6. **Statistics Calculation**: Providing URL access statistics with different time frames (last 24 hours, past week, all time) demonstrates a commitment to offering insightful metrics, which involves calculated queries that consider performance implications.

## Additional Thoughts:

- **Security Considerations**: While not explicitly mentioned, it's vital to consider security aspects such as validating and sanitizing input URLs to prevent injections and other web vulnerabilities.

- **Error Handling**: The code includes basic error responses (e.g., for missing long URLs), but comprehensive error handling throughout the application would be crucial for robustness.

- **Performance Optimization**: The current design decisions around caching and database access aim to optimize performance, but ongoing monitoring and profiling would be necessary to identify and address potential bottlenecks as the application scales.

# ShortURL Service API Documentation

## Overview
This document outlines the API for a ShortURL service developed with Flask. The service provides functionalities to shorten URLs, redirect to the original URLs using their short versions, and gather statistics about URL usage.

### Environment Setup
- The application uses environment variables for configuration, loaded from a `.env` file.
- `FLASK_ENV` determines the running mode of the application (development or production).
- Other relevant environment variables include `DATABASE_URL` for the database connection and `BASE_URL` for constructing short URLs.

### Initialization
- Flask and Flask-Migrate are used for application setup and database migrations.
- A caching mechanism is initialized for optimizing redirects and access statistics.
- The database schema is automatically created on the first request if it does not exist.

## API Endpoints

### POST /shorten
Create a short URL from a given long URL.

- **Payload**: JSON object containing `{"long_url": "http://example.com"}`.
- **Response**: JSON object with `short_url` containing the shortened URL.
- **Status Codes**:
  - 201 Created: Successfully created the short URL.
  - 400 Bad Request: Missing `long_url` in the request body.

### GET /\<short_code>
Redirect to the original URL based on the provided short code.

- **URL Parameter**: `short_code` is the short code part of the URL.
- **Response**: HTTP 302 redirection to the original long URL.
- **Status Codes**:
  - 302 Found: Redirect to the original URL.
  - 404 Not Found: Short code does not exist.

### GET /stats/\<short_code>
Provides statistics for a short URL: accesses in the last 24 hours, past week, and all time.

- **URL Parameter**: `short_code` is the short code part of the URL for which statistics are requested.
- **Response**: JSON object containing statistics about URL accesses.
- **Status Codes**:
  - 200 OK: Successfully retrieved statistics.
  - 404 Not Found: Short code does not exist.

## Running the Application
- For production: The application can be served using Waitress with `serve(app, host='0.0.0.0', port=5000)`.
- For development: The Flask built-in server can be used with `app.run(debug=True)`.

## Dependencies
- Flask for the web framework.
- Flask-Migrate for database migrations.
- Flask-Caching for caching responses.
- Waitress as a production WSGI server.
- Python-dotenv for loading environment variables.

Ensure all dependencies are installed using `pip` to run the application successfully.

## Building and Running the System

To build, run, and test a system based on the provided Python, Flask, and SQLAlchemy setup, follow the documentation outlined below. This guide covers setting up a Python virtual environment, configuring environment variables, installing dependencies, and running the Flask application. Additionally, it includes instructions for migrating database schemas and running the application in different environments.

### Prerequisites

- Python 3.x installed
- PostgreSQL server running (if using PostgreSQL in production)
- Basic knowledge of Python, Flask, and virtual environments

### Clone the repository:


```bash
git clone https://github.com/AsmaKarakra/url-shortner-tool.git
```


# System Build, Run, and Test Documentation

For regular builds, set up a Python virtual environment, configure environment variables, install dependencies, and run the Flask application.

For Docker builds, use docker-compose to build, run, and test the Flask application. Containerization simplifies deployment and ensures consistency across environments.

## Prerequisites

- Python 3.x
- PostgreSQL server (for production use)
- Basic understanding of Python, Flask, and virtual environments

## Step 1: Setting Up a Python Virtual Environment

1. Open a terminal or command prompt.
2. Navigate to your project directory.
3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
## Step 2: Configuring Environment Variables

Ensure your project's environment is correctly configured by creating and populating a `.env` file at the root of your project directory. This file will store crucial variables required for your application's runtime environment.

1. **Create `.env` File:**
   - Navigate to the root of your project directory.
   - Create a new file named `.env`.

2. **Configure Variables:**
   Add the following lines to your `.env` file, adjusting the `DATABASE_URL` with the username and password specific to your PostgreSQL setup. In this example, we use `postgres` as the username and `123456789` as the password.

   ```plaintext
   FLASK_ENV=production
   FLASK_APP = "app/main.py"
   DATABASE_URL=postgresql://postgres:123456789@localhost/postgres
   SECRET_KEY=your_secret_key
   BASE_URL=http://localhost:5000/

## Step 3: Installing Dependencies

Ensure your virtual environment is active, then install the required dependencies:
```bash
pip install -r requirements.txt
```

## Step 4: Database Migration

Set up the database schema before running the application:

1. Execute the database migration commands:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

## Step 5: Running the Application

- **For development**:
  Set `FLASK_ENV=development` in your `.env` file for debug-enabled development mode, then start the application in the root of your project directory:
  ```bash
  flask run
  ```
- **For production**:
  Ensure `FLASK_ENV=production` in your `.env` file, then use `waitress` as a WSGI server, and naviagte to 'app' folder:
  ```bash
   waitress-serve --listen=*:5000 main:app
  ```
  Modify the port number in the curl commands if your application is running on a different port.

## Testing the System

To test the Flask application using curl, we'll focus on the endpoints that are defined in the code. These endpoints include creating a short URL, redirecting to the original (long) URL based on the short code, and getting statistics for a specific short URL. 

Here's how you can test each of these functionalities using curl from the command line:

1. **Testing the Shorten URL Endpoint**

   To test the endpoint that shortens URLs (`/shorten`), you'll need to send a POST request with a JSON payload containing the `long_url` key. Here's an example curl command:

   ```sh
   curl -X POST http://localhost:5000/shorten \
   -H "Content-Type: application/json" \
   -d '{"long_url": "https://www.example.com"}'
   ```

   This command sends a POST request to the `/shorten` endpoint with a JSON body specifying the long URL you want to shorten. Replace `"https://www.example.com"` with the actual URL you want to shorten.

2. **Testing the Redirect to Long URL Endpoint**

   Assuming the previous step provided you with a short code, you can test the redirect functionality by simply accessing the short code path. For example, if the short code is `abcd123`, you would use:

   ```sh
   curl -I http://localhost:5000/abcd123
   ```

   A successful redirect will show a 302 status code followed by a Location header indicating the target URL. Using -I will show the headers only, which is useful for quickly checking the redirect without loading the full content.

3. **Testing the URL Statistics Endpoint**

   To get statistics for a specific short URL, you'll use its short code with the `/stats` endpoint. Assuming the short code is `abcd123`, the curl command would be:

   ```sh
   curl http://localhost:5000/stats/abcd123
   ```

   This sends a GET request to retrieve the access statistics for the short URL associated with the provided short code.

## Additional Notes
- Always activate your virtual environment before working on the project.
- Keep your `.env` file secure and away from version control.
- Adjust database connection strings as per your setup.
- Depending on your Flask configuration and the environment it's running in, you might need to adjust these curl commands, especially the URL part, to match your actual setup.

These curl commands will help you interact with your Flask application from the command line, allowing you to test its functionality without needing a frontend interface.


