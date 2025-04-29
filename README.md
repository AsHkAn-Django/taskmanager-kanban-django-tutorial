# taskmanager-kanban-django-tutorial

Interactive Django task manager with a drag-and-drop Kanban board, AJAX updates, and real-time task status syncing using SortableJS.

## Features
- Drag-and-drop Kanban board powered by SortableJS  
- AJAX updates for seamless, real-time task status syncing  
- Full CRUD on tasks, columns, and boards  
- User authentication and permissions  

## Getting Started

### Prerequisites
- Python 3.8+  
- Django 4.x  
- Node.js & npm  

### Installation
1. Clone the repository  
```bash
git clone https://github.com/yourusername/taskmanager-kanban.git
cd taskmanager-kanban
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
```

3. Install Python dependencies
```bash
pip install -r requirements.txt
```

4. Install frontend dependencies
```bash
npm install
```

### Configuration
1. Copy .env.example to .env and fill in your settings (e.g., SECRET_KEY, DATABASE_URL, etc.)

2. In .env, set your allowed hosts as a comma-separated list:

```env
ALLOWED_HOSTS=127.0.0.1,localhost,yourdomain.com
```

3. In settings.py, parse that into a Python list:

```python
from decouple import config

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')
```

### Usage
1. Apply migrations and create a superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

2. Build frontend assets
```bash
npm run build
```

3. Run the development server
```bash
python manage.py runserver
```

4. Open http://127.0.0.1:8000/ in your browser to access the Kanban board.


### Contributing
1. Fork the repository

2. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

3. Commit your changes:
```bash
git commit -m "Add your feature"
```

4. Push to your fork:

```bash
git push origin feature/your-feature-name
```

5. Open a Pull Request

## Tutorial