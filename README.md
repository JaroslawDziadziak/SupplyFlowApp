# SupplyFlowApp

A web application for managing supply chain tickets and orders within an organization.
Built as a full-stack project using Django REST Framework and Vue.js.

---

## Tech Stack

**Backend**
- Python 3.11
- Django 5.2
- Django REST Framework 3.14
- PostgreSQL
- Simple JWT (token-based authentication)

**Frontend**
- Vue.js 3 (Composition API)
- Vue Router
- Axios
- Vite

---

## Features

- **User registration and login** with role-based access (Logistics, Project Manager, Engineer, Other)
- **JWT authentication** — secure token-based sessions
- **Ticket management** — create, view, edit, and filter support tickets
- **Ticket assignment** — assign tickets to specific users
- **Comments** — add comments to tickets for team communication
- **Filters** — view all tickets, tickets you created, or tickets assigned to you
- **Role display** — each user sees their role in the sidebar

---

## Project Structure

SupplyFlowApp/
├── config/          # Django settings, URLs, WSGI
├── tickets/         # Main Django app (models, views, serializers, URLs)
├── frontend/        # Vue.js application
│   ├── src/
│   │   ├── views/       # LoginView, RegisterView, TicketsView
│   │   ├── components/  # Reusable Vue components
│   │   ├── services/    # Axios API client (api.js)
│   │   └── router/      # Vue Router configuration
├── .env             # Environment variables (not committed)
├── manage.py
└── requirements.txt

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL

### Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Create a .env file in the project root with the following variables:
# DB_NAME=supplyflow_db
# DB_USER=postgres
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432
# SECRET_KEY=your_secret_key
# DEBUG=True

# Run database migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the Django development server
python manage.py runserver

---

Frontend Setup

cd frontend

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
The application will be available at:

#Frontend: http://localhost:5173
#Backend API: http://localhost:8000/api

API Endpoints
Method	Endpoint	Description
#POST	/api/token/	Obtain JWT token pair
#POST	/api/token/refresh/	Refresh access token
#POST	/api/register/	Register new user
#GET	/api/me/	Get current user info
#GET/POST	/api/tickets/	List or create tickets
#GET/PATCH	/api/tickets/{id}/	Retrieve or update ticket
#GET/POST	/api/comments/	List or create comments
#GET	/api/users/	List all users

Author
Jaroslaw Dziadziak


