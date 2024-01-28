import tkinter as tk
from tkinter import ttk

class WyszukiwarkaNieruchomosciGUI: 
    def __init__(self, root):
        self.root = root
        self.root.title("Wyszukiwarka Nieruchomości")
        self.saved_lokalizacja = None
        self.saved_cena_max = None
        self.saved_powierzchnia_od = None
        self.saved_powierzchnia_do = None
        self.saved_pokoje = None

        self.label_lokalizacja = ttk.Label(root, text="Lokalizacja:")
        self.label_lokalizacja.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.lokalizacja_var = tk.StringVar()
        self.combo_lokalizacja = ttk.Combobox(root, textvariable=self.lokalizacja_var, values=["Psie Pole", "Krzyki", "Fabryczna", "Śródmieście", "Stare Miasto"])
        self.combo_lokalizacja.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        self.label_cena = ttk.Label(root, text="Cena (max):")
        self.label_cena.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_cena_max = ttk.Entry(root)
        self.entry_cena_max.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        self.label_powierzchnia = ttk.Label(root, text="Powierzchnia (od - do):")
        self.label_powierzchnia.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_powierzchnia_od = ttk.Entry(root)
        self.entry_powierzchnia_od.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        self.entry_powierzchnia_do = ttk.Entry(root)
        self.entry_powierzchnia_do.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)

        self.label_pokoje = ttk.Label(root, text="Liczba pokoi:")
        self.label_pokoje.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

        self.pokoje_var = tk.StringVar()
        self.combo_pokoje = ttk.Combobox(root, textvariable=self.pokoje_var, values=["1", "2", "3", "4"])
        self.combo_pokoje.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

        # Przycisk do uruchamiania wyszukiwania
        self.button_szukaj = ttk.Button(root, text="Szukaj", command=self.wyszukaj_nieruchomosci)
        self.button_szukaj.grid(row=10, column=0, columnspan=3, pady=20)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


    def wyszukaj_nieruchomosci(self):
        self.saved_lokalizacja = self.lokalizacja_var.get()
        self.saved_cena_max = self.entry_cena_max.get()
        self.saved_powierzchnia_od = self.entry_powierzchnia_od.get()
        self.saved_powierzchnia_do = self.entry_powierzchnia_do.get()
        self.saved_pokoje = self.pokoje_var.get()
        self.on_close()

    def on_close(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WyszukiwarkaNieruchomosciGUI(root)
    root.mainloop()
