"""Todo service for managing todo items."""
import json
from pathlib import Path
from typing import List, Optional
from ..models.todo import Todo


class TodoService:
    """Service class for managing todo items with persistent storage."""
    
    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize the TodoService.
        
        Args:
            storage_path: Path to the JSON file for storing todos.
                         Defaults to ~/.todo-cli/todos.json
        """
        if storage_path is None:
            storage_path = Path.home() / ".todo-cli" / "todos.json"
        
        self.storage_path = storage_path
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize storage file if it doesn't exist
        if not self.storage_path.exists():
            self._save_todos([])
    
    def _load_todos(self) -> List[Todo]:
        """Load todos from storage.
        
        Returns:
            List of Todo objects
        """
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                return [Todo.from_dict(todo_dict) for todo_dict in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_todos(self, todos: List[Todo]) -> None:
        """Save todos to storage.
        
        Args:
            todos: List of Todo objects to save
        """
        with open(self.storage_path, 'w') as f:
            json.dump([todo.to_dict() for todo in todos], f, indent=2)
    
    def add_todo(self, title: str) -> Todo:
        """Add a new todo item.
        
        Args:
            title: The title/description of the todo
            
        Returns:
            The newly created Todo object
            
        Raises:
            ValueError: If title is empty or only whitespace
        """
        if not title or not title.strip():
            raise ValueError("Todo title cannot be empty")
        
        todos = self._load_todos()
        new_todo = Todo(title=title.strip())
        todos.append(new_todo)
        self._save_todos(todos)
        
        return new_todo
    
    def get_all_todos(self) -> List[Todo]:
        """Get all todo items.
        
        Returns:
            List of all Todo objects
        """
        return self._load_todos()
    
    def get_todo_by_id(self, todo_id: str) -> Optional[Todo]:
        """Get a specific todo by its ID.
        
        Args:
            todo_id: The ID of the todo to retrieve
            
        Returns:
            The Todo object if found, None otherwise
        """
        todos = self._load_todos()
        for todo in todos:
            if todo.id == todo_id:
                return todo
        return None
    
    def complete_todo(self, todo_id: str) -> Optional[Todo]:
        """Mark a todo as completed.
        
        Args:
            todo_id: The ID of the todo to complete
            
        Returns:
            The updated Todo object if found, None otherwise
        """
        todos = self._load_todos()
        for todo in todos:
            if todo.id == todo_id:
                todo.mark_completed()
                self._save_todos(todos)
                return todo
        return None
    
    def update_todo_title(self, todo_id: str, new_title: str) -> Optional[Todo]:
        """Update a todo's title.
        
        Args:
            todo_id: The ID of the todo to update
            new_title: The new title for the todo
            
        Returns:
            The updated Todo object if found, None otherwise
            
        Raises:
            ValueError: If new_title is empty or only whitespace
        """
        if not new_title or not new_title.strip():
            raise ValueError("Todo title cannot be empty")
        
        todos = self._load_todos()
        for todo in todos:
            if todo.id == todo_id:
                todo.update_title(new_title.strip())
                self._save_todos(todos)
                return todo
        return None
    
    def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo.
        
        Args:
            todo_id: The ID of the todo to delete
            
        Returns:
            True if the todo was deleted, False if not found
        """
        todos = self._load_todos()
        original_count = len(todos)
        todos = [todo for todo in todos if todo.id != todo_id]
        
        if len(todos) < original_count:
            self._save_todos(todos)
            return True
        return False