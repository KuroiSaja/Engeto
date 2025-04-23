#definice objektů
menu = """
Správce úkolů - Hlavní menu
1. Přidat nový úkol
2. Zobrazit všechny úkoly
3. Odstranit úkol
4. Konec programu
"""

ukoly = []


#definice funkcí
def hlavni_menu():
    while True:
        print (menu)
##zadej už. input
        user_choice = input("Vyberte možnost (1-4):")
##vyber funkci dle výběru
        if user_choice == "1":
            pridat_ukol ()
        elif user_choice == "2":
            zobrazit_ukoly (ukoly)
        elif user_choice == "3":
            odstranit_ukol (ukoly)
        elif user_choice == "4":
            print ("""
Konec programu.""")
            break
##upozorni pokud je input neplatný
        else:
            print ("""
Taková možnost neexistuje, zkus to znovu.""")


def pridat_ukol ():
    while True:
##zadej název a upozorni, pokud je prázdný input
        nazev = input("Zadejte název úkolu: ").strip()
        if not nazev:
            print("Název úkolu nesmí být prázdný!")
            continue
##zadej popis a upozorni pokud je prázdný input        
        popis = input("Zadejte popis úkolu: ").strip()
        if not popis:
            print("Popis úkolu nesmí být prázdný!")
            continue
##přidej úkol a popis do slovníku        
        ukoly.append({"název": nazev, "popis": popis})
        print(f"Úkol '{nazev}' byl přidán do seznamu úkolů.")
        break



def zobrazit_ukoly(ukoly):
##slovník je prázdný
    if not ukoly:
        print("Žádné úkoly nebyly nalezeny.")
    else:
##očísluj úkoly a zobraz seznam
        print ("\nSeznam úkolů:")
        for i, ukol in enumerate(ukoly, start=1):
            print(f"{i}. {ukol['název']} - {ukol['popis']}")
    
def odstranit_ukol(ukoly):
##zobraz seznam jako ve fci zobrazit_ukoly   
###slovník je prázdný
    if not ukoly:
        print("Seznam úkolů je prázdný. Není co mazat.")
        return
###zobraz seznam    
    print ("\nSeznam úkolů:")
    for i, ukol in enumerate(ukoly, start=1):
        print(f"{i}. {ukol['název']} - {ukol['popis']}")
##vyber a vymaž úkol, pokud to jde    
    try:
###zadej už. input
        volba = int(input("Zadej číslo úkolu, který chceš odstranit: "))
###zkontroluj jestli je v seznamu
        if 1 <= volba <= len(ukoly):
            odstraneny = ukoly.pop(volba - 1)
            print(f"Úkol '{odstraneny['název']}' byl odstraněn.")
        else:
            print(f"V seznamu neexistuje úkol s číslem {volba}.")
###dej chybu, pokud to není číslo    
    except ValueError:
        print("Zadej prosím platné číslo.")



#run programu
hlavni_menu ()
