from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import json
from pathlib import Path

app = FastAPI(title="Dogs Demo API", version="1.0.0")

DATA_FILE = Path("dogs.json")


class DogBase(BaseModel):
    name: str = Field(..., min_length=1, description="Dog name")
    breed: str = Field(..., min_length=1, description="Dog breed")
    age: int = Field(..., ge=0, description="Dog age in years")
    owner: str = Field(..., min_length=1, description="Dog owner")
    gender: str = Field(..., min_length=1, description="Dog gender")


class DogCreate(DogBase):
    pass


class DogUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    breed: Optional[str] = Field(None, min_length=1)
    age: Optional[int] = Field(None, ge=0)
    owner: Optional[str] = Field(None, min_length=1)
    gender: Optional[str] = Field(None, min_length=1)


class Dog(DogBase):
    id: int


def load_dogs() -> List[dict]:
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_dogs(dogs: List[dict]) -> None:
    DATA_FILE.write_text(json.dumps(dogs, indent=2), encoding="utf-8")


@app.get("/")
def root():
    return {"message": "Welcome to the Dogs Demo API"}


@app.get("/dogs", response_model=List[Dog])
def get_all_dogs():
    return load_dogs()


@app.get("/dogs/{dog_id}", response_model=Dog)
def get_dog(dog_id: int):
    dogs = load_dogs()
    for dog in dogs:
        if dog["id"] == dog_id:
            return dog
    raise HTTPException(status_code=404, detail="Dog not found")


@app.post("/dogs", response_model=Dog, status_code=201)
def create_dog(dog: DogCreate):
    dogs = load_dogs()
    next_id = max((item["id"] for item in dogs), default=0) + 1

    new_dog = {
        "id": next_id,
        "name": dog.name,
        "breed": dog.breed,
        "age": dog.age,
        "owner": dog.owner,
        "gender": dog.gender,
    }

    dogs.append(new_dog)
    save_dogs(dogs)
    return new_dog


@app.put("/dogs/{dog_id}", response_model=Dog)
def update_dog(dog_id: int, updated_dog: DogUpdate):
    dogs = load_dogs()

    for index, dog in enumerate(dogs):
        if dog["id"] == dog_id:
            updated_data = updated_dog.model_dump(exclude_unset=True)
            dogs[index] = {**dog, **updated_data}
            save_dogs(dogs)
            return dogs[index]

    raise HTTPException(status_code=404, detail="Dog not found")


@app.delete("/dogs/{dog_id}")
def delete_dog(dog_id: int):
    dogs = load_dogs()

    for dog in dogs:
        if dog["id"] == dog_id:
            dogs.remove(dog)
            save_dogs(dogs)
            return {"message": f"Dog with id {dog_id} deleted successfully"}

    raise HTTPException(status_code=404, detail="Dog not found")
