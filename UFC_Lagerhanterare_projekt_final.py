'''
UFC_Lagerhanterare_projekts_final.PY: Lagerhanterare för ufc rankningarna.

__author__  = Hans-Ove Grahn
__version__ = "1.0.0"
__email__   = hans-ove.grahn@elev.ga.dbgy.se
'''
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os

class UFCFighterManager:
    def __init__(self, root):
        self.root = root
        self.root.title("UFC Fighter Lagerhanterare")
        self.root.geometry("1200x700")
        
        # Data storage
        self.fighters = []
        self.csv_file = "ufc_fighters_rankings.csv"
        self.sort_reverse = {}  
        
        # Create main layout
        self.create_widgets()
        
        self.division_order = { #rankar från lättast till tyngst
    "Flyweight": 1,
    "Bantamweight": 2,
    "Featherweight": 3,
    "Lightweight": 4,
    "Welterweight": 5,
    "Middleweight": 6,
    "Light Heavyweight": 7,
    "Heavyweight": 8
}

        
        # Load data om csv finns
        if os.path.exists(self.csv_file):
            self.load_data()
        
    def create_widgets(self):
        # Top frame for controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        # Title
        title_label = ttk.Label(control_frame, text="UFC FIGHTER LAGERHANTERARE", 
                                font=("Arial", 16, "bold"))
        title_label.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Lägg till Fighter", 
                   command=self.add_fighter_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Redigera", 
                   command=self.edit_fighter_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Ta bort", 
                   command=self.delete_fighter).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Spara", 
                   command=self.save_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Ladda", 
                   command=self.load_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exportera", 
                   command=self.export_data).pack(side=tk.LEFT, padx=5)
        
        # Sök fighter
        search_frame = ttk.Frame(control_frame)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="Sök:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_fighters)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        #Dropdown divisioner
        ttk.Label(search_frame, text="Division:").pack(side=tk.LEFT, padx=5)
        self.division_filter = ttk.Combobox(search_frame, width=20, state="readonly")
        self.division_filter['values'] = ["Alla", "Flyweight", "Bantamweight", "Featherweight", 
                                          "Lightweight", "Welterweight", "Middleweight", 
                                          "Light Heavyweight", "Heavyweight"]
        self.division_filter.set("Alla")
        self.division_filter.bind('<<ComboboxSelected>>', lambda e: self.search_fighters())
        self.division_filter.pack(side=tk.LEFT, padx=5)
        
        # Treeview ram
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Create treeview med iid 
        self.tree = ttk.Treeview(tree_frame, columns=("name", "division", "rank", "record", "p4p", "description"),
                                 show="headings", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Columner
        self.tree.heading("name", text="Namn", command=lambda: self.sort_column("name"))
        self.tree.heading("division", text="Division", command=lambda: self.sort_column("division"))
        self.tree.heading("rank", text="Rank", command=lambda: self.sort_column("rank"))
        self.tree.heading("record", text="Record", command=lambda: self.sort_column("record"))
        self.tree.heading("p4p", text="P4P Rank", command=lambda: self.sort_column("p4p"))
        self.tree.heading("description", text="Beskrivning")
        
        self.tree.column("name", width=150)
        self.tree.column("division", width=150)
        self.tree.column("rank", width=80)
        self.tree.column("record", width=100)
        self.tree.column("p4p", width=80)
        self.tree.column("description", width=400)
        
        # Pack treeview and scrollbars
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Redo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Dubbelklick
        self.tree.bind('<Double-1>', self.on_double_click)
        
    def load_data(self):
        """Ladda data från CSV-fil"""
        if not os.path.exists(self.csv_file):
            messagebox.showwarning("Varning", f"Filen {self.csv_file} finns inte!")
            return
        
        try:
            self.fighters = []
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.fighters.append(row)
            
            self.refresh_tree()
            self.status_bar.config(text=f"Laddade {len(self.fighters)} fighters från {self.csv_file}")
            messagebox.showinfo("Framgång", f"Laddade {len(self.fighters)} fighters!")
        except Exception as e:
            messagebox.showerror("Fel", f"Kunde inte ladda data: {str(e)}")
    
    def save_data(self):
        """Spara data till CSV-fil"""
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['name', 'division', 'rank', 'record', 'p4p_rank', 'description']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.fighters)
            
            self.status_bar.config(text=f"Sparade {len(self.fighters)} fighters till {self.csv_file}")
            messagebox.showinfo("Framgång", "Data sparad!")
        except Exception as e:
            messagebox.showerror("Fel", f"Kunde inte spara data: {str(e)}")
    
    def refresh_tree(self):
        """Uppdatera trädet med aktuell data"""
        # clear
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get filter
        division = self.division_filter.get()
        search_term = self.search_var.get().lower()
        
        # Add filtered items
        for idx, fighter in enumerate(self.fighters):
            # Apply filters
            if division != "Alla" and fighter['division'] != division:
                continue
            
            if search_term and search_term not in fighter['name'].lower():
                continue
            
            # Use the index as iid so we can map back to the fighter easily
            self.tree.insert("", tk.END, iid=str(idx), values=(
                fighter['name'],
                fighter['division'],
                fighter['rank'],
                fighter['record'],
                fighter.get('p4p_rank', 'N/A'),
                fighter['description']
            ))
    
    def on_double_click(self, event):
        """Hantera dubbelklick - redigera endast om det är en datarad"""
        # Identifiera vad som klickades på
        region = self.tree.identify_region(event.x, event.y)
        
        # Om det är en header/heading, gör ingenting
        if region == "heading":
            return
        
        # Kontrollera om det finns en vald rad
        if not self.tree.selection():
            return
        
        # Om det är en datarad (cell), öppna redigering
        if region == "cell" or region == "tree":
            self.edit_fighter_dialog()
    
    def search_fighters(self, *args):
        """Sök fighters"""
        self.refresh_tree()
    
    def add_fighter_dialog(self):
        """Dialog för att lägga till fighter"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Lägg till Fighter")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create form
        ttk.Label(dialog, text="Namn:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Division:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        division_combo = ttk.Combobox(dialog, width=37, state="readonly")
        division_combo['values'] = ["Flyweight", "Bantamweight", "Featherweight", "Lightweight", 
                                    "Welterweight", "Middleweight", "Light Heavyweight", "Heavyweight"]
        division_combo.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Rank:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        rank_entry = ttk.Entry(dialog, width=40)
        rank_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Record:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        record_entry = ttk.Entry(dialog, width=40)
        record_entry.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="P4P Rank:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        p4p_entry = ttk.Entry(dialog, width=40)
        p4p_entry.insert(0, "N/A")
        p4p_entry.grid(row=4, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Beskrivning:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        desc_text = tk.Text(dialog, width=40, height=5)
        desc_text.grid(row=5, column=1, padx=10, pady=5)
        
        def save_fighter():
            fighter = {
                'name': name_entry.get(),
                'division': division_combo.get(),
                'rank': rank_entry.get(),
                'record': record_entry.get(),
                'p4p_rank': p4p_entry.get(),
                'description': desc_text.get("1.0", tk.END).strip()
            }
            
            if not fighter['name'] or not fighter['division']:
                messagebox.showwarning("Varning", "Namn och Division är obligatoriska!")
                return
            
            self.fighters.append(fighter)
            self.refresh_tree()
            self.status_bar.config(text=f"Lade till {fighter['name']}")
            dialog.destroy()
        
        ttk.Button(dialog, text="Spara", command=save_fighter).grid(row=6, column=0, columnspan=2, pady=20)
    
    def edit_fighter_dialog(self):
        """Dialog för att redigera fighter"""
        selected = self.tree.selection()
        if not selected:
            # Endast visa meddelande om det faktiskt är ett manuellt försök att redigera
            # Inte vid dubbelklick på tomma områden
            return
        
        # Get the index from the iid
        fighter_index = int(selected[0])
        
        if fighter_index >= len(self.fighters):
            messagebox.showerror("Fel", "Kunde inte hitta fighter!")
            return
        
        fighter = self.fighters[fighter_index]
        
        # Popup för fighter
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Redigera Fighter - {fighter['name']}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Labels för redigerings box
        ttk.Label(dialog, text="Namn:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.insert(0, fighter['name'])
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        #Dropdown vy för divisioner
        ttk.Label(dialog, text="Division:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        division_combo = ttk.Combobox(dialog, width=37, state="readonly")
        division_combo['values'] = ["Flyweight", "Bantamweight", "Featherweight", "Lightweight",  
                                    "Welterweight", "Middleweight", "Light Heavyweight", "Heavyweight"]
        division_combo.set(fighter['division'])
        division_combo.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Rank:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        rank_entry = ttk.Entry(dialog, width=40)
        rank_entry.insert(0, fighter['rank'])
        rank_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Record:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        record_entry = ttk.Entry(dialog, width=40)
        record_entry.insert(0, fighter['record'])
        record_entry.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="P4P Rank:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        p4p_entry = ttk.Entry(dialog, width=40)
        p4p_entry.insert(0, fighter.get('p4p_rank', 'N/A'))
        p4p_entry.grid(row=4, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Beskrivning:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        desc_text = tk.Text(dialog, width=40, height=5)
        desc_text.insert("1.0", fighter['description'])
        desc_text.grid(row=5, column=1, padx=10, pady=5)
        
        def update_fighter():
            self.fighters[fighter_index] = {
                'name': name_entry.get(),
                'division': division_combo.get(),
                'rank': rank_entry.get(),
                'record': record_entry.get(),
                'p4p_rank': p4p_entry.get(),
                'description': desc_text.get("1.0", tk.END).strip()
            }
            
            self.refresh_tree()
            self.status_bar.config(text=f"Uppdaterade {name_entry.get()}")
            dialog.destroy()
        
        ttk.Button(dialog, text="Uppdatera", command=update_fighter).grid(row=6, column=0, columnspan=2, pady=20)
    
    def delete_fighter(self):
        """Ta bort vald fighter"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Varning", "Välj en fighter att ta bort!")
            return
        
        # Get the index from the iid
        fighter_index = int(selected[0])
        
        if fighter_index >= len(self.fighters):
            messagebox.showerror("Fel", "Kunde inte hitta fighter!")
            return
        
        fighter = self.fighters[fighter_index]
        
        # Bekräfta ta bort
        if not messagebox.askyesno("Bekräfta", f"Ta bort {fighter['name']}?"):
            return
        
        # Ta bort Fighter
        del self.fighters[fighter_index]
        
        self.refresh_tree()
        self.status_bar.config(text=f"Tog bort {fighter['name']}")
    
    def export_data(self):
        """Exportera data till ny CSV-fil"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    fieldnames = ['name', 'division', 'rank', 'record', 'p4p_rank', 'description']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.fighters)
                
                messagebox.showinfo("Framgång", f"Data exporterad till {filename}")
            except Exception as e:
                messagebox.showerror("Fel", f"Kunde inte exportera: {str(e)}")
    
    def sort_column(self, col):
        """Sortera kolumn med intelligent sortering och toggle reverse"""
        # Toggle reverse för column (ascending, descending ordning)
        if col not in self.sort_reverse:
            self.sort_reverse[col] = False
        else:
            self.sort_reverse[col] = not self.sort_reverse[col]
        
        reverse = self.sort_reverse[col]
                
        data = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Sorting för rank column
        if col == "rank":
            def rank_key(item):
                val = item[0]
                if val == "Champion":
                    return (0, 0)  # Champion först
                try:
                    return (1, int(val))  # Nummer ranks
                except ValueError:
                    return (2, val)  # annan value
            
            data.sort(key=rank_key, reverse=reverse)
        
        # Special sorting for P4P rank column
        elif col == "p4p":
            def p4p_key(item):
                val = item[0]
                if val == "N/A" or val == "":
                    return (1, 999)  # N/A sist
                try:
                    return (0, int(val))  # Numerad P4P ranks
                except ValueError:
                    return (1, 999)
            
            data.sort(key=p4p_key, reverse=reverse) #Sortera från lättast till tyngst
        elif col == "division":
            def division_key(item):
                val = item[0]
                return self.division_order.get(val, 999)
            data.sort(key=division_key, reverse=reverse)

        # Sorting för record column (wins-losses-draws)
        elif col == "record":
            def record_key(item):
                val = item[0]
                try:
                    # Parse record like "18-4-0"
                    parts = val.split('-')
                    if len(parts) >= 2:
                        wins = int(parts[0])
                        losses = int(parts[1])
                        draws = int(parts[2]) if len(parts) > 2 else 0
                        # Sort wins (descending), losses (ascending)
                        return (-wins, losses, draws)
                    return (0, 0, 0)
                except (ValueError, IndexError):
                    return (0, 0, 0)
            
            data.sort(key=record_key, reverse=reverse)
        
        # Alfabetisk sortering för name
        else:
            data.sort(key=lambda x: x[0].lower(), reverse=reverse)
                
        for index, (val, item) in enumerate(data):
            self.tree.move(item, '', index)
        
        # Update status bar för direction
        direction = "↓" if reverse else "↑"
        self.status_bar.config(text=f"Sorterad på {col} {direction}")
    
    

if __name__ == "__main__":
    root = tk.Tk()
    app = UFCFighterManager(root)
    root.mainloop()