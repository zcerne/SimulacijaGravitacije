# SimulacijaGravitacije
Simulacija gravitacije pri predmetu računalništvo.

Opis:
Program Simulira vpliv gravitacije med objekti v 2D prostoru. Za računanje sil med delci sem uporabil Barnes-Hutov algoritem.
Kako deluje.

Za delovanje so potrebne 3 datoteke Gravitacija.py, Kontrolna_plošča.py in tekstovni fajl info.txt. 
poženete program kontrolna plošča in odpre se okno z dvema možnostnima. Naključna razporeditev "y" ali datoteka "n"
- y, vpišite število delcev, ki jih želite simulirati in pritisnite enter. 
- n, vpišite ime vaše datoteke, v kateri so shranjeni podatki o začetnem stanju sistema
    Datoteka mora imeti obliko:

    masa,x_coord,y_coord,hitrost,kot/pi

    v vsaki vrstici naj bodo podatki za en delec

Pojavi se vam zaslon z nepremičnimi delci z naključno maso in hitrostjo nič.
s tipkami "l", "m" in "v" nadzorujete lokacijo, maso in hitrost. Uporabljate lahko le eno od teh treh funkcij naenkrat
    S pritiskom na:
    l in s klikom na delec določate njegovo lokacijo
    m in s klikom na delec določate njegovo maso/velikost
    v in s klikom na delec določate vektor hitrosti, ki je prikazan z zeleno puščico
    d - prikažete/ugasnete informacije o objektu
    s - shranite trenutno stanje v datoteko z imenom saved.txt
    r - nazaj v začetno stanje
    s pritiskom na tipko space poženete/ustavite simulacijo
    Z miško lahko pritisnete na gumb za informacije in s klikom na gumb "back" greste nazaj na začetni zaslon.
s tipkami + in - in puščicami lahko zaslon približate/oddaljite in spreminjate perspektivo, z miško lahko premikate objekte tudi med simulacijo. 
v spodnjem levem kotu s potegom kvadrata po premici spreminjate vrednost gravitacijeske konstante G.


Datoteka mora imeti obliko:

masa,x_coord,y_coord,hitrost,kot/pi

v vsaki vrstici naj bodo podatki za en delec
brez prazne vrstice na koncu



viri:
Koda v mapi gravitacija ja v znatni meri kopirana iz spodnjih virov. 
https://mikegrudic.wordpress.com/2017/07/11/a-simple-and-pythonic-barnes-hut-treecode/ - koda uporabljena za Barnes-hut algoritem 
http://arborjs.org/docs/barnes-hut
https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/ - Koda uporabljena za nekatere funkcije.
https://www.youtube.com/channel/UCfzlCWGWYyIQ0aLC5w48gBQ




