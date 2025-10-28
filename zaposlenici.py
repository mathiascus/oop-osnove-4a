class Zaposlenik:
    def __init__(self,ime,prezime,placa):
        self.ime = ime
        self.prezime = prezime
        self.placa = placa
    
    def info(self):
        print(f"Ime i prezime:{self.ime}{self.prezime}, Plaća:{self.placa}EUR")
class Programer(Zaposlenik):
    def __init__(self, ime, prezime, placa, programski_jezici):
        super().__init__(ime,prezime,placa)
        self.programski_jezici = programski_jezici

    def info(self):
        super().info()
        print(f"Programski jezici: {', '.join(self.programski_jezici)}")

class Menadzer(Zaposlenik):
    def __init__(self, ime, prezime, placa, tim):
        super().__init__(ime, prezime, placa)
        self.tim = tim

    def info(self):
        super().info()
        print("Tim:", ", ".join(self.tim))

#Korištenje
z1 = Zaposlenik("Ana", "Anić", 1200)
p1 = Programer("Petar", "Perić", 1800, ["Python", "JavaScript"])
m1 = Menadzer("Iva", "Ivić", 2500, ["Ana Anić", "Petar Perić"])

# Pozivanje metoda
print("--- Podaci o zaposleniku ---")
z1.info()

print("\n--- Podaci o programeru ---")
p1.info()

print("\n--- Podaci o menadžeru ---")
m1.info()
