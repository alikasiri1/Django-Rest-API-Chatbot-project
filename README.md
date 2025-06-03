# Django Chatbot With Rest API

A Django-based API for a chatbot using Cohere API with authentication features.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file in the root directory with the following variables:
```
COHERE_API_KEY=your_cohere_api_key
SECRET_KEY=your_django_secret_key
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- POST /api/auth/register/ - Register a new user
- POST /api/auth/login/ - Login and get JWT tokens
- POST /api/auth/refresh/ - Refresh JWT token

### Chatbot
- POST /api/chat/ - Send a message to the chatbot
- GET /api/chat/history/ - Get chat history for the authenticated user 

## documantaion 
https://documenter.getpostman.com/view/36760752/2sB2qi8Hzc
