#Připojení k databázi
import mysql.connector

##funkce připojení
def pripojeni_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1111",
            database="spravce_ukolu"
        )
        return conn
###upozorni na chybu připojení    
    except mysql.connector.Error as err:
        print(f"Chyba při připojování: {err}")
        return None

###podoba tabulky
tabulka_sql = """     
                CREATE TABLE IF NOT EXISTS ukoly (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nazev VARCHAR(255) NOT NULL CHECK (CHAR_LENGTH(nazev) > 0),
                    popis TEXT NOT NULL CHECK (CHAR_LENGTH(popis) > 0),
                    stav ENUM('nezahájeno', 'probíhá', 'hotovo') DEFAULT 'nezahájeno',
                    datum DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            """

##Vytvoř tabulku v databázi, pokud tam žádná není
def vytvoreni_tabulky():
    cursor.execute("SHOW TABLES LIKE 'ukoly'")
    vysledek = cursor.fetchone()
    if vysledek:
        print("Připojení je OK.")
    else:
        cursor.execute(tabulka_sql)
        print("Byla vytvořena nová tabulka 'ukoly'. Můžete zadat svůj první úkol.")

#Funkce programu
##podoba hlavního menu
menu = """
Správce úkolů - Hlavní menu
1. Přidat úkol
2. Zobrazit úkoly
3. Aktualizovat úkol
4. Odstranit úkol
5. Ukončit program
"""

##hlavní program
def hlavni_menu():
    global conn_db, cursor
    conn_db = pripojeni_db()
    cursor = conn_db.cursor()
###navaž spojení s databází, pokud to jde a zajisti tabulku v databázi   
    if conn_db == None:
        print("S databází se nepodařilo navázat spojení. Program bude ukončen.")
        exit()
    else:    
        vytvoreni_tabulky()
###vyber funkci dle výběru uživatele
    while True:
        print (menu)
        user_choice = input("Vyberte možnost (1-4):")
        if user_choice == "1":      #CREATE
    ####Donuť uživatele zadat název a popis, kontrola v pridat_ukol
            while True:
                nazev = input("Zadejte název úkolu: ").strip()
                popis = input("Zadejte popis úkolu: ").strip()
                try:
                    pridat_ukol(nazev, popis)
                    break
                except ValueError as e:
                    print(f"Chyba: {e}")
        elif user_choice == "2":    #READ
            zobrazit_ukoly ()
        elif user_choice == "3":    #UPDATE
        ####kontrola zda je co aktualizovat
            if not seznam_nehotove_ukoly():
                print("Žádné aktivní úkoly nebyly nalezeny.")
                continue
            while True:
                try:
                    while True:
        ####zadání ID a kontrola                   
                        ukol_up = int(input("Zadejte ID úkolu, jehož stav chcete aktualizovat: "))
                        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (ukol_up,))
                        if cursor.fetchone() is None:
                            print(f"Úkol s ID {ukol_up} neexistuje.")
                        else:
                            break
        ####zadání nového stavu, kontrola stavu je v aktualizovat_ukol, neptej se mě proč, prostě je tam a už o tom nechci mluvit
                    novy_stav = input(f"Zadejte nový stav úkolu č.{ukol_up} ('probíhá' nebo 'hotovo'): ").strip().lower()
        ####potvrzení změny a konrola vstupu potvrzení
                    while True:
                        potvrzeni_up = input(f"Opravdu chcete změnit stav úkolu č.{ukol_up} na '{novy_stav}'? (a/n): ").strip().lower()
                        if potvrzeni_up in ['a', 'n']:
                            break
                        else:
                            print("Zadejte prosím pouze 'a' pro ano nebo 'n' pro ne.")
                    if potvrzeni_up == 'a':
                        aktualizovat_ukol(ukol_up, novy_stav)
                        break
                    else:
                        print("Změna byla zrušena.")
                        break
                except ValueError:
                    print("Chyba: Zadejte platné číselné ID.")
        elif user_choice == "4":    #DELETE
        ####kontrola zda je co smazat
            if not seznam_ukolu():
                print("Žádné úkoly nebyly nalezeny.")
                continue
            while True:
                try:
        ####zadání ID, kontrola je v odstranit_ukol            
                    ukol_del = int(input("Zadejte ID úkolu který chcete smazat: "))
        ####potvrzení smazání            
                    while True:
                        potvrzeni_up = input(f"Opravdu chcete smazet úkol č.{ukol_del}? (a/n): ").strip().lower()
                        if potvrzeni_up in ['a', 'n']:
                            break
                        else:
                            print("Zadejte prosím pouze 'a' pro ano nebo 'n' pro ne.")
                    if potvrzeni_up == 'a':
                        try:
                            odstranit_ukol(ukol_del)
                            break
                        except ValueError as e:
                            print(f"Chyba: {e}")
                    else:
                        print("Smazání úkolu bylo zrušeno.")
                        break
                except ValueError:
                    print("Chyba: Zadejte platné číselné ID.")
        elif user_choice == "5":    #KONEC PROGRAMU
            conn_db.close()
            print ("""
Konec programu.""")
            break
###to je sice hezké, ale taková možnost neexistuje
        else:
            print ("""
Taková možnost neexistuje, zkus to znovu.""")

#CREATE fce
def pridat_ukol (nazev, popis):
##upozornění na prázdný název nebo popis
    if not nazev.strip():
        raise ValueError("Název úkolu nesmí být prázdný.")
    if not popis.strip():
        raise ValueError("Popis úkolu nesmí být prázdný.")
##zapiš úkol do databáze
    hodnoty_sql = "INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)"
    cursor.execute(hodnoty_sql, (nazev, popis))
    conn_db.commit()
    print(f"Úkol '{nazev}' byl přidán do seznamu úkolů.")

#READ fce
def zobrazit_ukoly():
##najdi úkoly které nejsou hotové
    cursor.execute("""
        SELECT id, nazev, popis, stav
        FROM ukoly
        WHERE stav IN ('nezahájeno', 'probíhá')
        ORDER BY datum ASC
    """)
    seznam_ukolu = cursor.fetchall()
##žádné úkoly tam nejsou, smutné, nemáme co na práci
    if not seznam_ukolu:
        print("Žádné aktivní úkoly nebyly nalezeny.")
##zobraz nalezené úkoly, které nejsou hotové
    else:
        print("\nSeznam aktuálních úkolů:")
        for id, nazev, popis, stav in seznam_ukolu:
            print(f"{id}. {nazev} - {popis} | Stav: {stav}")

#UPDATE fce
##najdi úkoly které nejsou hotové a zobraz je
def seznam_nehotove_ukoly():
    cursor.execute("""
        SELECT id, nazev, stav
        FROM ukoly
        WHERE stav IN ('nezahájeno', 'probíhá')
        ORDER BY datum ASC
    """)
    seznam_ukolu = cursor.fetchall()
    if seznam_ukolu:
        print("\nSeznam úkolů:")
        for id, nazev, stav in seznam_ukolu:
            print(f"{id}. {nazev} | Stav: {stav}")
        return True    
    else:    
        return False
def aktualizovat_ukol(ukol_up, novy_stav):
##kontrola nového stavu
    if novy_stav not in ['probíhá', 'hotovo']:
        raise ValueError("Neplatný stav. Stav musí být 'probíhá' nebo 'hotovo'. Úkol zůstal nezměněn.")
##zapiš změny   
    cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, ukol_up))
    conn_db.commit()
    print(f"Stav úkolu č.{ukol_up} byl aktualizován na '{novy_stav}'.")  

#DELETE fce
##najdi seznam všech úkolů
def seznam_ukolu():
    cursor.execute("""
        SELECT id, nazev, stav
        FROM ukoly
        ORDER BY datum ASC
    """)
    seznam_ukolu = cursor.fetchall()
    if seznam_ukolu:
        print("\nSeznam úkolů:")
        for id, nazev, stav in seznam_ukolu:
            print(f"{id}. {nazev} | Stav: {stav}")
        return True    
    else:    
        return False          
def odstranit_ukol(ukol_del):
##kontrola jestli existuje ID    
    cursor.execute("SELECT id FROM ukoly WHERE id = %s", (ukol_del,))
    if cursor.fetchone() is None:
        raise ValueError(f"Úkol s ID {ukol_del} neexistuje.")
##odstraň úkol           
    cursor.execute("DELETE FROM ukoly WHERE id = %s", (ukol_del,))
    conn_db.commit()
    print(f"Úkol č. {ukol_del} byl úspěšně odstraněn.")


#spuštění programu
if __name__ == "__main__":
    hlavni_menu()

