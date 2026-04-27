from db_manager import DBManager

db = DBManager()

def main_menu():
    while True:
        print("\n--- PhoneBook Advanced ---")
        print("1. Search by Name/Email/Phone")
        print("2. Paginated View (Next/Prev)")
        print("3. Export to JSON")
        print("4. Exit")
        
        choice = input("Choice: ")
        
        if choice == "1":
            q = input("Query: ")
            for r in db.search_full(q): print(r)
        
        elif choice == "2":
            page = 0
            while True:
                with db.conn.cursor() as cur:
                    cur.execute("SELECT * FROM contacts ORDER BY name LIMIT 5 OFFSET %s", (page * 5,))
                    rows = cur.fetchall()
                    for r in rows: print(r)
                
                nav = input("\n[n]ext, [p]rev, [q]uit: ").lower()
                if nav == 'n': page += 1
                elif nav == 'p' and page > 0: page -= 1
                elif nav == 'q': break
        
        elif choice == "3":
            db.export_json()
            print("Exported to data/contacts.json")
            
        elif choice == "4":
            break

if __name__ == "__main__":
    main_menu()
