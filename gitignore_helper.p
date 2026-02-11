# gitignore_helper.py

def add_to_gitignore(filename=".env"):
    try:
        # 'a+' mód: hozzáfűzéshez nyitja meg, és létrehozza, ha nem létezik
        with open(".gitignore", "a+") as f:
            # Ugorjunk a fájl elejére ellenőrizni a tartalmat
            f.seek(0)
            content = f.read()
            
            # Csak akkor adjuk hozzá, ha még nincs benne
            if filename not in content:
                # Biztosítjuk, hogy új sorba kerüljön
                if content and not content.endswith('\n'):
                    f.write('\n')
                f.write(f"{filename}\n")
                print(f"Sikeresen hozzáadva: {filename}")
            else:
                print(f"A(z) {filename} már szerepel a .gitignore fájlban.")
                
    except Exception as e:
        print(f"Hiba történt: {e}")

if __name__ == "__main__":
    add_to_gitignore()
