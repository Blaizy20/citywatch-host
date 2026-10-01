# CityWatch

CityWatch is a Django web application for submitting, tracking, and analyzing community reports.

## Local Development

### Requirements

- Python 3.12 or newer
- Git
- A terminal opened in the project root

### 1. Open the project folder

PowerShell:

```powershell
cd C:\Users\Meia\citywatch
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once for the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Django

This project currently does not include a `requirements.txt` file.

```powershell
python -m pip install --upgrade pip
python -m pip install django
```

### 4. Apply database migrations

```powershell
python manage.py migrate
```

The local SQLite database is `db.sqlite3` in the project root. Do not delete it if you need the existing local data.

### 5. Check the project

```powershell
python manage.py check
```

### 6. Run the automated tests

```powershell
python manage.py test
```

Some apps currently have limited test coverage, but this command checks all Django app tests.

### 7. Start the local server

```powershell
python manage.py runserver
```

Open the URL shown in the terminal, normally:

- http://127.0.0.1:8000/
- http://localhost:8000/

Leave the server terminal running while testing. Press `Ctrl+C` to stop it.

### Email OTP delivery

OTP email verification is enabled for registration and password resets. By default,
the development console email backend prints each message, including its code, in
the terminal running Django. This is useful for local testing and does not send
real email.

To deliver codes to inboxes, set these environment variables before starting the
server. Use SMTP credentials from your email provider; do not commit credentials
to the repository.

```powershell
$env:EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
$env:EMAIL_HOST = "smtp.gmail.com"
$env:EMAIL_PORT = "587"
$env:EMAIL_HOST_USER = "your-sender@gmail.com"
$env:EMAIL_HOST_PASSWORD = "your-provider-app-password"
$env:EMAIL_USE_TLS = "true"
$env:EMAIL_USE_SSL = "false"
$env:DEFAULT_FROM_EMAIL = "CityWatch <your-sender@gmail.com>"
python manage.py runserver
```

OTP codes expire after 10 minutes, allow five verification attempts, and can be
resent after a 60-second cooldown.

## Local Test Flow

1. Open the landing page at http://127.0.0.1:8000/.
2. Open the registration page at http://127.0.0.1:8000/accounts/register/.
3. Create a resident account with a unique username and email.
4. Open the login page at http://127.0.0.1:8000/accounts/login/.
5. Log in with the new account and verify that the resident dashboard opens.
6. Test invalid login details and mismatched registration passwords.
7. After changing a template, refresh the browser with `Ctrl+Shift+R`.
8. If a route behaves unexpectedly, check the Django server terminal for errors.

## Frontend Template Paths

The templates are stored inside each Django app. These are the main UI files:

### Authentication and account UI

- `accounts/templates/accounts/landing.html` - public landing page
- `accounts/templates/accounts/login.html` - **login UI**
- `accounts/templates/accounts/register.html` - **registration UI**
- `accounts/templates/accounts/profile.html` - user profile UI
- `accounts/templates/accounts/user_list.html` - staff user management UI

Routes:

- `/` - landing page
- `/accounts/login/` - login
- `/accounts/register/` - registration
- `/accounts/profile/` - profile
- `/accounts/users/` - staff user list

### Reports UI

- `reports/templates/reports/home.html`
- `reports/templates/reports/dashboard.html`
- `reports/templates/reports/report_list.html`
- `reports/templates/reports/report_detail.html`
- `reports/templates/reports/report_form.html`
- `reports/templates/reports/report_confirm_delete.html`
- `reports/templates/reports/public_board.html`
- `reports/templates/reports/admin_report_list.html`
- `reports/templates/reports/admin_report_detail.html`
- `reports/templates/reports/announcements.html`

### Analytics UI

- `analytics/templates/analytics/dashboard.html`
- `analytics/templates/analytics/map_view.html`
- `analytics/templates/analytics/reports_analytics.html`

### Assignments UI

- `assignments/templates/assignments/department_list.html`

## Useful Commands

```powershell
# Check for Django configuration problems
python manage.py check

# Run tests
python manage.py test

# Run one app's tests
python manage.py test accounts
python manage.py test reports

# Create migrations after changing models
python manage.py makemigrations
python manage.py migrate

# Create an admin account for /admin/
python manage.py createsuperuser
```

## Git Workflow

Check the current state before committing:

```powershell
git status
git diff
```

Commit and push source/template changes:

```powershell
git add .
git commit -m "Describe the change"
git push origin main
```

Avoid committing local Python cache files or accidental database changes unless they are intentionally part of the change.
