import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import xml.etree.ElementTree as ET

class Medij:
    def __init__(self, naziv, godina, zanr, ocjena, status, putanja):
        self.naziv = naziv
        self.godina = godina
        self.zanr = zanr
        self.ocjena = ocjena
        self.status = status
        self.putanja = putanja
    def to_xml(self, parent):
        """Uzmimo sve podatke iz ovog objekta i zapišimo ih u XML datoteku kako bismo ih mogli kasnije opet učitati """
        elem = ET.SubElement(parent, self.__class__.__name__)
        for key, value in vars(self).items():
            child = ET.SubElement(elem, key)
            child.text = str(value)
        return elem
class Film(Medij):
    def __init__(self, naziv, godina, zanr, redatelj, ocjena, status, putanja):
        super().__init__(naziv, godina, zanr, ocjena, status, putanja)
        self.redatelj = redatelj

    def to_xml(self, parent):
        elem = super().to_xml(parent)
        ET.SubElement(elem, "redatelj").text = self.redatelj
        return elem

class Album(Medij):
    def __init__(self, naziv, godina, zanr, izvodac, ocjena, status, putanja):
        super().__init__(naziv, godina, zanr, ocjena, status, putanja)
        self.izvodac = izvodac

    def to_xml(self, parent):
        elem = super().to_xml(parent)
        ET.SubElement(elem, "izvodac").text = self.izvodac
        return elem
    
class MediaShelfApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MediaShelf - Katalog medija")
        self.geometry("900x600")
        self.configure(bg="#89CFF0")

        self.mediji = []

        self._kreiraj_menu()
        self._kreiraj_gui()
        self.ucitaj_xml()        