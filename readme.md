# Short URL Management RESTful API

The challenge is to build a HTTP-based RESTful API for managing Short URLs and redirecting clients similar to bit.ly or goo.gl. The system must support millions of short URLs while ensuring reliability and performance. This README provides documentation on how to build, run, and test the system, along with stating assumptions and design decisions.

## Requirements

A Short URL:
1. Has one long URL.
2. Is permanent; once created, it remains unchanged.
3. Is unique; if a long URL is added twice, it should result in two different short URLs.
4. Is not easily discoverable; incrementing an already existing short URL should have a low probability of finding a working short URL.

Solution must support:
1. Generating a short URL from a long URL.
2. Redirecting a short URL to a long URL within 10 ms.
3. Listing the number of times a short URL has been accessed in the last 24 hours, past week, and all time.
4. Persistence (data must survive computer restarts).
5. System must eventually support millions of short urls

Shortcuts:
1. No authentication is required.
2. No HTML or web UI is required.
3. Transport/Serialization format is your choice, but the solution should be testable via curl.

## Implementation

### Technologies Used
- Flask for building the RESTful API.
- SQLAlchemy for ORM (Object-Relational Mapping) to interact with the database.
- SQLite for the database to ensure persistence.
- Python for server-side logic and business rules.

### Assumptions and Design Decisions
1. **Database Choice**: SQLite was chosen for testing due to its simplicity and ease of use. However, it may not be suitable for large-scale applications. When scaling to production grade, switching to a more robust database like PostgreSQL has been implmeented. 
2. **Short URL Generation**: SHA-256 hash of the long URL is used to generate a short code. While this provides uniqueness and security, it may not be the most efficient method for generating short URLs at scale. Consideration should be given to implementing a more optimized algorithm.
3. **Redirection Performance**: To ensure redirection within 10 ms, caching mechanisms or a highly efficient lookup algorithm should be implemented. Additionally, the server infrastructure must be optimized for low-latency responses.
4. **Access Statistics**: Access statistics are stored in the database for each short URL. However, retrieving statistics for millions of short URLs may impact performance. Consideration should be given to optimizing database queries or implementing caching mechanisms.
5. **API Documentation**: Detailed API documentation should be provided using tools like Swagger or OpenAPI to facilitate understanding and usage of the API.

## Building and Running the System

1. Clone the repository:

```bash
git clone <repository_url>

