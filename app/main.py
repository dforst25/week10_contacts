from data_interactor import *
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class ContactBody(BaseModel):
    first_name: str
    last_name: str
    phone_number: str


@app.get("/contacts")
def get_all_contacts_api():
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        contacts = get_all_contacts(conn)
        return contacts
    finally:
        disconnect(conn)


@app.post("/contacts")
def create_contact_api(contact: ContactBody):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        new_id = create_contact(conn, contact.first_name, contact.last_name, contact.phone_number)
        return {
            "message": "Contact created successfully",
            "id": new_id
        }
    finally:
        disconnect(conn)


@app.put("/contacts/{id}")
def update_contact_api(id: int, updated_contact: ContactBody):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        result = update_contact(conn, id, updated_contact.first_name, updated_contact.last_name,
                                updated_contact.phone_number)
        message = "contact updated successfully" if result else "Failed updating contact"
        return {
            "message": message
        }
    finally:
        disconnect(conn)


@app.delete("/contacts/{id}")
def delete_contact_api(id: int):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        result = delete_contact(conn, id)
        message = "contact removed successfully" if result else "Failed removing contact"
        return {
            "message": message
        }
    finally:
        disconnect(conn)


if __name__ == "__main__":
    uvicorn.run(app)