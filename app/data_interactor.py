from contact import Contact
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}


def get_connection():
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as e:
        print(e)


def disconnect(conn):
    if conn and conn.is_connected():
        conn.close()



def create_contact(conn, first_name: str, last_name: str, phone_number: str):
    crs = conn.cursor()
    contact = Contact(None, first_name, last_name, phone_number)
    contact_dict = contact.to_dict()
    query = "INSERT INTO contacts (first_name, last_name, phone_number) VALUES (%s, %s, %s)"
    params = (contact_dict["first_name"], contact_dict["last_name"], contact_dict["phone_number"])

    crs.execute(query, params)
    conn.commit()
    new_id = crs.lastrowid
    crs.close()
    return new_id


def get_all_contacts(conn):
    crs = conn.cursor(dictionary=True)
    query = "SELECT * FROM contacts"
    crs.execute(query)
    contact_dicts = crs.fetchall()
    contact_list = list(map(Contact.from_dict, contact_dicts))
    crs.close()
    return contact_list


def update_contact(conn, contact_id: int, first_name: str | None = None,
                   last_name: str | None = None, phone_number: str | None = None) -> bool:
    crs = conn.cursor()
    try:
        query_select = "SELECT * FROM contacts WHERE id = %s"
        crs.execute(query_select, (contact_id,))
        current_data = crs.fetchone()

        if not current_data:
            return False

        query_update = '''
            UPDATE contacts
            SET first_name = %s, last_name = %s, phone_number = %s
            WHERE id = %s
        '''

        params = (
            current_data[1] if first_name is None else first_name,
            current_data[2] if last_name is None else last_name,
            current_data[3] if phone_number is None else phone_number,
            contact_id
        )

        crs.execute(query_update, params)
        conn.commit()
        return True

    except Exception as e:
        print(f"Error updating contact: {e}")
        conn.rollback()
        return False
    finally:
        crs.close()


def delete_contact(conn, contact_id):
    crs = conn.cursor()
    try:
        query_select = "SELECT * FROM contacts WHERE id = %s"
        crs.execute(query_select, (contact_id,))
        current_data = crs.fetchone()

        if not current_data:
            return False

        query_update = '''
                DELETE FROM contacts
                WHERE id = %s
            '''

        crs.execute(query_update, (contact_id,))
        conn.commit()
        return True

    except Exception as e:
        print(f"Error deleting contact: {e}")
        conn.rollback()
        return False
    finally:
        crs.close()