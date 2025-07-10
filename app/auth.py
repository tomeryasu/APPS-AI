import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
print("DATABASE_URL:", os.getenv("DATABASE_URL"))
import psycopg
from passlib.context import CryptContext

DB_URL = os.getenv("DATABASE_URL")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_conn():
    return psycopg.connect(DB_URL)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    conn.commit()
    c.close()
    conn.close()

def create_user(name: str, email: str, password: str) -> bool:
    hashed = pwd_context.hash(password)
    try:
        conn = get_conn()
        c = conn.cursor()
        c.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (name, email, hashed))
        conn.commit()
        c.close()
        conn.close()
        return True
    except psycopg2.IntegrityError:
        return False
    except Exception as e:
        print(f"Error in create_user: {e}")
        return False

def verify_user(email: str, password: str) -> bool:
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE email = %s', (email,))
    row = c.fetchone()
    c.close()
    conn.close()
    if row and pwd_context.verify(password, row[0]):
        return True
    return False
