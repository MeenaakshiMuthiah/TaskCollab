# TaskCollab - Task Collaboration Web App

## Features
- Signup / Login (username + email + password)
- Create tasks (title, description, deadline, priority)
- Assign tasks to self or other users
- Mark tasks Completed / Pending
- Dashboard showing tasks created by user and tasks assigned to user
- Overdue tasks highlighted in red
- Filter/sort tasks, CSV export, basic analytics

## Quick start (local)
```bash
git clone <repo-url>
cd taskcollab
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
