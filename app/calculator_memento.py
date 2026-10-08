"""Memento: snapshots of the entire calculation history."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Memento:
    entries: tuple

class Caretaker:
    """Maintains undo and redo stacks of history snapshots."""
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def remember(self, entries):
        self.undo_stack.append(Memento(tuple(entries)))
        self.redo_stack.clear()

    def undo(self, current):
        if not self.undo_stack:
            return list(current)
        self.redo_stack.append(Memento(tuple(current)))
        return list(self.undo_stack.pop().entries)

    def redo(self, current):
        if not self.redo_stack:
            return list(current)
        self.undo_stack.append(Memento(tuple(current)))
        return list(self.redo_stack.pop().entries)
