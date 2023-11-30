import haravasto
import random
import datetime


NAPPI_LEVEYS = 40
NAPPI_KORKEUS = 40

tilasto = []

tila = {
    "kentta": [],
    "nakyva_kentta": [],
    "leveys": 0,
    "korkeus": 0,
    "vuorot" : 0,
    "pelin_loppu": 0,
    "pelin_alku": 0
}
def tilaston_tallennus():
    """tässä tallennetaan pelin tiedot erilliseen tiedostoon"""
    try:
        with open("miinantallaajan_tilasto.txt", "a") as kohde:
            for peli in tilasto:
                kohde.write(peli +", ")
            kohde.write("\n")
    except IOError:
        print("Kohdetiedostoa ei voitu avata. Tallennus epäonnistui")
        
        
def tulosta_tilasto():
    """ tässä funktiossa tulostetaan käyttäjän halutessa tilasto. Tässä muotoillaan tilaston tulostus"""
    try:
        with open("miinantallaajan_tilasto.txt") as tiedosto:
            for i, rivi in enumerate(tiedosto):
                osat = rivi.split(",")
                pvm = osat[0]
                koko = osat[1]
                miinat = osat[2]
                tulos = osat[3]
                vuorot = osat[4]
                minuutit = osat[5]
                sekunnit = osat[6]
 
                print("{}.Peli: pvm: {}, kentan koko: {}, miinojen maara: {}, lopputulos: {}, vuorot: {}, kesto: {} min, {} s".
                    format(i+1, pvm, koko, miinat, tulos, vuorot, minuutit, sekunnit))
    except ValueError:
        print("Rivin tulostus ei onnistunut.")
    except FileNotFoundError:
        print("Tilastoa et voi nähdä ennen kuin olet pelannut edes kerran.")

def miinoita(kentta, jaljella, miinat):
    """Asettaa kentälle käyttäjän antaman määrän miinoja"""
    miinojen_maara = 0
    while miinojen_maara < miinat:
        i = random.randint(0, len(kentta) - 1)
        j = random.randint(0, len(kentta[1]) - 1)
        if (i, j) in jaljella:
            jaljella.remove((i, j))
            kentta[j][i] = "x"
            miinojen_maara += 1
        else:
            continue
            
def tayta_kentta(kentta,leveys, korkeus):
    """Täyttää kentän muut kohdat lähellä olevien miinojen mukaan"""
    for y in range(korkeus):
        for x in range(leveys):
            if kentta[y][x] == " ":
                kentta[y][x] = "0"
                laskuri = 0
                for i in range(y-1,y+2):
                    for j in range(x-1,x+2):
                        if i >= 0 and i < korkeus:
                            if j >= 0 and j < leveys:
                                if kentta[i][j] == "x":
                                    laskuri += 1
                                    kentta[y][x] = str(laskuri)
                                else:
                                    continue
            else:
                continue

def piirra_pelikentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for i, luku in enumerate(tila["nakyva_kentta"]):
        for j, merkki in enumerate(luku):
            haravasto.lisaa_piirrettava_ruutu(merkki, j*NAPPI_LEVEYS, i*NAPPI_KORKEUS)
    haravasto.piirra_ruudut()
 

def hiiri_kasittelija(x, y, nappi, muokkausnapit):
    """ 
    x ja y määrittävät klikkauksen sijainnin ruudulla ja nappi kertoo mitä nappia painettiin (saa
    arvoja HIIRI_VASEN, HIIRI_KESKI, HIIRI_OIKEA). Tässä funktiossa katsotaan mitä ruutua käyttäjä 
    on klikannut ja miten sen kanssa toimitaan.
    """
    x_indeksi = int(x / 40)
    y_indeksi = int(y / 40)
    if nappi == haravasto.HIIRI_OIKEA:
        tila["nakyva_kentta"][y_indeksi][x_indeksi] = "f"
        tila["vuorot"] += 1
        tarkista_kentta()
    elif nappi == haravasto.HIIRI_VASEN:
        if tila["kentta"][y_indeksi][x_indeksi] == "x":
            tila["vuorot"] += 1
            tila["pelin_loppu"] = datetime.datetime.now().replace(microsecond=0)
            tilasto.append("hävio")
            lopetus()
        else:
            if tila["nakyva_kentta"][y_indeksi][x_indeksi] == " ":
                tila["vuorot"] += 1
                if tila["kentta"][y_indeksi][x_indeksi] == "0":
                    tulvataytto(x_indeksi, y_indeksi)
                else:
                    tila["nakyva_kentta"][y_indeksi][x_indeksi] = tila["kentta"][y_indeksi][x_indeksi]
                    tarkista_kentta()
            elif tila["nakyva_kentta"][y_indeksi][x_indeksi] != "0" and tila["nakyva_kentta"][y_indeksi][x_indeksi] != "f":
                laske_miinat(x_indeksi, y_indeksi)
        
            
def tulvataytto(x, y):
        """tässä funktiossa täytetään kenttää, jos käyttäjä saa avata useamman ruudun kerralla"""
        tulvataytto = [(y, x)]
        while len(tulvataytto) > 0:
            y, x = tulvataytto.pop()
            tila["nakyva_kentta"][y][x] = tila["kentta"][y][x]
            for i in range(y-1, y+2):
                for j in range(x-1, x+2):
                    if i >= 0 and i < tila["korkeus"]:
                        if j >= 0 and j < tila["leveys"]:
                            if tila["kentta"][i][j] == "x":
                                continue
                            elif tila["kentta"][i][j] != "x":
                                if tila["nakyva_kentta"][i][j] == " ":
                                    if tila["kentta"][i][j] == "0":
                                        tulvataytto.append((i, j))
                                    else:
                                        tila["nakyva_kentta"][i][j] = tila["kentta"][i][j]
                                else:
                                    continue
        tarkista_kentta()                            
        
def laske_miinat(x,y):
    """tässä funktiossa tarkistetaan,jos henkilö on laittanut liput oikein laskemalla klikatun ruudun ympärillä miinat
    ja vertaamalla sitä täytettyyn kenttään.
    """
    laskuri = 0
    for i in range(y-1, y+2):
        for j in range(x-1, x+2):
            if i >= 0 and i < tila["korkeus"]:
                if j >= 0 and j < tila["leveys"]:
                    if tila["nakyva_kentta"][i][j] == "f":
                        if tila["kentta"][i][j] == "x":
                            laskuri += 1
                        else:
                            tila["pelin_loppu"] = datetime.datetime.now().replace(microsecond=0)
                            tilasto.append("häviö")
                            lopetus()                   
                    elif tila["nakyva_kentta"][i][j] == "x":
                        laskuri += 1
                    else:
                        continue
    if str(laskuri) == tila["kentta"][y][x]:
        tulvataytto(x, y)
                                    

def tarkista_kentta():
    """ Tarkistaa onko kenttä jo täysi ja erä siten voitettu """
    laskuri = 0
    for luku in tila["nakyva_kentta"]:
        for merkki in luku:
            if merkki == " ":
                laskuri += 1
                break
            else: 
                continue
    if laskuri == 0:
        tila["pelin_loppu"] = datetime.datetime.now().replace(microsecond=0)
        tilasto.append("voitto")
        lopetus()
        
def lopetus():
    """tässä funktiossa tehdään lopetustoimenpiteet"""
    kesto = int((tila["pelin_loppu"] - tila["pelin_alku"]).total_seconds())
    if kesto >= 60:
        minuutit = kesto // 60
        sekunnit = kesto % 60
    else: 
        minuutit = 0
        sekunnit = kesto
    tilasto.append(str(tila["vuorot"]))
    tilasto.append(str(minuutit))
    tilasto.append(str(sekunnit))
    tilaston_tallennus()
    haravasto.lopeta()


def main():
    """
    Lataa pelin grafiikat, luo peli-ikkunan, asettaa siihen piirtokäsittelijän ja aloittaa pelin.
    """
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(tila["leveys"] * NAPPI_LEVEYS, tila["korkeus"] * NAPPI_KORKEUS)
    haravasto.aseta_piirto_kasittelija(piirra_pelikentta)
    pelin_alku = []
    tila["pelin_alku"] = datetime.datetime.now().replace(microsecond=0)
    haravasto.aseta_hiiri_kasittelija(hiiri_kasittelija)
    haravasto.aloita()

    

if __name__ == "__main__":
    while True:
        print("Peli: Miinaharava")
        valinta = input("Valitse tehtävä, (U)uusi peli, (T)katso tilasto tai (L)lopeta: ")
        if valinta.lower() == "l":
            print("Kiitos ja tervetuloa uudelleen")
            break
        elif valinta.lower() == "t":
            tulosta_tilasto()
        elif valinta.lower() == "u":
            print("Valitse kentän koko ja miinojen määrä:")
            while True:
                try:
                    leveys = int(input("Anna kentän leveys: "))
                except ValueError:
                    print("Et antanut lukua")
                else:
                    if leveys > 0:
                        break
                    else:
                        print("leveyden on oltava vähintään yksi")
                        continue
            while True:
                try:
                    korkeus = int(input("Anna kentän korkeus: "))
                except ValueError:
                    print("Et antanut lukua")
                else:
                    if korkeus > 0:
                        break
                    else:
                        print("korkeuden on oltava vähintään yksi")
                        continue
            while True:
                try:
                    miinat = int(input("Anna miinojen määrä: "))
                except ValueError:
                    print("Et antanut lukua")
                else:
                    if miinat > 0 and miinat < leveys * korkeus:
                        break
                    else:
                        print("miinoja on oltava vähintään yksi, mutta maksimissaan yksi per ruutu")
                        continue
            kentta = []
            tilasto = []
            nakyva_kentta = []
            tila["leveys"] = leveys
            tila["korkeus"] = korkeus
            tilasto.append(str(datetime.datetime.now().replace(microsecond=0)))
            tilasto.append(str(leveys*korkeus))
            tilasto.append(str(miinat))
            for rivi in range(korkeus):
                kentta.append([])
                for sarake in range(leveys):
                    kentta[-1].append(" ")
            tila["kentta"] = kentta
                
            for rivi in range(korkeus):
                nakyva_kentta.append([])
                for sarake in range(leveys):
                    nakyva_kentta[-1].append(" ")
            tila["nakyva_kentta"] = nakyva_kentta
                

            jaljella = []
            for x in range(leveys):
                for y in range(korkeus):
                    jaljella.append((x, y))
            miinoita(kentta, jaljella, miinat)
            tayta_kentta(kentta, leveys, korkeus)
            main()
        else:
            print("Väärä valinta, valitse u, t tai l")