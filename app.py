"""
Task Management System
A command-line application for managing tasks with priorities, deadlines, and categories.
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class Task:
    """Represents a single task with various attributes."""
    
    def __init__(self, title: str, description: str = "", priority: str = "medium",
                 category: str = "general", deadline: Optional[str] = None):
        self.id = None
        self.title = title
        self.description = description
        self.priority = priority  # low, medium, high
        self.category = category
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.deadline = deadline
        self.completed_at = None
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'category': self.category,
            'completed': self.completed,
            'created_at': self.created_at,
            'deadline': self.deadline,
            'completed_at': self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create task from dictionary."""
        task = cls(data['title'], data['description'], data['priority'], 
                   data['category'], data['deadline'])
        task.id = data['id']
        task.completed = data['completed']
        task.created_at = data['created_at']
        task.completed_at = data['completed_at']
        return task
    
    def mark_complete(self):
        """Mark task as completed."""
        self.completed = True
        self.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if self.deadline and not self.completed:
            deadline_date = datetime.strptime(self.deadline, "%Y-%m-%d")
            return datetime.now() > deadline_date
        return False


class TaskManager:
    """Manages a collection of tasks."""
    
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.next_id = 1
        self.load_tasks()
    
    def add_task(self, task: Task) -> int:
        """Add a new task and return its ID."""
        task.id = self.next_id
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        return task.id
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID."""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False
    
    def complete_task(self, task_id: int) -> bool:
        """Mark task as completed."""
        task = self.get_task(task_id)
        if task:
            task.mark_complete()
            self.save_tasks()
            return True
        return False
    
    def get_tasks_by_category(self, category: str) -> List[Task]:
        """Get all tasks in a category."""
        return [t for t in self.tasks if t.category == category]
    
    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """Get all tasks with specific priority."""
        return [t for t in self.tasks if t.priority == priority]
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all incomplete tasks."""
        return [t for t in self.tasks if not t.completed]
    
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks."""
        return [t for t in self.tasks if t.completed]
    
    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue tasks."""
        return [t for t in self.tasks if t.is_overdue()]
    
    def save_tasks(self):
        """Save tasks to JSON file."""
        data = {
            'next_id': self.next_id,
            'tasks': [task.to_dict() for task in self.tasks]
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_tasks(self):
        """Load tasks from JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.next_id = data.get('next_id', 1)
                self.tasks = [Task.from_dict(t) for t in data.get('tasks', [])]


def print_task(task: Task, detailed: bool = False):
    """Print task information."""
    status = "✓" if task.completed else "○"
    priority_symbols = {"low": "↓", "medium": "→", "high": "↑"}
    priority = priority_symbols.get(task.priority, "→")
    
    overdue = " [OVERDUE]" if task.is_overdue() else ""
    deadline = f" | Due: {task.deadline}" if task.deadline else ""
    
    print(f"{status} [{task.id}] {priority} {task.title}{deadline}{overdue}")
    
    if detailed:
        print(f"   Category: {task.category}")
        print(f"   Priority: {task.priority}")
        print(f"   Created: {task.created_at}")
        if task.description:
            print(f"   Description: {task.description}")
        if task.completed:
            print(f"   Completed: {task.completed_at}")
        print()


def main():
    """Main application loop."""
    manager = TaskManager()
    
    while True:
        print("\n=== Task Manager ===")
        print("1. Add task")
        print("2. List all tasks")
        print("3. List pending tasks")
        print("4. List completed tasks")
        print("5. List overdue tasks")
        print("6. Complete task")
        print("7. Delete task")
        print("8. View task details")
        print("9. Exit")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == "1":
            title = input("Title: ").strip()
            description = input("Description (optional): ").strip()
            priority = input("Priority (low/medium/high) [medium]: ").strip() or "medium"
            category = input("Category [general]: ").strip() or "general"
            deadline = input("Deadline (YYYY-MM-DD) [optional]: ").strip() or None
            
            task = Task(title, description, priority, category, deadline)
            task_id = manager.add_task(task)
            print(f"Task added with ID: {task_id}")
        
        elif choice == "2":
            tasks = manager.tasks
            if tasks:
                for task in tasks:
                    print_task(task)
            else:
                print("No tasks found.")
        
        elif choice == "3":
            tasks = manager.get_pending_tasks()
            if tasks:
                for task in tasks:
                    print_task(task)
            else:
                print("No pending tasks.")
        
        elif choice == "4":
            tasks = manager.get_completed_tasks()
            if tasks:
                for task in tasks:
                    print_task(task)
            else:
                print("No completed tasks.")
        
        elif choice == "5":
            tasks = manager.get_overdue_tasks()
            if tasks:
                for task in tasks:
                    print_task(task)
            else:
                print("No overdue tasks.")
        
        elif choice == "6":
            task_id = int(input("Enter task ID to complete: "))
            if manager.complete_task(task_id):
                print("Task marked as completed!")
            else:
                print("Task not found.")
        
        elif choice == "7":
            task_id = int(input("Enter task ID to delete: "))
            if manager.delete_task(task_id):
                print("Task deleted!")
            else:
                print("Task not found.")
        
        elif choice == "8":
            task_id = int(input("Enter task ID: "))
            task = manager.get_task(task_id)
            if task:
                print_task(task, detailed=True)
            else:
                print("Task not found.")
        
        elif choice == "9":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()