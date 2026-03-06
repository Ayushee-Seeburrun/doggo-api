# FastAPI Dogs Demo API

A simple FastAPI demo API that performs CRUD operations on a JSON file containing dog information.

## Data stored
Each dog record contains:
- id
- name
- breed
- age
- owner
- gender

## Install
```bash
pip install -r requirements.txt
```

## Run
```bash
uvicorn main:app --reload
```

## Open in browser
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Endpoints
- `GET /` - welcome message
- `GET /dogs` - list all dogs
- `GET /dogs/{dog_id}` - get one dog
- `POST /dogs` - create a dog
- `PUT /dogs/{dog_id}` - update a dog
- `DELETE /dogs/{dog_id}` - delete a dog

## Example POST body
```json
{
  "name": "Rocky",
  "breed": "German Shepherd",
  "age": 3,
  "owner": "Anita",
  "gender": "Male"
}
```
