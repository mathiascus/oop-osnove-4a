#1.zadatak knjiga
class knjiga:
    def __init_(self,naslov,autor,godina_izdanja):
        self.naslov = naslov
        self.autor = autor
        self.godina_izdanja = godina_izdanja

knjiga1 = knjiga('Hamlet','William Shakespeare', 1603)
knjiga2 = knjiga('Gospodar prstenova','J.R.R Tolkien', 1954)

print(f'Naslov: {knjiga1.naslov}, Autor: {knjiga1.autor}, Godina izdavanja: {knjiga1.godinaizdanja}')
print(f'Naslov: {knjiga2.naslov}, Autor: {knjiga2.autor}, Godina izdavanja: {knjiga2.godinaizdanja}')

