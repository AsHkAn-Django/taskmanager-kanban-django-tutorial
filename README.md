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

1. for the start I added an `PositiveBigIntegerField` to the model

```python
# models.py
class Task(models.Model):
    name = models.CharField(max_length=264)
    is_complete = models.BooleanField(default=False)
    # we set the null true and blank false so we want to let the order null then we give it a value
    order = models.PositiveBigIntegerField(null=True, blank=False)

    class Meta:
        # set the order base on order field
        ordering = ['order']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        check if the object doesn't have a pk it means it's new so save it, then if it its orderfield is null set it as the pk value.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.order is None:
            self.order = self.pk
            super().save(update_fields=['order'])

        return super().save(*args, **kwargs)
```

2. create a view for reordering the tasks

```python
# views.py
from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def reorder_items(request):
    """
    Accepts a JSON POST request with a list of item IDs in new order.
    Updates each item's 'order' field to reflect the new order.
    """
    try:
        # Parse JSON request body into Python dictionary
        data = json.loads(request.body)

        # Extract the 'order' list from the data
        order = data.get('order', [])

        # Update each item in the database
        for index, task_id in enumerate(order):
            task = Task.objects.get(id=task_id)
            task.order = index
            task.save()

        # Respond with success
        return JsonResponse({'status': 'success'})
    except Exception as e:
        # If something goes wrong, respond with an error
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
```

3. create the url for it

```python
# urls.py
# ...
    path('reorder/', reorder_items, name='reorder-items'),
# ...
```

4. edit the template that shows the list of the tasks

```html
<!-- task_list.html -->
<script src="https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js"></script>

<!-- Django's template tag for CSRF token -->
{% csrf_token %}

<!-- Hidden input to get the CSRF token -->
<input type="hidden" id="csrf-token" value="{{ csrf_token }}" />

<!-- the id is set for using it again -->
<div class="row" id="item-list">
  {% for task in tasks %}
  <!-- set the id of each div(for a task) the same amnount of task.id -->
  <div class="col-md-4 mb-4 task" data-id="{{ task.id }}"></div>
</div>


<!-- and the javascript part-->
<script>
  // 1. Select the sortable list by ID
  const sortableList = document.getElementById("item-list");

  // 2. Select the hidden input that holds the CSRF token
  const csrfToken = document.getElementById("csrf-token").value;

  // 3. Initialize SortableJS on the list
  new Sortable(sortableList, {
    animation: 150, // Smooth drag animation

    // 4. Function triggered when the user finishes dragging an item
    onEnd: function () {
      // 5. Get all the list items after they’ve been reordered
      const items = sortableList.querySelectorAll(".task");

      // 6. Map over them to create an array of their data-id attributes (as strings)
      const order = Array.from(items).map((item) => item.dataset.id);

      // 7. Send the new order to the Django backend using fetch()
      fetch("/reorder/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Tell Django we're sending JSON
          "X-CSRFToken": csrfToken, // Include the CSRF token securely!
        },
        body: JSON.stringify({ order: order }), // Send the new order list
      })
        .then((response) => response.json()) // Convert response to JSON
        .then((data) => {
          console.log("Server response:", data); // Log the server response
        })
        .catch((error) => {
          console.error("Error saving new order:", error); // Log any errors
        });
    },
  });
</script>
```
