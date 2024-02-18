import datetime
import os
import threading
import platform
import time

Vrijeme = datetime.datetime.now()  # vrijeme
import signal


# funkcije
def Poruka():
    """Funkcija sluzi za ispis pozdravne poruke, trenutnog datuma i vrijeme oblika Sat%Minute%Sekunde DanUTjednu Dan-Mjesec-Godina,
        verziju interpretora programskog jezika Python, te naziv operacijskog sustava i prijavljenog korisnika"""

    print("Dobrodošli u Osnovnu komandnu liniju,(",
          (Vrijeme.strftime("%H:%M:%S %A %d-%m-%Y")), ")\nTrenutna verzija python interpretora je:",
          platform.python_version(), "\nNaziv operacijskig sustava:", platform.uname()[0], "\nTrenutni korisnik:",
          os.getlogin())


def Brisanje():
    """"Funkcija se pokrece kao stavka izbornika 2, od korisnika traži unos apsolutne/relativne adrese"""
    """"Nakon unosa adrese, vrsi se provjera tocnosti adrese te postoji li uopce unesena adresa, te se nakon pozitivne provjere vrsi brisanje objekta ako je to moguce
        (direktorij je prazan), nakon brisanja ispisuje se ime i sadrzaj direktorija nadredjenog obrisanog objekta"""

    Adresa = input("Unesite Adresu koju zelite obrisati")       #Unos adrese
    home = (os.path.expanduser("~"))
    Nadredena = os.path.dirname(Adresa)        #Adresa nadredjenog direktorija

    if os.path.exists(Adresa):      #Provjera validacije adrese
        velicina = os.path.getsize(Adresa)

        try:
            os.remove(Adresa)                       #Ako je to moguce, obrisi objekt
            print("Nadređeni direktori", Nadredena, ":\n", os.listdir(Nadredena))       #Izlistaj nadredjeni direktorij
            print("Velicina obrisanog objekta je", velicina, "b")           #Ispis velicine obrisanoga objekta

        except OSError as error:
            try:
                os.rmdir(Adresa)        #Ako je objekt direktorij, te je prazan, slijedi brisanje istoga
                print("Velicina praznog direktorija je 0")          #Velicina obrisanoga direktorija
                print("Nadređeni direktori", Nadredena, ":\n", os.listdir(Nadredena))           #Ispis sadrzaja nadredjenog direktorija

            except OSError as error:
                print("Direktoriji nije prazan, pa se neće izbrisati")      #Ako je objekt u pitanju direktorij, te nije prazan, brisanje nije moguce
    else:
        print("Direktoriji ne postoji")     #Ako upisani objekt/direktorij ne postoji, slijedi ispis prikladne poruke



def handler(signum, frame):

    print("prekinuto")
    raise prekid()


def prekid():
    pass


def syst():

    komanda = input("Upišite naredbu sustava")
    a = (((os.system(komanda))))
    signal.alarm(0)
    time.sleep(2)

def upravljac(a, b):
    """Funkcija jest dio 3. zadatka, te se koristi kao alat za dohvat PPID-a i PID-a procesa, te se rezultat ispisuje u txt datoteku."""

    print("zaprimljen je signal", signal.getsignal(a))
    home = (os.path.expanduser("~"))
    file = open("/" + home + "/stogprocesa.txt", "w")           #Otvaranje .txt datoteke za ispis
    os.getpid()
    file.write("Stanje stoga: " + str(b)+"\nPid procesa je:"+str(os.getpid())+"\nPPid procesa je:"+str(os.getppid()))         #U datoteku se upisuju stanje stoga, PPID-a i PID-a procesa
    file.close()    #Zatvaranje datoteke
    return


def Procesi():
    """Funkcija sluzi za unos broja signala, s kojim se izvodi daljne izvrsavanje. Ukoliko jest broj unesenog signala izmedju 10-20, isti se ignoriraju, ako je broj
       signala veći od 31 javlja se poruka o pogresnom unosu. Za signale pod brojem 1 ili 10, slijedi ispis stanje stoga PPID i PID procesa, te ispis trenutnog stanja stoga
       u stogprocesa.txt"""

    print("Unesite broj signala")
    n = int(input())
    Pid = os.getpid()                       #Dohvat PID-a procesa
    if n > 31:
        n = int(input("Neispravan unos, pokusajte ponovo: "))       #Provjera unosa n>31

    elif (n > 10 and n < 20):
        signal.signal(n, signal.SIG_IGN)
        print("Procesi od 10-20 su \"ignorirani\"")             #Provjera unosa broja signala  n>10 and n<20

    elif (n == 1 or n == 10):
        signal.signal(n, upravljac)                     #Za signale 1 ili 10 javlja se funkcija "upravljac"

    else:
        signal.signal(n, signal.SIG_DFL)            #Za sve ostale signale, vrsi se normalna zadaca

    os.kill(Pid, n)


listaParnih = []                                #Lista u koju se upisuju elementi
Povecanje15 = open("Povecanje15.txt", "w")      #Datoteka za ispis liste
lockCetv = threading.Lock()                     #Lokot
Brojac = 0

def Zadatak4():
    """Funkcija sluzi za unos broja veceg od 2 900 000, nakon cega se pokrecu dvije dretve. Prva dretva radi listu samo parnih brojeva iz intervala od 0 do unesenoga broja,
       a druga dretva uzima tu listu, svaki element liste uvecava za 1/5 te rezultat ispisuje u povecanje15.txt"""

    global Brojac
    n = int(input("Unesite n (>2900000)"))
    while n < 2900001:
        n = int(input("Neispravan unos pokusajte ponovno"))

    Prva = threading.Thread(target=Parni, args=(n,))                                                #Definiramo prvu dretvu te u njoj pozivamo funkciju "Parni"
    Druga = threading.Thread(target=Pomnozeni, args=(int(n / 2),threading.get_native_id()))         #Definiramo drugu dretvu te u njoj pozivamo funkciju "Pomnozeni"

    Prva.start()            #Pokrecemo prvu dretvu
    Druga.start()           #Pokrecemo drugu dretvu

    Prva.join()             #Dretve se spajaju sa glavnom
    Druga.join()

def Parni(n):
    """Funkcija upisuje sve parne brojeve izmedju 0 i unesenog broja u listu"""

    global Brojac
    lockCetv.acquire()

    for i in range(2, n + 1, 2):
        listaParnih.insert(Brojac, i)           #Upisivanje parnih brojeva u listu
        Brojac += 1

    lockCetv.release()


def Pomnozeni(Brojacc,id):
    """Funkcija sluzi za uvecanje svih elemenata liste za 1/5 te se rezultat liste ispisuje u datoteku povecanje15.txt. Na kraju, dretva koja je izradila listu, ispisuje poruku."""

    for g in range(0, int(Brojacc), 1):                             #Od nula do zadnjeg elementa liste
        Povecanje15.write(str(listaParnih[g] * 1.2) + "\n")         #Ispis mnozenja elemenata liste u .txt datoteku
    print(id,": posao je izvrsen")                                  #Poruka dretve



VelikBroj = 43430430430430430430

def Zadatak5():
    """Zadatak ove funkcije jest, nakon unosa broja izmedju 10 i 130 000, od broja 43430430430430430430 oduzimaju se kubovi brojevima u rasponu od 1 do unesene vrijednosti."""

    global VelikBroj
    n = int(input("Unesite n (10<n<130000)"))                                                       #Unos vrijednosti
    while (n < 9 and n > 130000):
        n = int(input("Neispravan unos pokusajte ponovno"))                                         #Provjera krive vrijednosti
    Podjela = n // 3                                                                                #Bitno za rasporedjivanje rada dretvi

    Dretva1 = threading.Thread(target=Oduzimakubove, args=(1, 1, Podjela))                          #Dretva 1 izvrsava funkciju "Oduzimakubove"
    Dretva2 = threading.Thread(target=Oduzimakubove, args=(2, Podjela, 2 * Podjela))                #Dretva 2 izvrsava funkciju "Oduzimakubove"
    Dretva3 = threading.Thread(target=Oduzimakubove, args=(3, 2 * Podjela, n))                      #Dretva 3 izvrsava funkciju "Oduzimakubove"


    Dretva1.start()
    Dretva2.start()
    Dretva3.start()

    Dretva1.join()
    Dretva2.join()
    Dretva3.join()

def Oduzimakubove(id, pocetak, n):
    """Funkciji su potrebni id druge dretve za ispis rezultata njezinog djelovanja, te pocetak i n kao interval brojeva za oduzimanje"""

    global VelikBroj
    i = pocetak
    for i in range(pocetak, n, 1):
        VelikBroj -= (i ** 3)                           #Od velikoga broja oduzima se kub svakog broja od intervala [pocetak , n]
    if(id==2):
        print(VelikBroj)                                #Pomocu id dretve, ispisuje se rezultat njezinog oduzimanja




def umnozak(pocetak, n):
    """Funkcija prima argumente pocetak i n kao granice intervala iz koje dretve izvlace proste brojeve."""
    global umn
    global ProstiBrojevi
    for num in range(pocetak, n):           #Od intervala [pocetak - n]
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:          #Nije prosti broj
                    break
                else:
                    ProstiBrojevi.append(num)       #Nasli smo prosti broj, isti se upisuje u listu
                    umn *= num                      #Varijabla umnozak se mnozi sa svakim nadjenim prostim brojem
                    break


def Zadatak6():
    """Funkcija za 6. zadatak seminara sluzi za pozivanje dretvi na rad, koje same pozivanju funkciju umnozak koja sluzi za izracun faktorijela
        svih prostih brojeva iz intervala [0 - 500 000]"""

    Dretva1 = threading.Thread(target=umnozak, args=(1, 125000))                #Dretva 1 izvodi funkciju od 1 - 125 000
    Dretva2 = threading.Thread(target=umnozak, args=(125000, 250000))           #Dretva 2 izvodi funkciju od 125 000 - 250 000
    Dretva3 = threading.Thread(target=umnozak, args=(250000, 375000))           #Dretva 3 izvodi funkciju od 250 000 - 375 000
    Dretva4 = threading.Thread(target=umnozak, args=(375000, 500000))           #Dretva 4 izvodi funkciju od 375 000 - 500 000

    Dretva1.start()
    Dretva2.start()
    Dretva3.start()
    Dretva4.start()

    Dretva1.join()
    Dretva2.join()
    Dretva3.join()
    Dretva4.join()

    global ProstiBrojevi
    global umn
    print("Prosti brojevi su", ProstiBrojevi, "\nNjihov umnožak je:", umn)      #Ispis svih prostih brojeva u intervalu [0 - 500 000], te ispis ukupnog umnoska



Poruka()            #Poziv funkcije poruka

provjera = "pokreni"
while 1:
    print(
        "1 - Pokreni bash naredbu\n2 - Izbriši datoteku il direktoriji""\n3 - Pošalji signal interpreteru\n4 - Uvećani parni brojevi pomoću dretve"
        "\n5 - oduzimanje kubova \n6 - prosti brojevi i njihov umnožak\nZa izlaz upisite exit ili logout ili out")
    provjera = input("Odaberite opciju")

    if (provjera == "2"):
        a = Brisanje()

    elif (provjera == "1"):
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(18)
        try:
            syst()
        except:
            prekid()

    elif (provjera == "3"):
        Procesi()

    elif (provjera == "4"):
        Zadatak4()

    elif (provjera == "5"):
        Zadatak5()

    elif (provjera == "6"):
        umn = 1
        ProstiBrojevi = []
        Zadatak6()

    elif (provjera == "exit" or provjera == "logout" or provjera == "out" or provjera == "end"):
        break

    elif (provjera == ""):
        pass

    else:
        print("Nepostojeća Naredba(error 17)\n")
