from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from data_interactor import DataInteractor
import uvicorn

app = FastAPI()
db = DataInteractor()


class ContactBody(BaseModel):
    first_name: str
    last_name: str
    phone_number: str


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None


@app.get("/contacts")
def get_all_contacts_api():
    contacts = db.get_all_contacts()
    return contacts


@app.post("/contacts")
def create_contact_api(contact: ContactBody):
    new_id = db.create_contact(contact.first_name, contact.last_name, contact.phone_number)
    if not new_id:
        raise HTTPException(status_code=500, detail="Failed to create contact")
    return {
        "message": "Contact created successfully",
        "id": new_id
    }


@app.put("/contacts/{id}")
def update_contact_api(id: int, updated_contact: ContactUpdate):
    update_data = updated_contact.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    result = db.update_contact(id, **update_data)

    if not result:
        raise HTTPException(status_code=404, detail="Contact not found or no changes made")

    return {"message": "Contact updated successfully", "updated_fields": list(update_data.keys())}


@app.delete("/contacts/{id}")
def delete_contact_api(id: int):
    result = db.delete_contact(id)
    if not result:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact removed successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
