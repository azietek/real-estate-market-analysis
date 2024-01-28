import tkinter as tk
from tkinter import ttk

class WyszukiwarkaNieruchomosciGUI: 
    def __init__(self, root):
        self.root = root
        self.root.title("Wyszukiwarka Nieruchomości")

        # Tworzenie etykiet i pól do wprowadzania danych
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
        # Tutaj możesz dodać kod do przetwarzania wprowadzonych danych, np. wysłanie zapytania do bazy danych
        # i wyświetlenie wyników na ekranie lub w innym formacie.

        # Poniżej znajduje się przykład wyświetlenia wprowadzonych danych w konsoli.
        print("Lokalizacja:", self.lokalizacja_var.get())
        print("Cena (max):", self.entry_cena_max.get())
        print("Powierzchnia (od - do):", self.entry_powierzchnia_od.get(), "-", self.entry_powierzchnia_do.get())
        print("Liczba pokoi:", self.pokoje_var.get())
        self.on_close()

    def on_close(self):
        # This method will be called when the user attempts to close the window
        if self.root:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WyszukiwarkaNieruchomosciGUI(root)
    root.mainloop()

