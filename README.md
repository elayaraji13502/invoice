# Invoice Hub - Automated Invoice Processing System

A professional invoice management and processing system with role-based access control.

## Features

- 🔐 **Secure Authentication** with JWT tokens and bcrypt password hashing
- 👥 **Role-Based Access** (Admin and Reviewer roles)
- 📊 **Admin Dashboard** for user management and system monitoring
- 📋 **Invoice Review Queue** for efficient invoice processing
- 📈 **Analytics & Reporting** for business insights
- 🎨 **Modern UI** built with React, TypeScript, and Tailwind CSS
- 🗄️ **Database Integration** with PostgreSQL and SQLAlchemy

## Tech Stack

### Frontend
- React 18.3.1 with TypeScript
- Vite for fast development
- Tailwind CSS for styling
- shadcn/ui for components
- React Router for navigation
- TanStack Query for state management

### Backend
- FastAPI for REST API
- PostgreSQL for database
- SQLAlchemy for ORM
- JWT for authentication
- bcrypt for password hashing

## Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+ and pip
- PostgreSQL database

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/subha19012005/Invoice-Analyzer.git
   cd Invoice-Analyzer
   ```

2. **Backend Setup**
   ```bash
   # from project root
   python -m venv venv
   venv\Scripts\activate
   pip install -r req.txt
   cd backend
   python main.py
   ```

3. **Frontend Setup**
   ```bash
   npm install
   npm run dev
   ```

### Default Credentials
- **Admin**: username `admin`, password `admin123`
- **Reviewer**: username `reviewer`, password `reviewer123`

## Project Structure

```
invoice-hub/
├── backend/                 # FastAPI backend
│   ├── main.py            # Application entry point
│   ├── models.py          # Database models
│   ├── routes/            # API routes
│   └── database.py        # Database configuration
├── src/                   # React frontend
│   ├── components/         # Reusable components
│   ├── pages/             # Page components
│   ├── hooks/             # Custom hooks
│   ├── services/          # API services
│   └── types/             # TypeScript types
└── public/                # Static assets
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Backend Python Dependencies

This project uses `req.txt` as the Python dependency lock file.

Install backend dependencies:

```bash
# from project root
venv\Scripts\activate
pip install -r req.txt
```

If dependencies are changed, update `req.txt`:

```bash
venv\Scripts\activate
pip freeze > req.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

The only requirement is having Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

Follow these steps:

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory.
cd <YOUR_PROJECT_NAME>

# Step 3: Install the necessary dependencies.
npm i

# Step 4: Start the development server with auto-reloading and an instant preview.
npm run dev
```

**Edit a file directly in GitHub**

- Navigate to the desired file(s).
- Click the "Edit" button (pencil icon) at the top right of the file view.
- Make your changes and commit the changes.

**Use GitHub Codespaces**

- Navigate to the main page of your repository.
- Click on the "Code" button (green button) near the top right.
- Select the "Codespaces" tab.
- Click on "New codespace" to launch a new Codespace environment.
- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

## How can I deploy this project?

Simply open [Lovable](https://lovable.dev/projects/REPLACE_WITH_PROJECT_ID) and click on Share -> Publish.

## Can I connect a custom domain to my Lovable project?

Yes, you can!

To connect a domain, navigate to Project > Settings > Domains and click Connect Domain.

Read more here: [Setting up a custom domain](https://docs.lovable.dev/features/custom-domain#custom-domain)
