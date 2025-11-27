from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Todo


class TodoModelTest(TestCase):
    """Test cases for the Todo model"""
    
    def setUp(self):
        self.todo = Todo.objects.create(
            title="Test Todo",
            description="Test Description",
            due_date=timezone.now() + timedelta(days=1)
        )
    
    def test_todo_creation(self):
        """Test that a TODO can be created successfully"""
        self.assertEqual(self.todo.title, "Test Todo")
        self.assertEqual(self.todo.description, "Test Description")
        self.assertFalse(self.todo.completed)
        self.assertIsNotNone(self.todo.created_date)
    
    def test_todo_str_method(self):
        """Test the string representation of a TODO"""
        self.assertEqual(str(self.todo), "Test Todo")
    
    def test_todo_default_completed_status(self):
        """Test that new TODOs are not completed by default"""
        new_todo = Todo.objects.create(title="Another Todo")
        self.assertFalse(new_todo.completed)
    
    def test_todo_ordering(self):
        """Test that TODOs are ordered by creation date (newest first)"""
        todo1 = Todo.objects.create(title="First")
        todo2 = Todo.objects.create(title="Second")
        todos = Todo.objects.all()
        self.assertEqual(todos[0].title, "Second")
        self.assertEqual(todos[1].title, "First")


class TodoViewTest(TestCase):
    """Test cases for TODO views"""
    
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(
            title="Test Todo",
            description="Test Description",
            due_date=timezone.now() + timedelta(days=1)
        )
    
    def test_todo_list_view(self):
        """Test that the home page displays TODOs"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Todo")
    
    def test_create_todo_view_get(self):
        """Test GET request to create TODO page"""
        response = self.client.get(reverse('create_todo'))
        self.assertEqual(response.status_code, 200)
    
    def test_create_todo_view_post(self):
        """Test creating a new TODO via POST"""
        response = self.client.post(reverse('create_todo'), {
            'title': 'New Todo',
            'description': 'New Description',
            'due_date': (timezone.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M')
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Todo.objects.filter(title='New Todo').exists())
    
    def test_create_todo_without_title(self):
        """Test that creating a TODO without title fails"""
        initial_count = Todo.objects.count()
        response = self.client.post(reverse('create_todo'), {
            'description': 'No title todo'
        })
        self.assertEqual(Todo.objects.count(), initial_count)
    
    def test_edit_todo_view_get(self):
        """Test GET request to edit TODO page"""
        response = self.client.get(reverse('edit_todo', args=[self.todo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Todo")
    
    def test_edit_todo_view_post(self):
        """Test editing an existing TODO"""
        response = self.client.post(reverse('edit_todo', args=[self.todo.id]), {
            'title': 'Updated Todo',
            'description': 'Updated Description',
            'due_date': (timezone.now() + timedelta(days=3)).strftime('%Y-%m-%dT%H:%M')
        })
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Todo')
        self.assertEqual(self.todo.description, 'Updated Description')
    
    def test_delete_todo_view(self):
        """Test deleting a TODO"""
        todo_id = self.todo.id
        response = self.client.post(reverse('delete_todo', args=[todo_id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(id=todo_id).exists())
    
    def test_mark_completed_view(self):
        """Test marking a TODO as completed"""
        self.assertFalse(self.todo.completed)
        response = self.client.post(reverse('mark_completed', args=[self.todo.id]))
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.completed)
    
    def test_view_with_invalid_todo_id(self):
        """Test accessing a non-existent TODO returns 404"""
        response = self.client.get(reverse('edit_todo', args=[9999]))
        self.assertEqual(response.status_code, 404)


class TodoDueDateTest(TestCase):
    """Test cases for TODO due dates"""
    
    def test_todo_with_due_date(self):
        """Test creating TODO with due date"""
        due_date = timezone.now() + timedelta(days=5)
        todo = Todo.objects.create(
            title="Todo with due date",
            due_date=due_date
        )
        self.assertEqual(todo.due_date, due_date)
    
    def test_todo_without_due_date(self):
        """Test creating TODO without due date"""
        todo = Todo.objects.create(title="Todo without due date")
        self.assertIsNone(todo.due_date)
    
    def test_overdue_todo(self):
        """Test identifying overdue TODOs"""
        overdue_todo = Todo.objects.create(
            title="Overdue Todo",
            due_date=timezone.now() - timedelta(days=1)
        )
        self.assertLess(overdue_todo.due_date, timezone.now())
        self.assertFalse(overdue_todo.completed)
