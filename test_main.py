from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_todo():
    response = client.post("/todos/", json={"title": "Testar Lista", "description": "Use o Pytest"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Testar Lista"  # Corrigido para corresponder ao valor enviado
    assert data["description"] == "Use o Pytest"  # Corrigido para corresponder ao valor enviado
    assert data["completed"] is False
    assert "id" in data

def test_get_todos():
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_todo():
    todo_response = client.post("/todos/", json={"title": "Pegar Todo", "description": "Pegar Description"})
    todo_id = todo_response.json()["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Pegar Todo"  # Corrigido para corresponder ao valor enviado

def test_update_todo():
    todo_response = client.post("/todos/", json={"title": "Um Novo Todo", "description": "Uma Nova Description"})
    todo_id = todo_response.json()["id"]

    update_response = client.put(f"/todos/{todo_id}", json={"title": "Updated", "description": "Updated Description", "completed": True})
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Updated"
    assert data["description"] == "Updated Description"  # Adicionado para verificar a descrição também
    assert data["completed"] is True

def test_delete_todo():
    todo_response = client.post("/todos/", json={"title": "Delete Todo", "description": "Delete Description"})
    todo_id = todo_response.json()["id"]

    delete_response = client.delete(f"/todos/{todo_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Tarefa excluída com sucesso"}

    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Tarefa não encontrada"}
