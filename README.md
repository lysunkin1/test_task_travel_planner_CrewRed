# Travel Planner API

RESTful API for managing travel projects and places.
Built with **FastAPI**, **SQLAlchemy**, **SQLite**.

## Setup

```bash
git clone https://github.com/lysunkin1/test_task_travel_planner_CrewRed.git
cd test_task_travel_planner_CrewRed

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
```

API: `http://localhost:8000`  
Swagger docs: `http://localhost:8000/docs`

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/projects` | Create project (with optional places) |
| `GET` | `/projects` | List all projects |
| `GET` | `/projects/{id}` | Get project |
| `PATCH` | `/projects/{id}` | Update project |
| `DELETE` | `/projects/{id}` | Delete project |
| `POST` | `/projects/{id}/places` | Add place to project |
| `GET` | `/projects/{id}/places` | List places |
| `GET` | `/projects/{id}/places/{place_id}` | Get place |
| `PATCH` | `/projects/{id}/places/{place_id}` | Update notes / mark visited |

## Notes

- Max 10 places per project
- Places are validated via [Art Institute of Chicago API](https://api.artic.edu/docs/)
- Project cannot be deleted if any place is already visited
- Project is auto-marked `completed` when all places are visited