from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

#Representando a Tarefa (To-Do)
class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

todos: List[Todo] = []

#Criar tarefa
@app.post("/todos/", response_model=Todo)
async def create_todo(todo: Todo):
    todo.id = len(todos) + 1
    todos.append(todo)
    return todo

#Listar tarefas
@app.get("/todos/", response_model=List[Todo])
async def read_todos():
    return todos

#Obter tarefa por ID
@app.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int):
    todo = next((todo for todo in todos if todo.id == todo_id), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return todo

#Atualizar Tarefa
@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, updated_todo: Todo):
    todo = next((todo for todo in todos if todo.id == todo_id), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    todo.title = updated_todo.title
    todo.description = updated_todo.description
    todo.completed = updated_todo.completed
    return todo

#Excluir Tarefa
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    global todos
    todos = [todo for todo in todos if todo.id != todo_id]
    return {"message": "Tarefa excluída com sucesso"}