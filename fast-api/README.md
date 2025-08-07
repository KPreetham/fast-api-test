# FastAPI Python Demo

A simple FastAPI project with PostgreSQL integration, JWT authentication, and user management.

## Features

- User registration and authentication with JWT tokens
- PostgreSQL database integration
- User posts management
- Random user selection with JWT token generation and verification

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd fastapi-python-demo
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your environment variables:

   **Option A: Generate secure credentials**

   ```bash
   python generate_secret.py
   ```

   This will generate secure JWT secret keys and database passwords.

   **Option B: Use the template**

   ```bash
   cp env_template.txt .env
   ```

   Then edit the `.env` file with your actual values.

   **Required environment variables:**

   ```bash
   # Database Configuration
   DATABASE_URL=postgresql://username:password@localhost:5432/fastapi_demo

   # JWT Configuration
   JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Server Configuration (optional)
   HOST=0.0.0.0
   PORT=8000
   DEBUG=true

   # Database Logging (optional, set to true only for debugging)
   DATABASE_LOGGING=false
   ```

4. Create the PostgreSQL database:

```sql
CREATE DATABASE fastapi_demo;
```

5. Run the database migrations (tables will be created automatically):

```bash
python main.py
```

6. (Optional) Generate mock data for testing:

```bash
# Install additional dependencies
pip install faker

# Generate comprehensive mock data (100 users, 20-50 posts each)
python3 generate_mock_data_auto.py

# Or use interactive version
python3 generate_mock_data.py
```

7. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication

- `POST /signup` - Create a new user account
- `POST /token` - Login and get JWT token

### Main Endpoints

- `GET /random` - Generate random number, create JWT for random user, decode it, and return user's posts
- `GET /users/me` - Get current user information (requires authentication)
- `GET /users/me/posts` - Get all posts for current user (requires authentication)

### API Documentation

- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Usage Examples

### 1. Create a User Account

```bash
curl -X POST "http://localhost:8000/signup" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "name": "John Doe",
       "password": "securepassword123"
     }'
```

### 2. Get JWT Token

```bash
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@example.com&password=securepassword123"
```

### 3. Use the Random Endpoint

```bash
curl -X GET "http://localhost:8000/random"
```

This endpoint will:

1. Generate a random integer from 1-1000
2. Select a random user from the database
3. Create a JWT token for that user
4. Decode the JWT token to verify it
5. Return the user's posts along with the random number and JWT token

### 4. Access Protected Endpoints

```bash
curl -X GET "http://localhost:8000/users/me" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Database Schema

The application uses two main tables:

### Users Table

- `id` - Primary key
- `name` - User's full name
- `email` - Unique email address
- `password` - Hashed password
- `created_at` - Account creation timestamp
- `updated_at` - Last update timestamp

### Posts Table

- `id` - Primary key
- `user_id` - Foreign key to users table
- `title` - Post title
- `content` - Post content
- `created_at` - Post creation timestamp
- `updated_at` - Last update timestamp

## Environment Variables

The application uses environment variables for configuration. Create a `.env` file in the project root with the following variables:

### Required Variables

- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET_KEY` - Secret key for JWT token signing
- `JWT_ALGORITHM` - JWT signing algorithm (default: HS256)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time (default: 30)

### Optional Variables

- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `DEBUG` - Debug mode (default: true)
- `LOG_LEVEL` - Logging level (default: info)
- `DATABASE_LOGGING` - Enable SQL query logging (default: false)

### Security Notes

- Never commit your `.env` file to version control
- Use strong, unique JWT secret keys in production
- Generate secure database passwords
- Use the `generate_secret.py` script to create secure credentials

### Database Logging

To disable SQL query logging (recommended for production), set `DATABASE_LOGGING=false`. Set to `true` only for debugging purposes. When enabled, all SQL queries will be printed to the console.

## Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- Email uniqueness validation
- Input validation using Pydantic schemas
- SQL injection protection with SQLAlchemy ORM
- Environment-based configuration management

## Development

To run the application in development mode with auto-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Mock Data Generation

The project includes comprehensive mock data generation scripts to populate your database with realistic test data:

### Automated Generation

```bash
python3 generate_mock_data_auto.py
```

- Generates 100 users with 20-50 posts each
- No user interaction required
- Clears existing data automatically

### Interactive Generation

```bash
python3 generate_mock_data.py
```

- Customizable number of users and posts
- Interactive prompts for configuration
- Option to preserve existing data

### Generated Data Features

- **Realistic user names and emails** using Faker library
- **Diverse post categories** (Technology, Programming, DevOps, etc.)
- **Varied post content** with different templates and structures
- **Realistic timestamps** spread over the last year
- **Consistent test credentials** (password: `password123`)

### Sample Output

```
🎉 Mock data generation completed!
   📊 Total users: 100
   📝 Total posts: 3,450
   📈 Average posts per user: 34.5

🔐 Test Credentials:
   Email: john.doe@example.com
   Password: password123
```

## Testing

You can test the API endpoints using the interactive documentation at `http://localhost:8000/docs` or using tools like curl, Postman, or any HTTP client.
