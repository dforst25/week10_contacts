class Contact:
    def __init__(self, contact_id: int | None, first_name, last_name, phone_number):
        self.id = contact_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return (f"Contact details:\nid: {self.id}\nfirst name: {self.first_name}\n"
                f"last_name: {self.last_name}\nphone number: {self.phone_number}")

    def __repr__(self):
        return (f"Contact details:\nid: {self.id}\nfirst name: {self.first_name}\n"
                f"last_name: {self.last_name}\nphone number: {self.phone_number}")

    @classmethod
    def from_dict(cls, dict_contact: dict):
        return cls(
            dict_contact["id"],
            dict_contact["first_name"],
            dict_contact["last_name"],
            dict_contact["phone_number"]
        )
