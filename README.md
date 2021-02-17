# SimulacijaGravitacije
Simulacija gravitacije pri predmetu računalništvo.

Opis:
Program Simulira vpliv gravitacije med objekti v 2D prostoru. Za računanje sil med delci sem uporabil Barnes-Hutov algoritem.
Kako deluje.

Za delovanje so potrebne 3 datoteke Gravitacija.py, Kontrolna_plošča.py in tekstovni fajl info.txt. 
poženete program kontrolna plošča, v komandni vrstici se pokaže vprašanje: Naključna razporeditev(y/n)?
če odgovorite:
- y, je potrebno vpisati še število delcev, ki jih želite simulirati. 
- n, je potrebno vpisati ime vaše datoteke, v kateri so shranjeni podatki o začnem stanju sistema
    Datoteka mora imeti obliko:

    masa,x_coord,y_coord,hitrost,kot/pi

    v vsaki vrstici naj bodo podatki za en delec

Pojavi se vam zaslon z nepremičnimi delci z naključno maso in hitrostjo nič.
s tipkami l, m, v nadzorujete lokacijo, maso in hitrost. uporabljate lahko le eno od teh treh funkcij naenkrat
    S pritiskom na:
    l - s klikom na delec določate njegovo lokacijo
    m - s klikom na delec določate njegovo maso/velikost
    v - s klikom na delec določate vektor hitrosti, ki je prikazan z zeleno puščico
    d - prikažete/ugasnete informacije o objektu
    s - shranite trenutno stanje v datoteko z imenom saved.txt
    r - nazaj v začetno stanje
    s pritiskom na tipko space poženete/ustavite simulacijo
s tipkami + in - in puščicami lahko zaslon približate/oddaljite in spreminjate perspektivo, z miško lahko premikate objekte tudi med simulacijo. 
v spodnjem levem kotu s potegom kvadrata po premici spreminjate vrednost gravitacijeske konstante G.


Datoteka mora imeti obliko:

masa,x_coord,y_coord,hitrost,kot/pi

v vsaki vrstici naj bodo podatki za en delec
brez prazne vrstice na koncu



viri:
https://mikegrudic.wordpress.com/2017/07/11/a-simple-and-pythonic-barnes-hut-treecode/
http://arborjs.org/docs/barnes-hut
https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/
https://www.youtube.com/channel/UCfzlCWGWYyIQ0aLC5w48gBQ




