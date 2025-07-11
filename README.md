# User Management System

A comprehensive Django-based user management system with robust authentication features.

## Features

- User registration with email verification
- User login/logout
- Password reset via email
- Welcome email after successful verification
- Profile management (view/update profile)
- Admin user management
- Secure authentication using Django's built-in security

## Prerequisites

- Python 3.8+
- Django 5.0+
- Email account for sending verification emails

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd User-Mgt/usermgmt
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   venv\Scripts\activate.bat  # On Windows
   source venv/bin/activate   # On Unix/MacOS
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root directory with the following content:
   ```
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Run the application using the provided script:
   ```
   run.bat
   ```
   
   This script will:
   - Apply any pending migrations
   - Create a default superuser if none exists (email: gladystbarasa@gmail.com)
   - Start the development server

7. Or run individual commands:
   ```
   # Create a superuser if none exists
   python manage.py create_superuser_if_none
   
   # Start the development server
   python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/
   
   Default superuser credentials:
   - Email: gladystbarasa@gmail.com
   - Password: Gladys@2030

## Email Configuration

This project uses Gmail SMTP for sending emails. To use your Gmail account:

1. Enable 2-Step Verification for your Google account
2. Generate an App Password
3. Use your Gmail address as EMAIL_HOST_USER
4. Use the generated App Password as EMAIL_HOST_PASSWORD

## Testing

To verify all flows work correctly:

1. Register a new user and check if verification email is sent
2. Verify the email using the link in the email
3. Log in with the verified account
4. Try the password reset functionality
5. Update your profile information

## Security Notes

- All passwords are securely hashed
- CSRF protection is enabled for all forms
- Email verification uses secure tokens
- Token expiration is enforced for security

## Project Structure

- `accounts/` - Main app for user management
  - `models.py` - CustomUser model
  - `forms.py` - Registration and profile forms
  - `views.py` - Authentication and profile views
  - `urls.py` - URL routing
- `templates/` - HTML templates
  - `accounts/` - Account-related templates
  - `accounts/email/` - Email templates
- `media/` - User uploaded files (profile pictures)
- `static/` - Static files (CSS, JS)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
