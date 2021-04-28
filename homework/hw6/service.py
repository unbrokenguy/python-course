from models import ToDoContainer


class ToDoService:
    def __init__(self):
        self.db = ToDoContainer({})

    def create(self, params):
        return self.db.create(params=params).to_json()

    def delete_todo(self, pk):
        return self.db.delete(pk=pk).to_json()

    def done_todo(self, pk):
        return self.db.done(pk=pk).to_json()

    def retrieve(self, pk):
        todo = self.db.retrieve(pk)
        if todo:
            return todo.to_json()
        else:
            return "404"

    def list(self):
        li = ", ".join(map(lambda x: x.to_json(), self.db.list()))
        return f"[{li}]"
