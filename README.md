# SimulacijaGravitacije
Simulacija gravitacije pri predmetu računalništvo.

Opis:
Program Simulira vpliv gravitacije med objekti v 2D prostoru. Za računanje sil med delci sem uporabil Barnes-Hutov algoritem.
Kako deluje.

Za delovanje sta potrebni datoteki Gravitacija.py in Kontrolna_plošča.py. 
poženete program kontrolna plošča, v komandni vrstici se pokaže vprašanje: Naključna razporeditev(y/n)?
če odgovorite:
- y, je potrebno vpisati še število delcev, ki jih želite simulirati. Pojavi se vam zaslon z nepremičnimi delci z naključno maso in hitrostjo nič.
s tipkami l, m, v nadzorujete lokacijo, maso in hitrost. uporabljate lahko le eno od teh treh funkcij naenkrat
    S pritiskom na:
    l - s klikom na delec določate njegovo lokacijo
    m - s klikom na delec določate njegovo maso/velikost
    v - s klikom na delec določate vektor hitrosti 
    s pritiskom na tipko space poženete/ustavite simulacijo

- n, je potrebno vpisati ime vaše datoteke, v kateri so shranjeni podatki o začnem stanju sistema

Datoteka mora imeti obliko:

masa,x_coord,y_coord,hitrost,kot/pi

v vsaki vrstici naj bodo poodatki za en delec
brez prazne vrstice na koncu

s tipkami + in - in puščicami lahko zaslon približate/oddaljite in spreminjate perspektivo, z miško lahko premikate objekte tudi med simulacijo. 

viri:
https://mikegrudic.wordpress.com/2017/07/11/a-simple-and-pythonic-barnes-hut-treecode/
http://arborjs.org/docs/barnes-hut
https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/




