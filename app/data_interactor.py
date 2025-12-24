import mysql.connector
import os
from dotenv import load_dotenv
from contact import Contact

load_dotenv()


class DataInteractor:
    def __init__(self):
        self.config = {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT", 3306)),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME")
        }

    def _get_connection(self):
        try:
            return mysql.connector.connect(**self.config)
        except mysql.connector.Error as e:
            print(f"Connection Error: {e}")
            return None

    def create_contact(self, first_name: str, last_name: str, phone_number: str):
        conn = self._get_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        try:
            query = "INSERT INTO contacts (first_name, last_name, phone_number) VALUES (%s, %s, %s)"
            cursor.execute(query, (first_name, last_name, phone_number))
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.Error as e:
            print(f"Error creating contact: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    def get_all_contacts(self):
        conn = self._get_connection()
        if not conn:
            return []

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM contacts")
            rows = cursor.fetchall()
            return [Contact.from_dict(row) for row in rows]
        finally:
            cursor.close()
            conn.close()

    def update_contact(self, contact_id: int, **kwargs) -> bool:
        conn = self._get_connection()
        if not conn:
            return False

        updates = []
        params = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key} = %s")
                params.append(value)

        if not updates:
            return False

        params.append(contact_id)
        query = f"UPDATE contacts SET {', '.join(updates)} WHERE id = %s"

        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as e:
            print(f"Update Error: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_contact(self, contact_id: int) -> bool:
        conn = self._get_connection()
        if not conn:
            return False

        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as e:
            print(f"Delete Error: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
