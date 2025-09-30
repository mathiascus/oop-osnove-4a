#zadtak 2: bankovni racun
class BankovniRacun:
    #klasa koja modelira jednostavna bankovni racun.
    def __init__(self,ime_prezime,broj_racuna):
        #konsturktor za BankovniRačun
        self.ime_prezime = ime_prezime
        self.broj_racuna = broj_racuna
        self.stanje = 0.0
    
    def uplati(self,iznos):
        """metoda za uplatu na račun"""
        if iznos > 0:
            self.stanje += iznos
            print(f"Uplata od {iznos:.2f} EUR na račun {self.broj_racuna} je uspješna.")
        else:
            print("Neispravan iznos za uplatu. Iznos mora biti pozitivan.")
    def isplati(self,iznos):
        if iznos < self.stanje:
            self.stanje -= iznos
            print(f"Isplata od {iznos:.2f} EUR uspješna.Novo stanje {self.stanje} EU.")
        elif iznos < 0:
            print("Nije moguce isplatiti negativan broj.")
        else:
            print("Isplata nije moguca. Iznos mora biti manji od stanja računa.(Stanje: {self.stanje:.2f})")
    def info(self):
        print("-" * 25)
        print(f"Vlasnik: {self.ime_vlasnika}")
        print(f"Broj_racuna: {self.broj_racuna}")
        print(f"Stanje: {self.stanje:.2f} eur")
        print("-" * 25)

#Testiranje klase
racun1 = BankovniRacun("Pero Perić","HR123456789")
racun1.info()
racun1.uplati(1000)
racun1.isplati(250)
racun1.isplati(800) #POkušaj isplate prevelikog iznosa.
racun1.isplati(-50) #Pokusah isplate neg broja.
racun1.info()
print("\n" + "="*30 + "\n")
