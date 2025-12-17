'''
Projekt_V1.PY: Lagerhanterare för ufc rankningarna.

__author__  = Hans-Ove Grahn
__version__ = "1.0.0"
__email__   = hans-ove.grahn@elev.ga.dbgy.se
'''

import csv
import os

FILENAME = "ufc_mens_p4p_products.csv"

def list_products(products):
    for idx, product in enumerate(products, start=1):
        print(f"{idx}: {product['name']} ({product['division_rank']}) - {product['weight_class']} - Record: {product['record']}")

def view_product(idx, products):
    return products[idx - 1]

def load_data(filename):
    products = []
    
    with open(filename, "r", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            p = {
                "id": int(row['id']),
                "name": row['name'],
                "description": row['description'],
                "record": row['record'],
                "weight_class": row['weight_class'],
                "division_rank": row['division_rank']
            }
            products.append(p)
    return products

def get_product_by_id(product_id, products):
    for product in products:
        if product["id"] == product_id:
            return product
    return None

def visa_produkt_med_id(products):
    idx = int(input("Välj produkt med id: "))
    product = get_product_by_id(idx, products)
    if product:
        print(f"{product['name']} - {product['description']}")
        print(f"Record: {product['record']} | Weight Class: {product['weight_class']} | Rank: {product['division_rank']}")
    else:
        print("Produkten hittades inte.")

def lägga_till_produkt(products):
    name = input("Namn: ")
    desc = input("Beskrivning: ")
    record = input("Record: ")
    weight_class = input("Viktklass: ")
    division_rank = input("Rank: ")

    new_id = max(p["id"] for p in products) + 1

    new_product = {
        "id": new_id,
        "name": name,
        "description": desc,
        "record": record,
        "weight_class": weight_class,
        "division_rank": division_rank
    }

    products.append(new_product)
    spara(products)

    print("Produkten har lagts till.")

def ta_bort_produkt(products):
    idx = int(input("Ange produktens id som ska tas bort: "))
    product = get_product_by_id(idx, products)

    if product:
        products.remove(product)
        spara(products)
        print("Produkten har tagits bort.")
    else:
        print("Produkten hittades inte.")

def edit_product(product):
    print("Ändra produkt:", product['name'])

    product['name'] = input("Nytt namn: ") or product['name']
    product['description'] = input("Ny beskrivning: ") or product['description']
    product['record'] = input("Nytt record: ") or product['record']
    product['weight_class'] = input("Ny viktklass: ") or product['weight_class']
    product['division_rank'] = input("Ny rank: ") or product['division_rank']

    return f"Ändrade: {product['id']}"

def spara(products):
    with open(FILENAME, "w", newline="", encoding='utf-8') as file:
        fieldnames = ["id", "name", "description", "record", "weight_class", "division_rank"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
import csv

def skapa_personlig_rankning(products):
    print("\n=== Skapa din personliga UFC P4P-ranking ===\n")
    print("Välj fighters i den ordning du vill ranka dem.")

    # Kopiera listan så den inte påverkar originalet
    available = products.copy()
    personal_ranking = []

    while available:
        print("\nTillgängliga fighters:")
        for idx, fighter in enumerate(available, start=1):
            print(f"{idx}. {fighter['name']} ({fighter['weight_class']})")

        try:
            val = int(input("\nVälj en fighter (nummer): "))
            if val < 1 or val > len(available):
                print("Felaktigt val, försök igen.")
                continue
        except ValueError:
            print("Skriv ett nummer.")
            continue

        chosen = available.pop(val - 1)
        personal_ranking.append(chosen)

        print(f"✔ {chosen['name']} lades till i din ranking!")

        if not available:
            break

        cont = input("Vill du fortsätta? (j/n): ").lower()
        if cont != 'j':
            break

    # Spara till CSV
    filename = "my_personal_ufc_rankings.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["rank", "id", "name", "description", "record", "weight_class", "division_rank"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for i, fighter in enumerate(personal_ranking, start=1):
            row = {"rank": i}
            row.update(fighter)
            writer.writerow(row)

    print(f"\n Din personliga ranking sparades i '{filename}'\n")

def Menu(products):
    print("==========================================================================")
    print("1. Visa pound for pound rakningarna")
    print("2. Visa fighter med rank")
    print("3. Lägg till fighter")
    print("4. Ta bort fighter med rank")
    print("5. Ändra fighter")
    print("6. Egen rankning")

    val = input("Välj ett alternativ (1–6): ")

    if val == "1":
        list_products(products)
    elif val == "2":
        visa_produkt_med_id(products)
    elif val == "3":
        lägga_till_produkt(products)
    elif val == "4":
        ta_bort_produkt(products)
    elif val == "5":
        idx = int(input("Ange Fighterns rank som ska ändras: "))
        product = get_product_by_id(idx, products)
        if product:
            edit_product(product)
            spara(products)
        else:
            print("Produkten hittades inte.")
    elif val == "6":
        skapa_personlig_rankning(products)


while True:
    products = load_data(FILENAME)
    Menu(products)
    os.system("pause")
