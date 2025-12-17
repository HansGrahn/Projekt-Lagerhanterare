import csv
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os

# ======================
#   CSV Files Configuration
# ======================

# Lägg till dina CSV-filer här med namn och filväg
CSV_FILES = {
    "P4P": "ufc_p4p.csv",
    "Flyweight": "ufc_flyweight.csv",
    "Bantamweight": "ufc_bantamweight.csv",
    "Featherweight": "ufc_featherweight.csv",
    "Lightweight": "ufc_lightweight.csv",
    "Welterweight": "ufc_welterweight.csv",
    "Middleweight": "ufc_middleweight.csv",
    "Light Heavyweight": "ufc_light_heavyweight.csv",
    "Heavyweight": "ufc_heavyweight.csv",   
}

PERSONAL_FILE = "my_personal_ufc_ranking.csv"

# ======================
#   Load Data
# ======================

def load_data(filename):
    """Load fighters from CSV file."""
    if not os.path.exists(filename):
        return []
    
    products = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                products.append(row)
    except Exception as e:
        messagebox.showerror("Fel", f"Kunde inte läsa filen {filename}:\n{e}")
    return products


def load_all_divisions():
    """Load fighters i en lista för att visa alla samtidigt."""
    all_fighters = []
    for division, filename in CSV_FILES.items():
        if os.path.exists(filename):
            fighters = load_data(filename)

            # Numrera fighters efter ordning (divisionens rank)
            for i, fighter in enumerate(fighters, start=1):

                # Add missing fields so everything is consistent
                fighter['division'] = division
                fighter['weight_class'] = division
                fighter['division_rank'] = i  # <-- NYTT!

                all_fighters.append(fighter)

    return all_fighters


def add_fighter_to_personal_csv():
    """Add a fighter manually to personal ranking CSV."""
    
    # Ask user for info
    print("Lägg till en fighter i din personliga UFC-ranking:\n")

    name = input("Fighterns namn: ")
    division = input("Division / viktklass: ")
    record = input("Record (ex 15–3): ")

    # Load existing ranking
    fighters = []

    if os.path.exists(PERSONAL_FILE):
        with open(PERSONAL_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                fighters.append(row)

    # Determine new rank number
    new_rank = len(fighters) + 1

    # Create fighter entry
    new_fighter = {
        "rank": new_rank,
        "name": name,
        "division": division,
        "record": record
    }

    # Add to list
    fighters.append(new_fighter)

    # Save back to CSV
    try:
        with open(PERSONAL_FILE, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["rank", "name", "division", "record"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            # Reassign ranking numbers in case file was edited manually
            for i, fighter in enumerate(fighters, start=1):
                fighter["rank"] = i
                writer.writerow(fighter)

        print(f"\n✅ {name} har lagts till i din personliga ranking!")

    except Exception as e:
        print(f"\n❌ Fel vid sparande: {e}")
        
def add_custom_fighter():
    """Open a popup window to manually add a fighter."""

    popup = tk.Toplevel(root)
    popup.title("Lägg till egen fighter")
    popup.geometry("350x320")
    popup.resizable(False, False)

    tk.Label(popup, text="Namn:", font=("Arial", 11)).pack(pady=5)
    name_entry = tk.Entry(popup, width=30)
    name_entry.pack()

    tk.Label(popup, text="Beskrivning:", font=("Arial", 11)).pack(pady=5)
    desc_entry = tk.Entry(popup, width=30)
    desc_entry.pack()

    tk.Label(popup, text="Record:", font=("Arial", 11)).pack(pady=5)
    record_entry = tk.Entry(popup, width=30)
    record_entry.pack()

    # Weightclass dropdown
    tk.Label(popup, text="Viktklass:", font=("Arial", 11)).pack(pady=5)
    weight_var = tk.StringVar()
    weight_dropdown = ttk.Combobox(
        popup,
        textvariable=weight_var,
        values=list(CSV_FILES.keys()),  # ALLA divisioner du definierat
        state="readonly",
        width=27
    )
    weight_dropdown.pack()

    def submit():
        name = name_entry.get().strip()
        desc = desc_entry.get().strip()
        record = record_entry.get().strip()
        weight = weight_var.get().strip()

        if not name or not weight:
            messagebox.showerror("Fel", "Namn och viktklass måste fyllas i!")
            return

        # Create fighter dict
        new_fighter = {
            "id": str(len(personal_ranking) + 1),
            "name": name,
            "description": desc,
            "record": record,
            "division": weight,
            "weight_class": weight
        }

        # Add to personal ranking
        personal_ranking.append(new_fighter)
        refresh_ranking_display()

        # Autosave to CSV
        save_ranking()

        messagebox.showinfo("Klar!", f"{name} lades till i din personliga ranking!")
        popup.destroy()

    tk.Button(
        popup,
        text="Lägg till fighter",
        font=("Arial", 12),
        bg="#4CAF50",
        fg="white",
        width=20,
        command=submit
    ).pack(pady=15)

# ======================
#   GUI Functions
# ======================

def refresh_list():
    """Refresh fighter list in GUI utan dubbletter."""
    listbox.delete(0, tk.END)
    
    selected_division = division_filter_var.get()

    seen = set()   # <-- håller koll på fighters som redan visats

    for p in current_fighters:

        # Filtrering per division
        if selected_division != "Alla divisioner":
            if p.get('division', p.get('weight_class', '')) != selected_division:
                continue

        fighter_name = p["name"]

        # Hoppa över om namnet redan har visats
        if fighter_name in seen:
            continue
        seen.add(fighter_name)

        display_text = f" {p['name']} ({p.get('weight_class', ...)}) #{p['division_rank']}"

        listbox.insert(tk.END, display_text)



def add_to_ranking():
    """Add selected fighter to personal ranking."""
    try:
        index = listbox.curselection()[0]
    except:
        messagebox.showwarning("Fel", "Välj en fighter först.")
        return

    # Find the actual fighter from current_fighters based on filtered view
    selected_division = division_filter_var.get()
    filtered_fighters = []
    
    for p in current_fighters:
        if selected_division != "Alla divisioner":
            if p.get('division', p.get('weight_class', '')) != selected_division:
                continue
        filtered_fighters.append(p)
    
    if index >= len(filtered_fighters):
        messagebox.showwarning("Fel", "Kunde inte hitta fighter.")
        return
    
    fighter = filtered_fighters[index]
    
    # Check if fighter already in ranking
    for ranked_fighter in personal_ranking:
        if ranked_fighter['name'] == fighter['name']:
            messagebox.showwarning("Finns redan", f"{fighter['name']} finns redan i din ranking!")
            return
    
    personal_ranking.append(fighter.copy())
    
    display_text = f"{fighter['name']} ({fighter.get('weight_class', fighter.get('division', 'N/A'))})"
    ranking_listbox.insert(tk.END, display_text)
    
    update_ranking_numbers()


def remove_from_ranking():
    """Remove selected fighter from personal ranking."""
    try:
        index = ranking_listbox.curselection()[0]
    except:
        messagebox.showwarning("Fel", "Välj en fighter från din ranking först.")
        return
    
    fighter = personal_ranking.pop(index)
    ranking_listbox.delete(index)
    
    messagebox.showinfo("Borttagen", f"{fighter['name']} togs bort från din ranking.")
    update_ranking_numbers()


def move_up():
    """Move selected fighter up in ranking."""
    try:
        index = ranking_listbox.curselection()[0]
    except:
        messagebox.showwarning("Fel", "Välj en fighter från din ranking först.")
        return
    
    if index == 0:
        messagebox.showinfo("Info", "Fighter är redan högst upp!")
        return
    
    # Swap fighters
    personal_ranking[index], personal_ranking[index-1] = personal_ranking[index-1], personal_ranking[index]
    
    # Update listbox
    refresh_ranking_display()
    ranking_listbox.selection_clear(0, tk.END)
    ranking_listbox.selection_set(index-1)
    ranking_listbox.see(index-1)


def move_down():
    """Move selected fighter down in ranking."""
    try:
        index = ranking_listbox.curselection()[0]
    except:
        messagebox.showwarning("Fel", "Välj en fighter från din ranking först.")
        return
    
    if index == len(personal_ranking) - 1:
        messagebox.showinfo("Info", "Fighter är redan längst ner!")
        return
    
    # Swap fighters
    personal_ranking[index], personal_ranking[index+1] = personal_ranking[index+1], personal_ranking[index]
    
    # Update listbox
    refresh_ranking_display()
    ranking_listbox.selection_clear(0, tk.END)
    ranking_listbox.selection_set(index+1)
    ranking_listbox.see(index+1)


def refresh_ranking_display():
    """Refresh the ranking listbox display."""
    ranking_listbox.delete(0, tk.END)
    for i, fighter in enumerate(personal_ranking, start=1):
        display_text = f"#{i} {fighter['name']} ({fighter.get('weight_class', fighter.get('division', 'N/A'))})"
        ranking_listbox.insert(tk.END, display_text)


def update_ranking_numbers():
    """Update ranking numbers in display."""
    refresh_ranking_display()


def save_ranking():
    """Save personal ranking to CSV."""
    if not personal_ranking:
        messagebox.showerror("Fel", "Din ranking är tom.")
        return

    try:
        with open(PERSONAL_FILE, "w", newline="", encoding="utf-8") as file:
            if personal_ranking:
                fieldnames = ["rank"] + list(personal_ranking[0].keys())
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                for i, f in enumerate(personal_ranking, start=1):
                    row = {"rank": i}
                    row.update(f)
                    writer.writerow(row)

        messagebox.showinfo("Sparat!", f"Din personliga ranking med {len(personal_ranking)} fighters sparades i:\n{PERSONAL_FILE}")
    except Exception as e:
        messagebox.showerror("Fel", f"Kunde inte spara filen:\n{e}")


def load_saved_ranking():
    """Load previously saved ranking."""
    if not os.path.exists(PERSONAL_FILE):
        messagebox.showinfo("Info", "Ingen sparad ranking hittades.")
        return
    
    try:
        loaded_ranking = load_data(PERSONAL_FILE)
        if loaded_ranking:
            personal_ranking.clear()
            personal_ranking.extend(loaded_ranking)
            refresh_ranking_display()
            messagebox.showinfo("Laddat!", f"Laddade {len(personal_ranking)} fighters från sparad ranking.")
    except Exception as e:
        messagebox.showerror("Fel", f"Kunde inte ladda ranking:\n{e}")


def reset_ranking():
    """Start over."""
    if personal_ranking:
        result = messagebox.askyesno("Bekräfta", "Är du säker på att du vill återställa din ranking?")
        if not result:
            return
    
    ranking_listbox.delete(0, tk.END)
    personal_ranking.clear()


def on_division_filter_change(*args):
    """Handle division filter dropdown change."""
    refresh_list()
    update_status()


def update_status():
    """Update status label with current info."""
    total_fighters = len(current_fighters)
    selected_division = division_filter_var.get()
    
    if selected_division == "Alla divisioner":
        status_label.config(text=f"Visar alla {total_fighters} fighters från alla divisioner", fg="green")
    else:
        filtered_count = sum(1 for f in current_fighters if f.get('division', f.get('weight_class', '')) == selected_division)
        status_label.config(text=f"Visar {filtered_count} fighters från {selected_division}", fg="green")

def add_custom_fighter():
    """Open a popup window to manually add a fighter."""

    popup = tk.Toplevel(root)
    popup.title("Lägg till egen fighter")
    popup.geometry("350x380")
    popup.resizable(False, False)

    # --- Namn ---
    tk.Label(popup, text="Namn:", font=("Arial", 11)).pack(pady=5)
    name_entry = tk.Entry(popup, width=30)
    name_entry.pack()

    # --- Beskrivning ---
    tk.Label(popup, text="Beskrivning:", font=("Arial", 11)).pack(pady=5)
    desc_entry = tk.Entry(popup, width=30)
    desc_entry.pack()

    # --- Record ---
    tk.Label(popup, text="Record:", font=("Arial", 11)).pack(pady=5)

    frame = tk.Frame(popup)
    frame.pack()

    tk.Label(frame, text="Vinster").grid(row=0, column=0, padx=5)
    wins_entry = tk.Entry(frame, width=5)
    wins_entry.grid(row=1, column=0)

    tk.Label(frame, text="Förluster").grid(row=0, column=1, padx=5)
    loss_entry = tk.Entry(frame, width=5)
    loss_entry.grid(row=1, column=1)

    tk.Label(frame, text="Oavgjort (valfritt)").grid(row=0, column=2, padx=5)
    draw_entry = tk.Entry(frame, width=5)
    draw_entry.grid(row=1, column=2)

    # --- Viktklass ---
    tk.Label(popup, text="Viktklass:", font=("Arial", 11)).pack(pady=5)
    weight_var = tk.StringVar()
    weight_dropdown = ttk.Combobox(
        popup,
        textvariable=weight_var,
        values=list(CSV_FILES.keys()),
        state="readonly",
        width=27
    )
    weight_dropdown.pack()

    # --- Submit ---
    def submit():
        name = name_entry.get().strip()
        desc = desc_entry.get().strip()
        wins = wins_entry.get().strip()
        losses = loss_entry.get().strip()
        draws = draw_entry.get().strip() or "0"
        weight = weight_var.get()

        record = f"{wins}-{losses}-{draws}"

        # Skapa fighter-objektet ENDAST för personliga rankingen
        new_fighter = {
            "id": str(len(personal_ranking) + 1),
            "name": name,
            "description": desc,
            "record": record,
            "division": weight,
            "weight_class": weight
        }

        personal_ranking.append(new_fighter)
        refresh_ranking_display()
        save_ranking()

        messagebox.showinfo("Klar!", f"{name} lades till i din personliga ranking!")
        popup.destroy()

    tk.Button(popup, text="Lägg till", command=submit).pack(pady=15)


def add_custom_csv():
    """Add a custom CSV file to the list."""
    filename = filedialog.askopenfilename(
        title="Välj CSV-fil",
        filetypes=[("CSV-filer", "*.csv"), ("Alla filer", "*.*")]
    )
    
    if filename:
        class_name = os.path.splitext(os.path.basename(filename))[0]
        CSV_FILES[class_name] = filename
        
        # Reload all fighters
        global current_fighters
        current_fighters = load_all_divisions()
        
        # Update dropdown
        all_divisions = ["Alla divisioner"] + sorted(set(f.get('division', f.get('weight_class', '')) for f in current_fighters))
        division_filter_dropdown['values'] = all_divisions
        
        refresh_list()
        messagebox.showinfo("Tillagd", f"Fil tillagd: {class_name}\nTotalt {len(current_fighters)} fighters")

def show_fighter_details(event):
    """Open a popup displaying full fighter details when clicked."""
    try:
        index = listbox.curselection()[0]
    except:
        return  # Om inget valts

    selected_division = division_filter_var.get()
    filtered_fighters = []

    # Filtrera rätt fighters
    for f in current_fighters:
        if selected_division != "Alla divisioner":
            if f.get("division", f.get("weight_class", "")) != selected_division:
                continue
        filtered_fighters.append(f)

    if index >= len(filtered_fighters):
        return

    fighter = filtered_fighters[index]

    # ---- POPUP FÖR DETALJER ----
    popup = tk.Toplevel(root)
    popup.title(fighter["name"])
    popup.geometry("380x330")
    popup.resizable(False, False)

    tk.Label(popup, text=fighter["name"], font=("Arial", 16, "bold")).pack(pady=10)

    details = [
        ("ID", fighter.get("id", "N/A")),
        ("Namn", fighter.get("name", "N/A")),
        ("Beskrivning", fighter.get("description", "N/A")),
        ("Record", fighter.get("record", "N/A")),
        ("Viktklass", fighter.get("weight_class", fighter.get("division", "N/A"))),
        ("Division", fighter.get("division", "N/A")),
        ("Rank", fighter.get("division_rank", "N/A")),
    ]

    for label, value in details:
        tk.Label(
            popup,
            text=f"{label}: {value}",
            font=("Arial", 11),
            anchor="w",
            justify="left",
        ).pack(fill="x", padx=20, pady=2)

    tk.Button(popup, text="Stäng", command=popup.destroy).pack(pady=10)

# ======================
#   Main GUI Window
# ======================

root = tk.Tk()
root.title("UFC All-Divisions Personal Ranking Tool")
root.geometry("1100x650")
root.resizable(False, False)

current_fighters = load_all_divisions()
personal_ranking = []

# Top Frame - Division Filter
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Label(top_frame, text="Filtrera division:", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)

division_filter_var = tk.StringVar()
division_filter_var.set("Alla divisioner")

# Get all unique divisions
all_divisions = ["Alla divisioner"] + sorted(set(f.get('division', f.get('weight_class', '')) for f in current_fighters))

division_filter_dropdown = ttk.Combobox(
    top_frame, 
    textvariable=division_filter_var, 
    values=all_divisions,
    state="readonly",
    width=20,
    font=("Arial", 11)
)
division_filter_dropdown.pack(side=tk.LEFT, padx=5)
division_filter_var.trace('w', on_division_filter_change)

tk.Button(top_frame, text="➕ Lägg till egen CSV", command=add_custom_csv, font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
tk.Button(top_frame, text="📂 Ladda sparad ranking", command=load_saved_ranking, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

# Status Label
status_label = tk.Label(root, text="", font=("Arial", 9), fg="gray")
status_label.pack()

# Main Frame
frame = tk.Frame(root)
frame.pack(pady=10)

# Available Fighters
left_frame = tk.Frame(frame)
left_frame.grid(row=0, column=0, padx=20)

tk.Label(left_frame, text="Tillgängliga fighters", font=("Arial", 14, "bold")).pack()

listbox = tk.Listbox(left_frame, width=45, height=22, font=("Arial", 11))
listbox.pack()

# Buttons
mid_frame = tk.Frame(frame)
mid_frame.grid(row=0, column=1, padx=15)

tk.Button(mid_frame, text="➡ Lägg till", font=("Arial", 11), width=18, command=add_to_ranking, bg="#4CAF50", fg="white").pack(pady=5)
tk.Button(mid_frame, text="⬆ Flytta upp", font=("Arial", 11), width=18, command=move_up).pack(pady=5)
tk.Button(mid_frame, text="⬇ Flytta ner", font=("Arial", 11), width=18, command=move_down).pack(pady=5)
tk.Button(mid_frame, text="❌ Ta bort", font=("Arial", 11), width=18, command=remove_from_ranking, bg="#f44336", fg="white").pack(pady=5)
tk.Label(mid_frame, text="", height=2).pack()  # Spacer
tk.Button(mid_frame, text="🔄 Återställ ranking", font=("Arial", 11), width=18, command=reset_ranking).pack(pady=5)
tk.Button(mid_frame, text="💾 Spara ranking", font=("Arial", 11), width=18, command=save_ranking, bg="#2196F3", fg="white").pack(pady=5)

# Personal Ranking
right_frame = tk.Frame(frame)
right_frame.grid(row=0, column=2, padx=20)

tk.Label(right_frame, text="Din personliga ranking", font=("Arial", 14, "bold")).pack()
tk.Label(right_frame, text="(Alla divisioner kombinerat)", font=("Arial", 9, "italic"), fg="gray").pack()

ranking_listbox = tk.Listbox(right_frame, width=45, height=22, font=("Arial", 11))
ranking_listbox.pack()

#Skriv in fighter

tk.Button(mid_frame, text="➕ Lägg till fighter manuellt", font=("Arial", 11), width=18, command=add_custom_fighter, bg="#8E44AD", fg="white").pack(pady=5)

listbox.bind("<<ListboxSelect>>", show_fighter_details)

# Initialize
refresh_list()
update_status()

root.mainloop()