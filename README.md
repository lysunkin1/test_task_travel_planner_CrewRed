Travel Planner API
RESTful API for managing travel projects and places.
Built with FastAPI, SQLAlchemy, SQLite.
Setup
bashgit clone https://github.com/lysunkin1/test_task_travel_planner_CrewRed.git
cd test_task_travel_planner_CrewRed

python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
uvicorn main:app --reload
API доступен на http://localhost:8000
Swagger docs: http://localhost:8000/docs

Notes

Max 10 places per project
Places are validated via Art Institute of Chicago API
Project cannot be deleted if any place is already visited
Project is auto-marked completed when all places are visited
