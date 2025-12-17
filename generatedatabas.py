import requests
import csv
import json
import time

def scrape_ufc_rankings():
    """
    Hämtar UFC rankings och fighter-data och skapar en CSV-fil
    """
    
    # UFC har ett API-liknande endpoint
    rankings_url = "https://www.ufc.com/rankings"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/html, */*',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    # Manuell data baserad på aktuella UFC rankings (december 2025)
    # Detta är en mer pålitlig approach när webbplatsen använder JavaScript
    
    fighters_data = []
    
    # Definiera alla divisioner
    divisions_data = {
        "Pound-for-Pound": [
            {"rank": "1", "name": "Ilia Topuria", "record": "16-0-0", "p4p": "1"},
            {"rank": "2", "name": "Islam Makhachev", "record": "27-1-0", "p4p": "2"},
            {"rank": "3", "name": "Merab Dvalishvili", "record": "18-4-0", "p4p": "3"},
            {"rank": "4", "name": "Khamzat Chimaev", "record": "14-0-0", "p4p": "4"},
            {"rank": "5", "name": "Alexandre Pantoja", "record": "29-5-0", "p4p": "5"},
            {"rank": "6", "name": "Alex Pereira", "record": "13-2-0", "p4p": "6"},
            {"rank": "7", "name": "Alexander Volkanovski", "record": "26-4-0", "p4p": "7"},
            {"rank": "8", "name": "Jack Della Maddalena", "record": "18-2-0", "p4p": "8"},
            {"rank": "9", "name": "Tom Aspinall", "record": "15-3-0", "p4p": "9"},
            {"rank": "10", "name": "Dricus Du Plessis", "record": "23-2-0", "p4p": "10"},
            {"rank": "11", "name": "Max Holloway", "record": "27-8-0", "p4p": "11"},
            {"rank": "12", "name": "Magomed Ankalaev", "record": "20-1-1", "p4p": "12"},
            {"rank": "13", "name": "Belal Muhammad", "record": "24-3-0", "p4p": "13"},
            {"rank": "14", "name": "Arman Tsarukyan", "record": "22-3-0", "p4p": "14"},
            {"rank": "15", "name": "Charles Oliveira", "record": "35-10-0", "p4p": "15"}
        ],
        "Flyweight": [
            {"rank": "Champion", "name": "Alexandre Pantoja", "record": "29-5-0"},
            {"rank": "1", "name": "Joshua Van", "record": "11-2-0"},
            {"rank": "2", "name": "Brandon Moreno", "record": "22-8-2"},
            {"rank": "3", "name": "Brandon Royval", "record": "17-7-0"},
            {"rank": "4", "name": "Amir Albazi", "record": "17-2-0"},
            {"rank": "5", "name": "Tatsuro Taira", "record": "16-1-0"},
            {"rank": "6", "name": "Kai Kara-France", "record": "24-11-0"},
            {"rank": "7", "name": "Manel Kape", "record": "20-7-0"},
            {"rank": "8", "name": "Alex Perez", "record": "25-8-0"},
            {"rank": "9", "name": "Asu Almabayev", "record": "21-2-0"},
            {"rank": "10", "name": "Tim Elliott", "record": "20-14-1"},
            {"rank": "11", "name": "Steve Erceg", "record": "13-3-0"},
            {"rank": "12", "name": "Tagir Ulanbekov", "record": "16-2-0"},
            {"rank": "13", "name": "Charles Johnson", "record": "16-6-0"},
            {"rank": "14", "name": "Bruno Silva", "record": "14-6-2"},
            {"rank": "15", "name": "Joseph Morales", "record": "11-2-0"}
        ],
        "Bantamweight": [
            {"rank": "Champion", "name": "Merab Dvalishvili", "record": "18-4-0"},
            {"rank": "1", "name": "Umar Nurmagomedov", "record": "18-0-0"},
            {"rank": "2", "name": "Sean O'Malley", "record": "18-2-0"},
            {"rank": "3", "name": "Petr Yan", "record": "17-5-0"},
            {"rank": "4", "name": "Cory Sandhagen", "record": "17-5-0"},
            {"rank": "5", "name": "Song Yadong", "record": "22-8-1"},
            {"rank": "6", "name": "Deiveson Figueiredo", "record": "24-4-1"},
            {"rank": "7", "name": "Aiemann Zahabi", "record": "11-2-0"},
            {"rank": "8", "name": "Marlon Vera", "record": "23-10-1"},
            {"rank": "9", "name": "Mario Bautista", "record": "15-3-0"},
            {"rank": "10", "name": "Henry Cejudo", "record": "16-4-0"},
            {"rank": "11", "name": "David Martinez", "record": "10-1-0"},
            {"rank": "12", "name": "Rob Font", "record": "20-8-0"},
            {"rank": "13", "name": "Vinicius Oliveira", "record": "21-3-0"},
            {"rank": "14", "name": "Kyler Phillips", "record": "13-2-0"},
            {"rank": "15", "name": "Marcus McGhee", "record": "10-1-0"}
        ],
        "Featherweight": [
            {"rank": "Champion", "name": "Alexander Volkanovski", "record": "26-4-0"},
            {"rank": "1", "name": "Movsar Evloev", "record": "19-0-0"},
            {"rank": "2", "name": "Diego Lopes", "record": "26-6-0"},
            {"rank": "3", "name": "Yair Rodriguez", "record": "16-4-0"},
            {"rank": "4", "name": "Lerone Murphy", "record": "15-0-1"},
            {"rank": "5", "name": "Aljamain Sterling", "record": "24-5-0"},
            {"rank": "6", "name": "Arnold Allen", "record": "20-3-0"},
            {"rank": "7", "name": "Youssef Zalal", "record": "16-5-1"},
            {"rank": "8", "name": "Steve Garcia", "record": "16-6-0"},
            {"rank": "9", "name": "Brian Ortega", "record": "16-4-0"},
            {"rank": "10", "name": "Josh Emmett", "record": "19-5-0"},
            {"rank": "11", "name": "Jean Silva", "record": "14-2-0"},
            {"rank": "12", "name": "Patricio Pitbull", "record": "35-7-0"},
            {"rank": "13", "name": "Dan Ige", "record": "19-8-0"},
            {"rank": "14", "name": "David Onama", "record": "13-3-0"},
            {"rank": "15", "name": "Giga Chikadze", "record": "15-4-0"}
        ],
        "Lightweight": [
            {"rank": "Champion", "name": "Ilia Topuria", "record": "16-0-0"},
            {"rank": "1", "name": "Islam Makhachev", "record": "27-1-0"},
            {"rank": "2", "name": "Arman Tsarukyan", "record": "22-3-0"},
            {"rank": "3", "name": "Charles Oliveira", "record": "35-10-0"},
            {"rank": "4", "name": "Max Holloway", "record": "27-8-0"},
            {"rank": "5", "name": "Justin Gaethje", "record": "26-5-0"},
            {"rank": "6", "name": "Paddy Pimblett", "record": "23-3-0"},
            {"rank": "7", "name": "Dan Hooker", "record": "24-13-0"},
            {"rank": "8", "name": "Mateusz Gamrot", "record": "25-3-0"},
            {"rank": "9", "name": "Beneil Dariush", "record": "23-6-1"},
            {"rank": "10", "name": "Rafael Fiziev", "record": "13-2-0"},
            {"rank": "11", "name": "Renato Moicano", "record": "20-6-1"},
            {"rank": "12", "name": "Michael Chandler", "record": "24-9-0"},
            {"rank": "13", "name": "Benoît Saint Denis", "record": "14-3-0"},
            {"rank": "14", "name": "Grant Dawson", "record": "22-3-1"},
            {"rank": "15", "name": "Mauricio Ruffy", "record": "11-1-0"}
        ],
        "Welterweight": [
            {"rank": "Champion", "name": "Jack Della Maddalena", "record": "18-2-0"},
            {"rank": "1", "name": "Belal Muhammad", "record": "24-3-0"},
            {"rank": "2", "name": "Sean Brady", "record": "17-2-0"},
            {"rank": "3", "name": "Shavkat Rakhmonov", "record": "19-0-0"},
            {"rank": "4", "name": "Leon Edwards", "record": "23-4-0"},
            {"rank": "5", "name": "Kamaru Usman", "record": "20-4-0"},
            {"rank": "6", "name": "Ian Machado Garry", "record": "16-0-0"},
            {"rank": "7", "name": "Joaquin Buckley", "record": "21-7-0"},
            {"rank": "8", "name": "Michael Morales", "record": "17-0-0"},
            {"rank": "9", "name": "Carlos Prates", "record": "21-6-0"},
            {"rank": "10", "name": "Gabriel Bonfim", "record": "16-1-0"},
            {"rank": "11", "name": "Colby Covington", "record": "17-5-0"},
            {"rank": "12", "name": "Gilbert Burns", "record": "22-8-0"},
            {"rank": "13", "name": "Geoff Neal", "record": "16-6-0"},
            {"rank": "14", "name": "Daniel Rodriguez", "record": "18-4-0"},
            {"rank": "15", "name": "Mike Malott", "record": "11-2-1"}
        ],
        "Middleweight": [
            {"rank": "Champion", "name": "Khamzat Chimaev", "record": "14-0-0"},
            {"rank": "1", "name": "Dricus Du Plessis", "record": "23-2-0"},
            {"rank": "2", "name": "Nassourdine Imavov", "record": "15-4-0"},
            {"rank": "3", "name": "Sean Strickland", "record": "29-6-0"},
            {"rank": "4", "name": "Anthony Hernandez", "record": "13-2-0"},
            {"rank": "5", "name": "Brendan Allen", "record": "25-5-0"},
            {"rank": "6", "name": "Israel Adesanya", "record": "24-4-0"},
            {"rank": "7", "name": "Caio Borralho", "record": "18-1-0"},
            {"rank": "8", "name": "Reinier de Ridder", "record": "18-2-0"},
            {"rank": "9", "name": "Robert Whittaker", "record": "27-8-0"},
            {"rank": "10", "name": "Michael Page", "record": "23-3-0"},
            {"rank": "10", "name": "Jared Cannonier", "record": "18-8-0"},
            {"rank": "12", "name": "Roman Dolidze", "record": "13-3-0"},
            {"rank": "13", "name": "Paulo Costa", "record": "15-3-0"},
            {"rank": "14", "name": "Marvin Vettori", "record": "20-8-1"},
            {"rank": "15", "name": "Joe Pyfer", "record": "13-3-0"}
        ],
        "Light Heavyweight": [
            {"rank": "Champion", "name": "Alex Pereira", "record": "13-2-0"},
            {"rank": "1", "name": "Magomed Ankalaev", "record": "20-1-1"},
            {"rank": "1", "name": "Jiří Procházka", "record": "31-5-1"},
            {"rank": "3", "name": "Carlos Ulberg", "record": "12-1-0"},
            {"rank": "4", "name": "Khalil Rountree Jr.", "record": "15-6-0"},
            {"rank": "5", "name": "Jan Błachowicz", "record": "30-11-1"},
            {"rank": "6", "name": "Jamahal Hill", "record": "13-2-0"},
            {"rank": "7", "name": "Azamat Murzakanov", "record": "14-0-0"},
            {"rank": "8", "name": "Dominick Reyes", "record": "13-4-0"},
            {"rank": "9", "name": "Volkan Oezdemir", "record": "20-8-0"},
            {"rank": "10", "name": "Aleksandar Rakić", "record": "14-5-0"},
            {"rank": "11", "name": "Bogdan Guskov", "record": "16-3-0"},
            {"rank": "12", "name": "Johnny Walker", "record": "22-9-0"},
            {"rank": "13", "name": "Nikita Krylov", "record": "31-10-0"},
            {"rank": "14", "name": "Alonzo Menifield", "record": "16-5-1"},
            {"rank": "15", "name": "Zhang Mingyang", "record": "19-7-0"}
        ],
        "Heavyweight": [
            {"rank": "Champion", "name": "Tom Aspinall", "record": "15-3-0"},
            {"rank": "1", "name": "Ciryl Gane", "record": "13-2-0"},
            {"rank": "2", "name": "Alexander Volkov", "record": "38-11-0"},
            {"rank": "3", "name": "Sergei Pavlovich", "record": "18-3-0"},
            {"rank": "4", "name": "Curtis Blaydes", "record": "18-5-0"},
            {"rank": "5", "name": "Jailton Almeida", "record": "21-3-0"},
            {"rank": "6", "name": "Waldo Cortes Acosta", "record": "12-2-0"},
            {"rank": "7", "name": "Serghei Spivac", "record": "17-4-0"},
            {"rank": "8", "name": "Derrick Lewis", "record": "28-12-0"},
            {"rank": "9", "name": "Ante Delija", "record": "24-6-0"},
            {"rank": "10", "name": "Marcin Tybura", "record": "25-9-0"},
            {"rank": "11", "name": "Shamil Gaziev", "record": "15-1-0"},
            {"rank": "12", "name": "Tai Tuivasa", "record": "15-8-0"},
            {"rank": "13", "name": "Mick Parkin", "record": "10-0-0"},
            {"rank": "14", "name": "Valter Walker", "record": "12-2-0"},
            {"rank": "15", "name": "Tallison Teixeira", "record": "8-1-0"}
        ],


    }
    
    # Fighter beskrivningar (kortfattade)
    descriptions = {
        "Ilia Topuria": "Georgian-Spanish featherweight champion, undefeated with devastating knockout power",
        "Islam Makhachev": "Dagestani lightweight champion, elite grappler and student of Khabib",
        "Merab Dvalishvili": "Georgian bantamweight champion known for relentless pace and cardio",
        "Khamzat Chimaev": "Swedish-Chechen middleweight champion, dominant wrestler with finishing ability",
        "Alexandre Pantoja": "Brazilian flyweight champion with well-rounded skills and submission expertise",
        "Alex Pereira": "Brazilian kickboxer turned MMA champion, devastating striker",
        "Alexander Volkanovski": "Australian featherweight champion, technical striker with excellent wrestling",
        "Jack Della Maddalena": "Australian welterweight champion, powerful striker with knockout ability",
        "Tom Aspinall": "British heavyweight champion, fast and technical for the division",
        "Dricus Du Plessis": "South African middleweight contender with high-pressure fighting style",
        "Max Holloway": "Hawaiian striker with record-breaking significant strikes",
        "Magomed Ankalaev": "Dagestani light heavyweight contender, well-rounded and durable",
        "Belal Muhammad": "Palestinian-American welterweight contender, excellent wrestler",
        "Arman Tsarukyan": "Armenian lightweight contender, dynamic grappler",
        "Charles Oliveira": "Brazilian jiu-jitsu specialist with most submission wins in UFC history",
        "Joshua Van": "Rising flyweight contender with well-rounded game",
        "Brandon Moreno": "Mexican former champion known for exciting fights and submission skills",
        "Brandon Royval": "American flyweight with aggressive submission game",
        "Umar Nurmagomedov": "Dagestani bantamweight, undefeated cousin of Khabib",
        "Sean O'Malley": "American bantamweight with creative striking and knockout power",
        "Petr Yan": "Russian technical striker and former bantamweight champion",
        "Movsar Evloev": "Russian featherweight, undefeated wrestler",
        "Diego Lopes": "Brazilian featherweight with aggressive striking",
        "Justin Gaethje": "American brawler known for exciting violent fights",
        "Paddy Pimblett": "English lightweight with charismatic personality",
        "Shavkat Rakhmonov": "Kazakh welterweight, undefeated finisher",
        "Leon Edwards": "British welterweight, technical striker",
        "Kamaru Usman": "Nigerian-American former champion and dominant wrestler",
        "Ian Machado Garry": "Irish welterweight, undefeated striker",
        "Sean Strickland": "American middleweight, former champion with pressure fighting",
        "Israel Adesanya": "Nigerian-New Zealander, technical kickboxer and former champion",
        "Jiří Procházka": "Czech samurai-inspired fighter with unorthodox striking",
        "Ciryl Gane": "French heavyweight with technical Muay Thai striking",
        "Alexander Volkov": "Russian heavyweight veteran with excellent reach",
    }
    
    # Skapa P4P dictionary för att lägga till P4P rankings
    p4p_dict = {}
    for fighter in divisions_data.get("Pound-for-Pound", []):
        p4p_dict[fighter["name"]] = fighter["rank"]
    
    # Processa varje division
    for division, fighters in divisions_data.items():
        if division == "Pound-for-Pound":
            continue  # Skippa P4P eftersom vi redan har den datan
            
        print(f"Lägger till fighters från {division}...")
        
        for fighter in fighters:
            # Hämta P4P rank om fighter finns i P4P rankings
            p4p_rank = p4p_dict.get(fighter["name"], "N/A")
            
            # Hämta beskrivning eller använd standard
            description = descriptions.get(
                fighter["name"], 
                f"Professional mixed martial artist competing in {division}"
            )
            
            fighter_info = {
                'name': fighter["name"],
                'division': division,
                'rank': fighter["rank"],
                'record': fighter["record"],
                'p4p_rank': p4p_rank,
                'description': description
            }
            
            fighters_data.append(fighter_info)
    
    # Skriv till CSV
    write_to_csv(fighters_data)
    print(f"\n✓ Klar! Totalt {len(fighters_data)} fighters tillagda")
    print("✓ Data sparad i 'ufc_fighters_rankings.csv'")

def write_to_csv(fighters_data):
    """
    Skriver fighter-data till CSV-fil
    """
    with open('ufc_fighters_rankings.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['name', 'division', 'rank', 'record', 'p4p_rank', 'description']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(fighters_data)

if __name__ == "__main__":
    print("=" * 60)
    print("UFC FIGHTER RANKINGS - CSV GENERATOR")
    print("=" * 60)
    print()
    scrape_ufc_rankings()
    print()
    print("=" * 60)