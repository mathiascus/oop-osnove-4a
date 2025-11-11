import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import xml.etree.ElementTree as ET

#MODEL 
# Osnovna klasa koja predstavlja bilo koji medij (film ili album)
# Sadrži zajedničke atribute i metodu za spremanje u XML
class Medij:
    def __init__(self, naziv, godina, zanr, ocjena=0, status="Želim", putanja=""):
        self.naziv = naziv
        self.godina = godina
        self.zanr = zanr
        self.ocjena = ocjena
        self.status = status
        self.putanja = putanja

    def to_xml(self, parent):
    # Pretvara objekt u XML element kako bi se mogao spremiti u datoteku
        elem = ET.SubElement(parent, self.__class__.__name__)
        for key, value in vars(self).items():
            child = ET.SubElement(elem, key)
            child.text = str(value)
        return elem

class Film(Medij):
    def __init__(self, naziv, godina, zanr, redatelj, ocjena=0, status="Želim", putanja=""):
        super().__init__(naziv, godina, zanr, ocjena, status, putanja)
        self.redatelj = redatelj

    def to_xml(self, parent):
        elem = super().to_xml(parent)
        ET.SubElement(elem, "redatelj").text = self.redatelj
        return elem
# Podklase Film i Album koje nasljeđuju zajedničke osobine iz klase Medij
# Svaka ima dodatni atribut (redatelj ili izvođač)
class Album(Medij):
    def __init__(self, naziv, godina, zanr, izvodac, ocjena=0, status="Želim", putanja=""):
        super().__init__(naziv, godina, zanr, ocjena, status, putanja)
        self.izvodac = izvodac

    def to_xml(self, parent):
        elem = super().to_xml(parent)
        ET.SubElement(elem, "izvodac").text = self.izvodac
        return elem


#APLIKACIJA 
class MediaShelfApp(tk.Tk):
    # Glavna klasa aplikacije - postavlja prozor i pokreće sučelje
    def __init__(self):
        super().__init__()
        self.title("🎬 MediaShelf - Katalog medija")
        self.geometry("1000x600")
        self.configure(bg="#dfefff")

        self.mediji = []
        self._kreiraj_menu()
        self._kreiraj_gui()
        self.ucitaj_xml()
        self.osvjezi_statusnu_traku()

   
    def _kreiraj_menu(self):
        #Kreira meni traku s opcijama za spremanje, učitavanje i izlaz.
        #Meni traka aplikacije s opcijama za rad s datotekama i prikaz informacija
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Spremi", command=self.spremi_xml)
        file_menu.add_command(label="Učitaj", command=self.ucitaj_xml)
        file_menu.add_separator()
        file_menu.add_command(label="Izlaz", command=self.destroy)
        menu.add_cascade(label="Datoteka", menu=file_menu)

        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label="O aplikaciji", command=self.o_aplikaciji)
        menu.add_cascade(label="Pomoć", menu=help_menu)

        self.config(menu=menu)

    
    def _kreiraj_gui(self):
        #Koristi se LabelFrame za organizaciju unosa (Vrsta, Naziv, Godina, itd.).
        #Combobox služi za odabir vrste medija (Film/Album).
        #Scale omogućuje unos ocjene 1–5.
        #Entry polja služe za unos teksta.
        #Gumb “…” otvara FileDialog za odabir datoteke.
        frame_unos = ttk.LabelFrame(self, text="Unos medija")
        frame_unos.pack(fill="x", padx=10, pady=5) #automatski slaže elemente po redovima ili stupcima

        ttk.Label(frame_unos, text="Vrsta:").grid(row=0, column=0)
        self.vrsta_cb = ttk.Combobox(frame_unos, values=["Film", "Album"], width=10)
        self.vrsta_cb.grid(row=0, column=1)
        self.vrsta_cb.current(0)

        ttk.Label(frame_unos, text="Naziv:").grid(row=0, column=2)
        self.naziv_entry = ttk.Entry(frame_unos, width=20)
        self.naziv_entry.grid(row=0, column=3)

        ttk.Label(frame_unos, text="Godina:").grid(row=0, column=4)
        self.godina_entry = ttk.Entry(frame_unos, width=10)
        self.godina_entry.grid(row=0, column=5)

        ttk.Label(frame_unos, text="Žanr:").grid(row=1, column=0)
        self.zanr_entry = ttk.Entry(frame_unos, width=15)
        self.zanr_entry.grid(row=1, column=1)

        ttk.Label(frame_unos, text="Redatelj/Izvođač:").grid(row=1, column=2)
        self.autor_entry = ttk.Entry(frame_unos, width=20)
        self.autor_entry.grid(row=1, column=3)

        ttk.Label(frame_unos, text="Ocjena:").grid(row=1, column=4)
        self.ocjena_scale = ttk.Scale(frame_unos, from_=1, to=5, orient="horizontal")
        self.ocjena_scale.grid(row=1, column=5)

        ttk.Label(frame_unos, text="Status:").grid(row=2, column=0)
        self.status_cb = ttk.Combobox(frame_unos, values=["Posjedujem", "Želim", "Pogledao/Poslušao"])
        self.status_cb.grid(row=2, column=1)
        self.status_cb.current(1)

        ttk.Label(frame_unos, text="Putanja:").grid(row=2, column=2)
        self.putanja_entry = ttk.Entry(frame_unos, width=30)
        self.putanja_entry.grid(row=2, column=3)
        ttk.Button(frame_unos, text="...", command=self.odaberi_putanju).grid(row=2, column=4)

        ttk.Button(frame_unos, text="Dodaj", command=self.dodaj_medij).grid(row=3, column=3, pady=5)

        # Pretraga
        frame_pretraga = ttk.LabelFrame(self, text="Pretraga i sortiranje")
        frame_pretraga.pack(fill="x", padx=10, pady=5)
        ttk.Label(frame_pretraga, text="Pretraga:").pack(side="left")
        self.search_entry = ttk.Entry(frame_pretraga, width=30)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(frame_pretraga, text="Traži", command=self.pretrazi).pack(side="left", padx=5)
        ttk.Label(frame_pretraga, text="Sortiraj po:").pack(side="left", padx=5)
        self.sort_cb = ttk.Combobox(frame_pretraga, values=["Naziv", "Godina", "Ocjena"], width=10)
        self.sort_cb.pack(side="left")
        ttk.Button(frame_pretraga, text="Sortiraj", command=self.sortiraj).pack(side="left", padx=5)

        #Treeview prikazuje tablični prikaz svih medija.
        #Svaki redak predstavlja jedan film ili album.
        #Klikom na redak prikazuju se detalji.
        self.tree = ttk.Treeview(self, columns=("Vrsta", "Naziv", "Godina", "Žanr", "Autor", "Ocjena", "Status"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.prikazi_detalje)

        # Statusna traka
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

    #FUNKCIJE
    def odaberi_putanju(self):
        putanja = filedialog.askopenfilename()
        if putanja:
            self.putanja_entry.delete(0, tk.END)
            self.putanja_entry.insert(0, putanja)

    def dodaj_medij(self):                  #Preuzima podatke iz polja.
        vrsta = self.vrsta_cb.get()         #Ovisno o vrsti (Film/Album), stvara odgovarajući objekt.
        naziv = self.naziv_entry.get()      #Dodaje ga u listu self.mediji i osvježava prikaz.
        godina = self.godina_entry.get()
        zanr = self.zanr_entry.get()
        autor = self.autor_entry.get()
        ocjena = round(self.ocjena_scale.get(), 1)
        status = self.status_cb.get()
        putanja = self.putanja_entry.get()

        if not naziv:
            messagebox.showwarning("Upozorenje", "Naziv je obavezan!")
            return

        if vrsta == "Film":
            medij = Film(naziv, godina, zanr, autor, ocjena, status, putanja)
        else:
            medij = Album(naziv, godina, zanr, autor, ocjena, status, putanja)

        self.mediji.append(medij)
        self.osvjezi_prikaz()
        self.osvjezi_statusnu_traku()

    def osvjezi_prikaz(self, lista=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        prikaz = lista if lista else self.mediji
        for m in prikaz:
            autor = getattr(m, "redatelj", getattr(m, "izvodac", ""))
            self.tree.insert("", "end", values=(m.__class__.__name__, m.naziv, m.godina, m.zanr, autor, m.ocjena, m.status))

    def sortiraj(self):     
        
        #Parametar key određuje po kojem atributu se sortira.
        #lambda je anonimna funkcija — mala funkcija napisana "u jednoj liniji".
        #Ovdje znači:"Za svaki element m iz liste, uzmi njegov atribut m.ocjena kao ključ za usporedbu."             
        kriterij = self.sort_cb.get()
        if kriterij == "Naziv":
            self.mediji.sort(key=lambda m: m.naziv.lower())
        elif kriterij == "Godina":
            self.mediji.sort(key=lambda m: m.godina)
        elif kriterij == "Ocjena":
            self.mediji.sort(key=lambda m: m.ocjena, reverse=True)
        self.osvjezi_prikaz()

    def pretrazi(self):
        pojam = self.search_entry.get().lower()
        rezultat = [m for m in self.mediji if pojam in m.naziv.lower() or pojam in m.zanr.lower() or pojam in str(getattr(m, 'redatelj', getattr(m, 'izvodac', ''))).lower()]
        self.osvjezi_prikaz(rezultat)

    def prikazi_detalje(self, event):
        selektirano = self.tree.selection()
        if selektirano:
            indeks = self.tree.index(selektirano[0])
            m = self.mediji[indeks]
            autor = getattr(m, "redatelj", getattr(m, "izvodac", ""))
            detalji = f"Vrsta: {m.__class__.__name__}\nNaziv: {m.naziv}\nGodina: {m.godina}\nŽanr: {m.zanr}\nAutor: {autor}\nOcjena: {m.ocjena}\nStatus: {m.status}\nPutanja: {m.putanja}"
            if m.putanja and os.path.exists(m.putanja):
                if messagebox.askyesno("Pokreni datoteku?", f"{detalji}\n\nŽelite li otvoriti datoteku?"):
                    os.startfile(m.putanja)
            else:
                messagebox.showinfo("Detalji", detalji)

    def spremi_xml(self):
        root = ET.Element("MediaShelf")
        for m in self.mediji:
            m.to_xml(root)
        stablo = ET.ElementTree(root)
        stablo.write("mediji.xml", encoding="utf-8", xml_declaration=True)
        messagebox.showinfo("Spremanje", "Katalog je spremljen u 'mediji.xml'")

    def ucitaj_xml(self):
        if not os.path.exists("mediji.xml"):
            return
        stablo = ET.parse("mediji.xml")
        root = stablo.getroot()
        self.mediji.clear()
        for elem in root:
            podaci = {child.tag: child.text for child in elem}
            if elem.tag == "Film":
                self.mediji.append(Film(**podaci))
            elif elem.tag == "Album":
                self.mediji.append(Album(**podaci))
        self.osvjezi_prikaz()
        self.osvjezi_statusnu_traku()

    def osvjezi_statusnu_traku(self):
        if not self.mediji:
            self.status_var.set("Nema unosa.")
        else:
            prosjek = sum(float(m.ocjena) for m in self.mediji) / len(self.mediji)
            self.status_var.set(f"Ukupno medija: {len(self.mediji)} | Prosječna ocjena: {prosjek:.2f}")

    def o_aplikaciji(self):
        messagebox.showinfo("O aplikaciji", "MediaShelf © 2025\nAutor: Vaše ime\nKatalog filmova i glazbenih albuma s ocjenama i statusima.")


if __name__ == "__main__":
    app = MediaShelfApp()
    app.mainloop()
