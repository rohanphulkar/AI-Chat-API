# AI Chat Application

The AI Chat Application is a web-based chat application powered by artificial intelligence. It allows users to have interactive conversations with an AI-powered chatbot.

## Features

- User Registration: Users can register an account to access the chat application.
- AI Chatbot: Users can engage in conversations with the AI-powered chatbot.
- Chat History: Chat history is stored, allowing users to view previous conversations.
- Profile Management: Users can manage their profiles and update personal information.

## Technologies Used

- Python
- Django: Web framework used for building the backend server.
- Django REST Framework: Toolkit for building RESTful APIs.
- OpenAI: AI platform used for natural language processing and chatbot capabilities.
- Stripe: Payment processing API used for handling payment transactions.
- PostgreSQL: Relational database management system for data storage.
- Docker: Containerization platform for easy deployment and scalability.

## Installation

1. Clone the repository:

```
git clone https://github.com/rohanphulkar/AI-Chat-API.git
```

2. Navigate to the project directory:

```
cd AI-Chat-API
```

3. Create a virtual environment:

```
python -m venv venv
```

4. Activate the virtual environment:

```
source venv/bin/activate  # for Linux/Mac
venv\Scripts\activate  # for Windows
```

5. Install the dependencies:

```
pip install -r requirements.txt
```

6. Set up environment variables:

- Create a .env file in the project's root directory.
- Add the following environment variables:

```
SECRET_KEY=<your_secret_key>
OPENAI_API_KEY=<your_openai_api_key>
STRIPE_API_KEY=<your_stripe_api_key>
```

7. Migrate the database:

```
python manage.py migrate
```

8. Run the development server:

```
python manage.py runserver
```

9. Access the application at http://localhost:8000.

## API Endpoints

- **Registration**: `/accounts/register/` [POST]
- **Email Verification**: `/accounts/verify/<token>/` [GET]
- **Login**: `/accounts/login/` [POST]
- **Forgot Password**: `/accounts/forgot-password/` [POST]
- **Reset Password**: `/accounts/reset-password/<token>/` [POST]
- **Change Password**: `/accounts/change-password/` [POST]
- **User Profile**: `/profile/` [GET]
- **Checkout**: `/profile/checkout/` [POST]
- **Chat History**: `/chat/` [GET]
- **Chat**: `/chat/` [POST]
