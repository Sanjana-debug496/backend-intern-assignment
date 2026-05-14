# Backend Application - Project Documentation

Django REST Framework backend application with Celery task queue integration, JWT authentication, PostgreSQL database, and Redis caching.


## Project Overview

This backend application provides:
- **User Authentication**: Custom user model with email-based authentication using JWT tokens
- **Paragraph Management**: Create and manage text paragraphs
- **Text Search**: Search for words within paragraphs with frequency counting
- **Asynchronous Processing**: Celery integration for background task processing
- **RESTful API**: Complete REST API for all operations
- **Database**: PostgreSQL for persistent storage
- **Caching**: Redis for caching and Celery message broker

---


## Project Setup Instructions

#### Step 1: created a folder
```bash
cd Backend_app
```

#### Step 2: Created Virtual Environment
```bash
# Create virtual environment
python -m venv env

# Activate on Windows (Command Prompt)
env\Scripts\activate

#### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r server/requirements.txt
```

#### Step 4: Set Up Database
```bash
# Ensure PostgreSQL is running locally
# Create database
createdb backend_db

# Or using psql
psql -U postgres
CREATE DATABASE backend_db;
```

#### Step 5: Run Migrations
```bash
cd server
python manage.py migrate
```

#### Step 6: Created Superuser
```bash
python manage.py createsuperuser
```

#### Step 7: Start Redis (in new terminal)
```bash
# Windows with WSL or Docker
docker run -d -p 6379:6379 redis:7
```

#### Step 8: Start Celery Worker (in new terminal with venv activated)
```bash
cd server
celery -A server worker -l info
```

#### Step 9: Start Development Server (in another terminal with venv activated)
```bash
cd server
python manage.py runserver
```

API available at: `http://localhost:8000/`

---

### Option 2: Docker Setup (Recommended)

#### Step 1: Build & Start Services
```bash
# Navigate to project root
cd Backend_app

# Start all services
docker-compose up -d

# Or rebuild images
docker-compose up -d --build
```

Services will be available at:
- Web Server: `http://localhost:8000`
- Database: `localhost:5432`
- Redis: `localhost:6379`

#### Step 2: Run Migrations in Container
```bash
docker-compose exec web python manage.py migrate
```

#### Step 3: Create Superuser
```bash
docker-compose exec web python manage.py createsuperuser

```

#### Step 4: Stop Services
```bash
docker-compose down
```

---

## API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication
This API uses JWT (JSON Web Token) authentication. All protected endpoints require:
```
Authorization: Bearer <access_token>
```

---

### User Endpoints

#### 1. Register User
**Endpoint:** `POST /api/users/register/`

**Description:** Create a new user account

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password123",
  "name": "John Doe",
  "date_of_birth": "1990-01-15"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
  "email": ["This field may not be blank."],
  "password": ["This field may not be blank."]
}
```

---

#### 2. Login User (Get JWT Token)
**Endpoint:** `POST /api/users/login/`

**Description:** Authenticate user and receive JWT tokens

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password123"
}
```

**Response (200 OK):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Usage:**
- Use `access` token in Authorization header for API requests
- Use `refresh` token to get new access token when it expires

---

### Paragraph Endpoints

#### 1. Create Paragraph(s)
**Endpoint:** `POST /api/paragraphs/create/`

**Authentication:** Required ✓

**Description:** Create one or more paragraphs from text. Paragraphs separated by double line breaks (`\n\n`)

**Request Body:**
```json
{
  "text": "This is the first paragraph.\n\nThis is the second paragraph.\n\nThis is the third paragraph."
}
```

**Response (201 Created):**
```json
{
  "message": "Paragraphs stored successfully",
  "paragraphs": [
    "This is the first paragraph.",
    "This is the second paragraph.",
    "This is the third paragraph."
  ]
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Text is required"
}
```

**Notes:**
- Each paragraph triggers a background Celery task for word frequency analysis
- Only authenticated users can create paragraphs
- Paragraphs are associated with the authenticated user

---

#### 2. Search Word in Paragraphs
**Endpoint:** `GET /api/paragraphs/search/?word=<search_word>`

**Authentication:** Required ✓

**Description:** Search for a word across user's paragraphs and get frequency count

**Query Parameters:**
- `word` (required): The word to search for

**Example Request:**
```
GET /api/paragraphs/search/?word=the
```

**Response (200 OK):**
```json
[
  {
    "paragraph": "This is the first paragraph with the word repeated.",
    "count": 2
  },
  {
    "paragraph": "Another paragraph containing the searched word.",
    "count": 1
  }
]
```

**Notes:**
- Search is case-insensitive
- Results are sorted by frequency (highest first)
- Only top 10 results are returned
- Searches only within user's own paragraphs

---

## Code Documentation

### Project Structure
```
Backend_app/
├── env/                          # Virtual environment
├── server/
│   ├── manage.py                # Django CLI
│   ├── requirements.txt          # Dependencies
│   ├── Dockerfile               # Docker configuration
│   ├── docker-compose.yml       # Docker Compose setup
│   │
│   ├── server/                  # Main Django project
│   │   ├── settings.py          # Django settings
│   │   ├── urls.py              # Main URL routing
│   │   ├── celery.py            # Celery configuration
│   │   ├── asgi.py              # ASGI configuration
│   │   └── wsgi.py              # WSGI configuration
│   │
│   ├── users/                   # User authentication app
│   │   ├── models.py            # User model
│   │   ├── serializers.py       # Request/response serializers
│   │   ├── views.py             # View controllers
│   │   ├── urls.py              # User URL routes
│   │   └── migrations/          # Database migrations
│   │
│   └── paragraphs/              # Paragraph management app
│       ├── models.py            # Paragraph model
│       ├── serializers.py       # Serializers
│       ├── views.py             # View controllers
│       ├── tasks.py             # Celery tasks
│       ├── urls.py              # Paragraph URL routes
│       └── migrations/          # Database migrations
```

---

## Database Models

### CustomUser Model
**Location:** `users/models.py`

**Purpose:** Custom user model with email-based authentication

**Fields:**
| Field | Type | Required | Unique | Notes |
|-------|------|----------|--------|-------|
| email | EmailField | Yes | Yes | Primary identifier, replaces username |
| name | CharField(255) | Yes | No | Full name of the user |
| date_of_birth | DateField | Yes | No | User's date of birth |
| password | - | Yes | No | Automatically hashed by Django |
| created_date | DateTimeField | No | No | Auto-set on creation |
| modified_date | DateTimeField | No | No | Auto-updates on save |
| is_staff | BooleanField | No | No | Admin access flag |
| is_superuser | BooleanField | No | No | Superuser flag |

**Manager:** `CustomUserManager`
- `create_user(email, password, **extra_fields)` - Create regular user
- `create_superuser(email, password, **extra_fields)` - Create admin user

**Example Usage:**
```python
user = CustomUser.objects.create_user(
    email="john@example.com",
    password="secure_pass",
    name="John Doe",
    date_of_birth="1990-01-15"
)
```

---

### Paragraph Model
**Location:** `paragraphs/models.py`

**Purpose:** Store text paragraphs associated with users

**Fields:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| user | ForeignKey(CustomUser) | Yes | Associated user (CASCADE delete) |
| content | TextField | Yes | The paragraph text content |
| created_date | DateTimeField | No | Auto-set on creation |

**Relationships:**
- Belongs to: `CustomUser` (one-to-many)
- When user is deleted, all their paragraphs are deleted

**Methods:**
- `__str__()` - Returns first 50 characters of content

**Example Usage:**
```python
paragraph = Paragraph.objects.create(
    user=request.user,
    content="This is a sample paragraph text."
)
```

---

## Views & Serializers

### User Serializers
**Location:** `users/serializers.py`

#### RegisterSerializer
**Purpose:** Validate and process user registration

**Fields:**
- `email` - User email (unique, required)
- `password` - User password (write-only, required)
- `name` - User full name (required)
- `date_of_birth` - User birth date (required)

**Methods:**
- `create(validated_data)` - Creates CustomUser with hashed password

#### CustomTokenObtainPairSerializer
**Purpose:** Extended JWT token serializer with email field

**Features:**
- Uses email as username field instead of username
- Returns access and refresh tokens

---

### Paragraph Serializer
**Location:** `paragraphs/serializers.py`

#### ParagraphSerializer
**Purpose:** Serialize/deserialize Paragraph model

**Fields:**
- `id` - Paragraph ID (read-only)
- `content` - Paragraph text
- `created_date` - Creation timestamp (read-only)

---

### User Views
**Location:** `users/views.py`

#### RegisterView
**HTTP Method:** POST

**Purpose:** Handle user registration

**Request:** RegisterSerializer data

**Response:** 
- Success (201): `{"message": "User registered successfully"}`
- Error (400): Validation errors

**Code:**
```python
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
```

#### CustomLoginView
**HTTP Method:** POST

**Purpose:** Authenticate user and return JWT tokens

**Parent:** TokenObtainPairView (from rest_framework_simplejwt)

**Serializer:** CustomTokenObtainPairSerializer

**Response:**
```json
{
  "refresh": "token_string",
  "access": "token_string"
}
```

---

### Paragraph Views
**Location:** `paragraphs/views.py`

#### ParagraphCreateView
**HTTP Method:** POST  
**Authentication:** Required ✓  
**Permission:** IsAuthenticated

**Purpose:** Create one or more paragraphs from text input

**Request Format:**
```json
{
  "text": "paragraph1\n\nparagraph2\n\nparagraph3"
}
```

**Logic:**
1. Extract `text` from request data
2. Split text by double line breaks (`\n\n`)
3. For each non-empty paragraph:
   - Strip whitespace
   - Create Paragraph object associated with user
   - Trigger async Celery task `process_paragraph.delay()`
4. Return created paragraphs

**Response (201):**
```json
{
  "message": "Paragraphs stored successfully",
  "paragraphs": ["para1", "para2"]
}
```

**Code:**
```python
class ParagraphCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        text = request.data.get('text')
        if not text:
            return Response(
                {"error": "Text is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        paragraphs = text.split('\n\n')
        created_paragraphs = []
        
        for para in paragraphs:
            para = para.strip()
            if para:
                paragraph = Paragraph.objects.create(
                    user=request.user,
                    content=para
                )
                process_paragraph.delay(para)
                created_paragraphs.append(paragraph.content)
        
        return Response(
            {
                "message": "Paragraphs stored successfully",
                "paragraphs": created_paragraphs
            },
            status=status.HTTP_201_CREATED
        )
```

---

#### SearchWordView
**HTTP Method:** GET  
**Authentication:** Required ✓  
**Permission:** IsAuthenticated

**Purpose:** Search for word occurrences in user's paragraphs

**Query Parameters:**
- `word` (required) - Word to search for

**Logic:**
1. Get `word` parameter from query string
2. Retrieve all paragraphs for authenticated user
3. For each paragraph:
   - Convert to lowercase and split into words
   - Count occurrences of search word
   - If found, add to results with paragraph text and count
4. Sort results by count (descending)
5. Return top 10 results

**Response (200):**
```json
[
  {
    "paragraph": "text content",
    "count": 3
  }
]
```

**Code:**
```python
class SearchWordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        word = request.GET.get('word')
        if not word:
            return Response(
                {"error": "Word parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        paragraphs = Paragraph.objects.filter(user=request.user)
        result = []
        
        for para in paragraphs:
            words = para.content.lower().split()
            count = words.count(word.lower())
            
            if count > 0:
                result.append({
                    "paragraph": para.content,
                    "count": count
                })
        
        result = sorted(
            result,
            key=lambda x: x['count'],
            reverse=True
        )
        top_10 = result[:10]
        
        return Response(top_10)
```

---

## Celery Tasks

### Overview
Location: `paragraphs/tasks.py`

Celery is configured for asynchronous task processing. The message broker and result backend are configured to use Redis.

---

### process_paragraph Task

**Purpose:** Asynchronously process paragraphs to calculate word frequency

**Decorator:** `@shared_task`

**Input:**
- `text` (str) - The paragraph text to process

**Output:**
- Returns a dictionary with word frequencies

**Processing Steps:**
1. Convert text to lowercase
2. Split text into individual words
3. Count occurrences of each word
4. Return frequency dictionary

**Example:**
```python
# Input
process_paragraph("hello world hello python world")

# Output
{
  "hello": 2,
  "world": 2,
  "python": 1
}
```

**Code:**
```python
@shared_task
def process_paragraph(text):
    words = text.lower().split()
    frequency = {}
    
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    
    print("Word Frequency:", frequency)
    return frequency
```

**How It's Used:**
- Called asynchronously when creating paragraphs: `process_paragraph.delay(para)`
- Doesn't block the HTTP response
- Results printed to console/logs

---

### Running Celery

**Start Worker:**
```bash
cd server
celery -A server worker -l info
```

**Monitoring with Flower (Optional):**
```bash
pip install flower
celery -A server flower
```
Then visit `http://localhost:5555` to monitor tasks

---

## Common Issues

### Issue: PostgreSQL Connection Error
**Solution:** 
```bash
# Check if PostgreSQL is running
# Windows: Ensure PostgreSQL service is started
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql

# Verify credentials in settings.py
```

### Issue: Redis Connection Error
**Solution:**
```bash
# Start Redis service
docker run -d -p 6379:6379 redis:7
# Or on macOS: redis-server
```

### Issue: Celery Tasks Not Processing
**Solution:**
```bash
# Ensure Celery worker is running
celery -A server worker -l info

# Check Redis is running and accessible
redis-cli ping  # Should return PONG
```

### Issue: Port Already in Use
**Solution:**
```bash
# For port 8000
python manage.py runserver 0.0.0.0:8001

# For port 5432 (PostgreSQL)
# Kill the process using it or use different port
```

### Issue: Virtual Environment Not Activating
**Solution:**
```bash
# Windows Command Prompt
env\Scripts\activate.bat

# Windows PowerShell
env\Scripts\Activate.ps1

# macOS/Linux
source env/bin/activate
```

---

## Environment Variables

Create `.env` file in project root (optional):
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=backend_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
```

---

## Useful Django Commands

```bash
# Create new Django app
python manage.py startapp app_name

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Revert migrations
python manage.py migrate app_name 0001

# Database shell
python manage.py dbshell

# Django shell
python manage.py shell

# Check project health
python manage.py check

# Collect static files
python manage.py collectstatic

# Flush database (DELETE ALL DATA)
python manage.py flush
```

---

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test paragraphs

# Run specific test class
python manage.py test users.tests.RegisterViewTests

# Verbose output
python manage.py test --verbosity=2
```

---

## Deployment Checklist

Before deploying to production:

- [ ] Set `DEBUG = False` in settings.py
- [ ] Update `SECRET_KEY` to a strong random value
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Use environment variables for sensitive data
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure database backups
- [ ] Set up logging and monitoring
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Configure CORS if needed
- [ ] Test database migrations thoroughly
- [ ] Set up CI/CD pipeline
- [ ] Plan for database optimization

---

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and test thoroughly
3. Commit with clear messages: `git commit -m "Add feature description"`
4. Push to repository: `git push origin feature/your-feature`
5. Create a Pull Request

---

