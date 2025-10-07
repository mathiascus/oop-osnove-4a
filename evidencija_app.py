class Ucenik:
    def __init__(self,ime,prezime,razred):
        self.ime=ime
        self.prezime=prezime
        self.razred=razred
    

    def __str__(self):
        return f"{self.ime} {self.prezime}, {self.razred}. razred"


#test klase
print(Ucenik("Pero","Peric","4.a"))

import tkinter as tk

class EvidencijaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evidencija učenika")
        self.root.geometry("500x400")

        #Konfiguracija responzivnosti
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        unos_frame = tk.Frame(self.root, padx=10, pady=10)
        unos_frame.grid(row=0, column=0, sticky="EW")

        #Okvir za prikaz (lista)
        prikaz_frame = tk.Frame(self.root, padx=10, pady=10)
        prikaz_frame.grid(row=1, column=0, sticky="NSEW") 
#Responzivnost unutar okvira za prikaz
        prikaz_frame.columnconfigure(0, weight=1)
        prikaz_frame.rowconfigure(0, weight=1)

#Widgeti za unos
#Ime
        tk.Label(unos_frame, text="Ime:").grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.ime_entry = tk.Entry(unos_frame)
        self.ime_entry.grid(row=0, column=1, padx=5, pady=5, sticky="EW")

# Prezime
        tk.Label(unos_frame, text="Prezime:").grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.prezime_entry = tk.Entry(unos_frame)
        self.prezime_entry.grid(row=1, column=1, padx=5, pady=5, sticky="EW")

#Razred
        tk.Label(unos_frame, text="Razred:").grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.razred_entry = tk.Entry(unos_frame)
        self.razred_entry.grid(row=2, column=1, padx=5, pady=5, sticky="EW")

#Gumbi
        self.dodaj_gumb = tk.Button(unos_frame, text="Dodaj učenika")
        self.dodaj_gumb.grid(row=3, column=0, padx=5, pady=10)

        self.spremi_gumb = tk.Button(unos_frame, text="Spremi izmjene")
        self.spremi_gumb.grid(row=3, column=1, padx=5, pady=10, sticky="W")

#Widgeti za prikaz
        self.listbox = tk.Listbox(prikaz_frame)
        self.listbox.grid(row=0, column=0, sticky="NSEW")

#Scrollbar za listbox
        scrollbar = tk.Scrollbar(prikaz_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.listbox.bind('<<ListboxSelect>>', self.odaberi_ucenika)

    def dodaj_ucenika(self):
        ime = self.ime_entry.get().strip()
        prezime = self.prezime_entry.get().strip()
        razred = self.razred_entry.get().strip()

        if not ime and not prezime or not razred:
            messagebox.showwarning("Neispravan unos", "Molimo unesite ime, prezime i razred učenika.")
            return
        novi_ucenik = Ucenik(ime, prezime, razred)
        self.ucenici.append(novi_ucenik)
        self.azuriraj_listbox()
        self.ocisti_unos()
        
    def azuriraj_listbox(self):
            
if __name__ == "__main__":
    root = tk.Tk()
    app = EvidencijaApp(root)
    root.mainloop()
