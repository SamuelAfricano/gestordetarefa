"""Este é o modulo controller do app. """

from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from rptodo_project.rptodo import DB_READ_ERROR, ID_ERROR
from rptodo_project.rptodo.database import DatabaseHandler


class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int


class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, description: List[str], priority: int = 2) -> CurrentTodo:
        """add novo item a tarefa """
        description_text = " ".join(description)
        if not description_text.endswith("."):
            description_text += "."
        todo = {
            "Descricao": description_text,
            "Prioridade": priority,
            "Feito": "Não",
        }
        read = self._db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return CurrentTodo(todo, read.error)
        read.todo_list.append(todo)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def get_todoer_list(self) -> List[Dict[str, Any]]:
        """ Retorna a lista de tarefa """
        read = self._db_handler.read_todos()
        return read.todo_list

    def set_done(self, todo_id: int) -> CurrentTodo:
        """Mudar para concluido """
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list[todo_id - 1]
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        todo["Feito"] = "Sim"
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def remove(self, todo_id: int) -> CurrentTodo:
        """romove um item com base neste ID."""
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list.pop(todo_id - 1)
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def  remove_todos(self):
        """Remove todas as tarefa"""
        write = self._db_handler.write_todos([])
        return CurrentTodo({}, write.error)