# gitignore_helper.py

def update_gitignore():
    # Ez a lista tartalmazza azokat a mappákat/fájlokat, amiket el akarunk rejteni
    ignored_items = [
        ".env",
        "node_modules/",
        "artifacts/",
        "cache/",
        "coverage/",
        "*.log"
    ]
    
    try:
        # Megnyitjuk a fájlt olvasásra és írásra (a+)
        with open(".gitignore", "a+") as f:
            f.seek(0)
            existing_content = f.read().splitlines()
            
            print("--- .gitignore frissítése ---")
            
            for item in ignored_items:
                if item not in existing_content:
                    f.write(f"{item}\n")
                    print(f"[+] Hozzáadva: {item}")
                else:
                    print(f"[-] Már szerepel: {item}")
                    
        print("\nKész! A .gitignore fájlod naprakész.")
        
    except Exception as error:
        print(f"Hiba történt a művelet során: {error}")

if __name__ == "__main__":
    update_gitignore()
