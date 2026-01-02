"""Todo data model."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class Todo:
    """Represents a todo item.
    
    Attributes:
        id: Unique identifier for the todo
        title: The todo item's title/description
        completed: Whether the todo is completed
        created_at: Timestamp when the todo was created
        updated_at: Timestamp when the todo was last updated
    """
    title: str
    id: str = field(default_factory=lambda: str(uuid4()))
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def mark_completed(self) -> None:
        """Mark this todo as completed."""
        self.completed = True
        self.updated_at = datetime.now()
    
    def update_title(self, new_title: str) -> None:
        """Update the todo's title.
        
        Args:
            new_title: The new title for the todo
        """
        self.title = new_title
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert todo to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        """Create a Todo instance from a dictionary.
        
        Args:
            data: Dictionary containing todo data
            
        Returns:
            A new Todo instance
        """
        return cls(
            id=data["id"],
            title=data["title"],
            completed=data["completed"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )