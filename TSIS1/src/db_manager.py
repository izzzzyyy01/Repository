import psycopg2
import json
from config import params

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(**params)
        self.conn.autocommit = True

    def search_full(self, query):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            return cur.fetchall()

    def export_json(self, filename="../data/contacts.json"):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, c.email, c.birthday, g.name, 
                       array_agg(p.phone || ' (' || p.type || ')')
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                GROUP BY c.id, g.name
            """)
            rows = cur.fetchall()
            data = [
                {"name": r[0], "email": r[1], "birthday": str(r[2]), "group": r[3], "phones": r[4]} 
                for r in rows
            ]
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)

    def import_json(self, filename="../data/contacts.json"):
        with open(filename, "r") as f:
            data = json.load(f)
            with self.conn.cursor() as cur:
                for entry in data:
                 
                    cur.execute("SELECT id FROM contacts WHERE name = %s", (entry['name'],))
                    exists = cur.fetchone()
                    if exists:
                        ans = input(f"Contact {entry['name']} exists. Overwrite? (y/n): ")
                        if ans.lower() != 'y': continue
                    
               
                    cur.execute("INSERT INTO contacts (name, email) VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET email = EXCLUDED.email", 
                                (entry['name'], entry.get('email')))
