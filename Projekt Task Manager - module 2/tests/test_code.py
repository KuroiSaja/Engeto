import pytest
import mysql.connector
import Task_manager_mod2.main as main

#Připojení k testovací databázi
@pytest.fixture(scope="module")
def test_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",
        database="test"
    )
    cursor = conn.cursor()

#Vytvoření testovací tabulky
    cursor.execute ("""     
                CREATE TABLE IF NOT EXISTS ukoly (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nazev VARCHAR(255) NOT NULL CHECK (CHAR_LENGTH(nazev) > 0),
                    popis TEXT NOT NULL CHECK (CHAR_LENGTH(popis) > 0),
                    stav ENUM('nezahájeno', 'probíhá', 'hotovo') DEFAULT 'nezahájeno',
                    datum DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            """)
                           
    conn.commit()
#Vytvoření úkoluv databázi
    cursor.execute("""
        INSERT INTO ukoly (nazev, popis)
        VALUES (%s, %s)
    """, ("Úkol1", "Popis1"))
    conn.commit()

##Přepsání globálních proměnných v main.py
    main.conn_db = conn
    main.cursor = cursor

    yield cursor, conn

    cursor.execute("DROP TABLE IF EXISTS ukoly")
    conn.commit()
    cursor.close()
    conn.close()

#TESTY
##CREATE tests
###test zda byl úkol zapsán
def test_pridat_ukol_positive(test_db):
    cursor, conn = test_db
    main.pridat_ukol("Test úkol", "Test popis")
    cursor.execute("SELECT * FROM ukoly WHERE nazev = 'Test úkol'")
    vysledek = cursor.fetchone()
    assert vysledek is not None

###test zda se program ozve pri zadání mezery v názvu 
def test_pridat_ukol_negative(test_db):
    cursor, conn = test_db
    with pytest.raises(ValueError) as info:
        main.pridat_ukol(" ", "Test popis")
    assert str(info.value) == "Název úkolu nesmí být prázdný."

##UPDATE tests
###test zda se správně změní stav úkolu na hotovo
def test_aktualizovat_ukol_positive(test_db):
    cursor, conn = test_db
    cursor.execute("SELECT id FROM ukoly WHERE stav != 'hotovo' LIMIT 1")
    ukol_id = cursor.fetchone()[0]
    main.aktualizovat_ukol(ukol_id, "hotovo")
    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol_id,))
    stav = cursor.fetchone()[0]
    assert stav == "hotovo"

###test zda program upozorní na nesrávně zadaný nový stav
def test_aktualizovat_ukol_negative(test_db):
    cursor, conn = test_db
    cursor.execute("SELECT id FROM ukoly WHERE stav != 'hotovo' LIMIT 1")
    ukol_id = cursor.fetchone()[0]
    with pytest.raises(ValueError) as info:
        main.aktualizovat_ukol(ukol_id, "nechci_to_delat")
    assert "Neplatný stav." in str(info.value)

##DELETE tests
###test zda se smaže úkol
def test_smazat_ukol_positive(test_db):
    cursor, conn = test_db
    cursor.execute("SELECT id FROM ukoly LIMIT 1")
    ukol_id = cursor.fetchone()[0]
    main.odstranit_ukol(ukol_id)
    cursor.execute("SELECT * FROM ukoly WHERE id = %s", (ukol_id,))
    ukol = cursor.fetchone()
    assert ukol is None

###test zda program upozorní na zadané neexistující ID
def test_smazat_ukol_negative():
    with pytest.raises(ValueError) as info:
        main.odstranit_ukol(99)
    assert "neexistuje" in str(info.value)    