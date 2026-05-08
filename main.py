from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Project, ProjectPlace
from schemas import (
    ProjectCreate,
    ProjectUpdate,
    PlaceCreate,
    PlaceUpdate,
)
from services import validate_artwork

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Travel Planner API")


@app.get("/")
def root():
    return {"message": "Travel Planner API"}


# CREATE PROJECT
@app.post("/projects")
async def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db)
):

    if len(payload.places) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 places allowed"
        )

    added_ids = set()

    for place in payload.places:

        if place.external_id in added_ids:
            raise HTTPException(
                status_code=400,
                detail="Duplicate places are not allowed"
            )

        exists = await validate_artwork(place.external_id)

        if not exists:
            raise HTTPException(
                status_code=404,
                detail=f"Artwork {place.external_id} not found"
            )

        added_ids.add(place.external_id)

    project = Project(
        name=payload.name,
        description=payload.description,
        start_date=payload.start_date,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    for place in payload.places:

        db_place = ProjectPlace(
            project_id=project.id,
            external_id=place.external_id,
        )

        db.add(db_place)

    db.commit()

    return project


# GET ALL PROJECTS
@app.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()


# GET SINGLE PROJECT
@app.get("/projects/{project_id}")
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


# UPDATE PROJECT
@app.patch("/projects/{project_id}")
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    data = payload.dict(exclude_unset=True)

    for key, value in data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project


# DELETE PROJECT
@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    visited_place = (
        db.query(ProjectPlace)
        .filter(
            ProjectPlace.project_id == project_id,
            ProjectPlace.visited == True
        )
        .first()
    )

    if visited_place:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete project with visited places"
        )

    db.delete(project)
    db.commit()

    return {"message": "Project deleted"}


# ADD PLACE TO PROJECT
@app.post("/projects/{project_id}/places")
async def add_place(
    project_id: int,
    payload: PlaceCreate,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    places_count = (
        db.query(ProjectPlace)
        .filter(ProjectPlace.project_id == project_id)
        .count()
    )

    if places_count >= 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 places allowed"
        )

    duplicate_place = (
        db.query(ProjectPlace)
        .filter(
            ProjectPlace.project_id == project_id,
            ProjectPlace.external_id == payload.external_id
        )
        .first()
    )

    if duplicate_place:
        raise HTTPException(
            status_code=400,
            detail="Place already exists in project"
        )

    exists = await validate_artwork(payload.external_id)

    if not exists:
        raise HTTPException(
            status_code=404,
            detail="Artwork not found"
        )

    place = ProjectPlace(
        project_id=project_id,
        external_id=payload.external_id,
    )

    db.add(place)
    db.commit()
    db.refresh(place)

    return place


# GET ALL PLACES IN PROJECT
@app.get("/projects/{project_id}/places")
def get_places(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return (
        db.query(ProjectPlace)
        .filter(ProjectPlace.project_id == project_id)
        .all()
    )


# GET SINGLE PLACE
@app.get("/projects/{project_id}/places/{place_id}")
def get_place(
    project_id: int,
    place_id: int,
    db: Session = Depends(get_db)
):

    place = (
        db.query(ProjectPlace)
        .filter(
            ProjectPlace.project_id == project_id,
            ProjectPlace.id == place_id
        )
        .first()
    )

    if not place:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )

    return place


# UPDATE PLACE
@app.patch("/projects/{project_id}/places/{place_id}")
def update_place(
    project_id: int,
    place_id: int,
    payload: PlaceUpdate,
    db: Session = Depends(get_db)
):

    place = (
        db.query(ProjectPlace)
        .filter(
            ProjectPlace.project_id == project_id,
            ProjectPlace.id == place_id
        )
        .first()
    )

    if not place:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )

    data = payload.dict(exclude_unset=True)

    for key, value in data.items():
        setattr(place, key, value)

    db.commit()
    db.refresh(place)

    all_places = (
        db.query(ProjectPlace)
        .filter(ProjectPlace.project_id == project_id)
        .all()
    )

    if all_places and all(p.visited for p in all_places):

        project = (
            db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

        project.completed = True

        db.commit()

    return place