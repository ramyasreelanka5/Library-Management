# Library Management System Pro

## Enhanced Professional Library Management System

A comprehensive library management solution built with Django and MySQL, featuring role-based access control, modern UI, and advanced features.

## Features

### Multi-User Roles
- **Admin**: Full system access and configuration
- **Librarian**: Book management, issue/return, fine collection
- **Student**: Self-service portal, book browsing, account management

### Core Functionality
- Book Management (Categories, Authors, Publishers)
- Issue/Return Tracking with Renewals
- Automated Fine Calculation
- Real-time Availability Status
- Search and Filtering
- Comprehensive Reports

### Advanced Features
- Role-based dashboards with statistics
- Book reservation system
- Audit logging
- Notification system
- Book reviews and ratings
- Modern responsive UI

## Tech Stack

- **Backend**: Django 6.0.2
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Authentication**: Django Auth with Custom Profiles

## Setup Instructions

### 1. Install Dependencies
```bash
cd "c:\Users\ramya\Downloads\project (2)\library_system_pro"
python -m pip install -r requirements.txt
```

### 2. Create Database
```bash
python create_database.py
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Create Users
```bash
python create_superuser.py
```

This creates:
- Admin: admin/admin123
- Librarian: librarian/lib123
- Student: student/stu123

### 5. Add Demo Data (Optional)
```bash
python populate_demo_data.py
```

### 6. Run Server
```bash
python manage.py runserver
```

### 7. Access Application
Open: http://127.0.0.1:8000/

## Default Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Librarian | librarian | lib123 |
| Student | student | stu123 |

## Database Schema

### Core Tables
- `user_profiles` - Extended user information with roles
- `books` - Book catalog with ISBN, authors, categories
- `book_categories` - Book categorization
- `authors` - Author information
- `publishers` - Publisher details
- `issues` - Book borrowing records
- `fines` - Fine/penalty tracking
- `reservations` - Book reservation queue
- `notifications` - User notifications
- `audit_logs` - System activity logs
- `book_reviews` - Student reviews

## Project Structure

```
library_system_pro/
├── library/                 # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin configuration
│   └── utils.py            # Utility functions
├── templates/              # HTML templates
│   ├── base.html          # Base template with CSS
│   ├── dashboard_*.html   # Role-based dashboards
│   ├── books/             # Book templates
│   ├── issues/            # Issue management
│   ├── fines/             # Fine management
│   └── student/           # Student portal
├── static/                 # Static files
├── media/                  # Uploaded files
├── create_database.py      # DB setup script
└── create_superuser.py     # User creation script
```

## Usage

### For Librarians
1. Login with librarian credentials
2. Add books via "Add New Book"
3. Issue books to students
4. Process returns and collect fines
5. View reports and statistics

### For Students
1. Register or login
2. Browse available books
3. View issued books and due dates
4. Check fine status
5. Renew books (if eligible)

## Features Highlight

- ✅ Role-based Access Control
- ✅ Modern Responsive Design
- ✅ Real-time Statistics Dashboard
- ✅ Advanced Search & Filtering
- ✅ Automated Fine Calculation
- ✅ Book Renewal System
- ✅ Comprehensive Reports
- ✅ Audit Logging
- ✅ Professional UI/UX

## Future Enhancements

- Email notifications
- Barcode/QR scanning
- Data visualization with Chart.js
- Export to Excel/PDF
- API endpoints
- Mobile app

## License

Educational/Portfolio Project

## Author

Created as an enhanced version of College Library Management System for professional showcase.
