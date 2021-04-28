from dataclasses import dataclass
from datetime import datetime


@dataclass
class TodoModel:
    title: str
    description: str
    pk: int = 0
    created_on: str = datetime.now().strftime("%H:%M:%S, %m.%d.%Y")
    due_date: str = ""
    _is_deleted: bool = False
    _is_done: bool = False

    def __dict__(self):
        return {
            "pk": self.pk,
            "title": self.title,
            "description": self.description,
            "created_on": self.created_on,
        }

    def to_json(self):
        return str(self.__dict__())

    def delete_todo(self):
        self._is_deleted = True

    def done_todo(self):
        self._is_done = True

    def is_deleted(self):
        return self._is_deleted

    def is_done(self):
        return self._is_done


@dataclass
class ToDoContainer:
    items: dict

    def create(self, params):
        due_date = params.get("due_date") or ""
        todo = TodoModel(title=params["title"], description=params["description"], due_date=due_date)
        try:
            todo.pk = max(self.items.keys()) + 1
        except ValueError:
            todo.pk = 1
        self.items[todo.pk] = todo
        return todo

    def delete(self, pk):
        self.items[pk].delete_todo()
        return self.items[pk]

    def done(self, pk):
        self.items[pk].done_todo()
        return self.items[pk]

    def retrieve(self, pk):
        if not (self.items[pk].is_done() or self.items[pk].is_deleted()):
            return self.items[pk]
        return None

    def list(self):
        li = []
        for key, value in self.items.items():
            if value.is_done() or value.is_deleted():
                pass
            else:
                li.append(self.items[key])
        return li
