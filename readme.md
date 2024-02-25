# Flask-Based URL Shortener Service

## Introduction

A Flask-based URL shortener service designed to offer functionalities for shortening URLs, redirecting to original URLs via short links, and tracking URL access statistics.

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

      - Additionally, the user is operating the application on a Windows OS, and the database server has been properly set up and is currently running without issues. 

2. **Database Schema**: It is assumed that the database schema, particularly for `Access`, `SequenceID`, and `ShortURL` models, is already defined and aligns with the operations performed in the code. This affects how sequence IDs are generated, how URLs are shortened, and how accesses are logged.

3. **Unique Identifier Generation**: The approach to generate unique identifiers for short URLs combines timestamp, a random component, and a sequence ID. This assumes that this method produces sufficiently unique values to avoid collisions.

4. **Cache Efficiency**: The code assumes that caching short URL lookups will significantly reduce database load by avoiding repetitive fetches for popular URLs.

5. **Sequential ID Integrity**: There's an implicit assumption that the mechanism to increment and retrieve the next sequence ID from the database is atomic and thread-safe, ensuring unique identifiers are consistently generated even under concurrent access.

6. **Base URL**: For the sake of simplicity, the base URL for constructing the short URL is set to the local host.

7. **Proximity to Servers**: Assume users are geographically close to your servers or edge nodes (CDN), minimizing the impact of physical distance on latency.

8. **High-Speed Internet**: Assume users have access to high-speed internet connections with low latency.

9. **Modern Hardware**: Assume users are on modern devices capable of quickly processing redirects and loading web content.

## Design Decisions:

1. Base62 Encoding for Short URLs

   Pros:

   - Compactness: Base62 encoding maximizes the use of a short URL length, making it easier to share and remember.
   - High Cardinality: Offers a large space of possible combinations, ensuring a vast number of unique identifiers.
   - URL-Friendly: Excludes characters that can cause issues in URLs, enhancing compatibility.

   Cons:

   - Case Sensitivity: May lead to confusion due to the similarity between some uppercase and lowercase letters.
   - Limited to ASCII: Restricts the encoding to ASCII characters, not leveraging the full range of Unicode characters.

   Alternatives:

   - Base58 Encoding: Excludes similar-looking characters (like 0OIl) to reduce user error.
   - Hashing: Using a hash function to generate parts of the URL, though it may require a lookup table to resolve collisions.

2. Environment-Specific Configuration

   Pros:

   - Security: Allows for stronger security settings in production versus more accessible settings in development.
   - Flexibility: Developers can test new features in development without affecting the production environment.
   - Customization: Enables environment-specific optimizations, like database connections and caching strategies.

   Cons:

   - Complexity: Managing different configurations can increase complexity and the risk of errors if not managed carefully.
   - Potential for Misconfiguration: There's a risk of deploying with the wrong configuration, leading to potential security vulnerabilities.

   Alternatives:

   - Containerization: Using Docker or similar technologies to encapsulate environment settings.
   - Feature Flags: Enabling or disabling features at runtime without relying on environment variables.

3. Use of Flask Extensions

   Pros:

      - Rapid Development: Extensions provide out-of-the-box solutions for common tasks, speeding up the development process.
      - Community Support: Popular extensions are well-documented and supported by the community.
      - Integration: Designed to integrate seamlessly with Flask, ensuring compatibility and stability.

      Cons:

      - Dependency Overhead: Relying on multiple extensions can lead to dependency management challenges.
      - Potential for Bloat: Incorporating too many extensions can make the application bloated and harder to maintain.

      Alternatives:

      - Custom Implementations: Developing in-house solutions tailored to specific requirements, offering more control but requiring more effort.
      - Minimalist Frameworks: Exploring lighter alternatives to Flask that come with fewer built-in features but potentially lower overhead.

4. Database-Driven Sequence ID Generation

   Pros:

   - Reliability: Ensures unique identifiers are generated reliably, avoiding collisions.
   - Scalability: Can handle high volumes of requests with proper database optimizations.
   - Atomicity: Database transactions ensure the atomicity of ID generation, preventing duplicate IDs.

   Cons:

   - Performance Bottleneck: Can become a bottleneck under heavy load, affecting performance.
   - Database Dependency: Tightly couples the URL generation process to the database, potentially affecting flexibility.

   Alternatives:

   - Distributed Unique ID Generators: Solutions like Twitter's Snowflake or Sony's Flake can generate unique IDs in a distributed environment without heavy reliance on a central database.
   - UUIDs: Using universally unique identifiers (UUIDs) can avoid the need for sequential IDs, though they are longer.

5. Caching Strategy

   Pros:

   - Performance Improvement: Significantly reduces response times by avoiding repeated database queries.
   - Scalability: Helps the application scale by reducing the load on the database.
   - Cost-Effective: Can reduce operational costs by requiring fewer resources to handle the same load.

   Cons:

   - Consistency Issues: Cached data may become stale, leading to inconsistencies.
   - Complexity: Implementing and managing cache invalidation strategies adds complexity.

   Alternatives:

   - Content Delivery Networks (CDNs): Using CDNs to cache and serve static and dynamic content at the edge, closer to users.
   - In-Memory Data Stores: Technologies like Redis or Memcached can offer faster access times and sophisticated eviction policies.

6. Statistics Calculation

   Pros:

      - User Engagement: Offers valuable insights into user behavior, which can inform future improvements.
      - Performance Optimization: Careful query optimization can ensure that statistics are generated efficiently without impacting overall performance.
      - Customizability: Allows for flexible time frames and metrics tailored to specific needs.

      Cons:

      - Resource Intensive: Complex queries can be resource-intensive, especially on large datasets.
      - Potential for Slowdowns: If not optimized, statistics calculation can slow down application response times.

      Alternatives:

      - Asynchronous Processing: Calculating statistics in the background and updating them periodically to reduce load on the main application thread.
      - Third-Party Analytics: Leveraging external analytics services to offload the computation and storage of usage statistics.


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

- [Python 3.x](https://www.python.org/downloads/) installed
- [PostgreSQL](https://www.postgresql.org/) server running
- Basic knowledge of Python, Flask, and virtual environments

### Clone the repository:


```bash
git clone https://github.com/AsmaKarakra/url-shortner-tool.git
```


# System Build, Run, and Test Documentation

## Prerequisites

- Python 3.x
- PostgreSQL server (for production use)
- Basic understanding of Python, Flask, and virtual environments

## Step 1: Setting Up a Python Virtual Environment

1. Open a terminal or command prompt.
2. Navigate to your project directory.
3. Create a virtual environment:
   ```bash
   python -m venv venv
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
  Ensure `FLASK_ENV=production` in your `.env` file, then use `waitress` as a WSGI server. 
  
  naviagte to 'app' folder:
   ```bash
   cd app
  ```
  Run the following command in your powershell terminal: 
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

4. **Testing Database Presistance**
   1. Ensure your coressponding PostgreSQL server is running 
   2.   Ensure `FLASK_ENV=production` in your `.env` file, then use `waitress` as a WSGI server. 
  
         naviagte to 'app' folder:
         ```bash
            cd app
         ```

         Run the following command in your powershell terminal: 
         ```bash
            waitress-serve --listen=*:5000 main:app
         ```
         Modify the port number in the curl commands if your application is running on a different port.
      

      3. Assuming the first two tests passed, you can test the presistance by using the redirect functionality by simply accessing the short code path. For example, if the short code is `abcd123`, you would use:

         ```sh
         curl -I http://localhost:5000/abcd123
         ```

## Additional Notes
- Always activate your virtual environment before working on the project.
- Keep your `.env` file secure and away from version control.
- Adjust database connection strings as per your setup.
- Depending on your Flask configuration and the environment it's running in, you might need to adjust these curl commands, especially the URL part, to match your actual setup.



