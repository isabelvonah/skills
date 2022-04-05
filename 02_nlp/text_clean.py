# scheint nicht zu funktionieren sieht Datei nicht
"""
def text_einlesen():
    with open("stopwords_german.txt", "r") as open_file:
        inhalt = open_file.read()
    return inhalt
"""

# Testtext um Funktionen zu Testen
bsp = "Bei uns arbeiten Diese Aufgabe bietet Ihnen ein spannendes und vielseitiges Betätigungsfeld, welches Platz für eigenen Gestaltungsspielraum, Eigeninitiative sowie die fachliche Weiterentwicklung lässt. Auf Sie wartet ein aufgestelltes und motiviertes Team. Zusammen leben Sie eine kommunikative, lösungsorientierte und selbständige Arbeitsweise."

def umlaute(texte):
    texte_uml = texte.replace("ü","ue").replace("ä","ae").replace("ö","oe")
    return texte_uml

def zeichenentfernen(texte):
    specialChars = "!#$%^&*()" 
    for specialChar in specialChars:
        texte_char = texte.replace(specialChar, '')
    texte_char = texte.replace(',', ' ').replace('.',' ')
    return texte_char

def normalisieren(texte):
    texte_klein = texte.lower()
    return texte_klein
   
def aufsplitten(texte):
    texte_aufgesplittet_oder_genau = texte.split()
    return texte_aufgesplittet_oder_genau


# texte = text_einlesen()
uml = umlaute(bsp)
symb = zeichenentfernen(uml)
norm = normalisieren(symb)
split = aufsplitten(norm)
print(split)
