# VZDIALENOSTI KU KONTAJNEROM by dancejod

Program vezme dva vstupne subory s mnozinami bodov adries a kontajnerov a vypocita z nich zvolene statistiky – priemernu dlzku vchodov od kontajnerov, median, priemernu vzdialenost.

Pracuje so suradnicami v S-JTSK, vstupne data automaticky prevadza do tohto systemu.

Vystupom je subor obsahujuci adresy, ku ktorym je priradene ID najblizsieho kontajnera.

## UZIVATELSKA DOKUMENTACIA
### VSTUP

Do programu vstupuju dva subory, ktore musia byt vo formate GEOJSON. Prvy subor s nazvom *adresy.geojson* bude obsahovat mnozinu uvazovanych adries. Druhy subor s nazvom *kontejnery.geojson* bude obsahovat mnozinu uvazovanych kontajnerov.

Oba vstupy su ostetrene takto: ak vstupny subor neexistuje, nie je precitatelny, nie je pristupny programu, nie je validny GEOJSON alebo nastane nepredvidatelna vynimka, chod programu sa ukonci a nebude pokracovat vo vypoctoch. Ak vstupy prejdu cez tieto vynimky, vypocty prebehnu; chod programu sa vsak ukonci, ak vo vstupoch budu chybat potrebne atributy.

Program postupne bude prechadzat kazdu adresu. V ramci kazdej adresy sa prechadzaju vsetky kontajnery. Najprv sa suradnice adries transformuju do systemu S-JTSK. Potom sa zisti, ci je prave prechadzany kontajner verejny alebo pristupny iba obyvatelom domu – ak je verejny, pomocou Pytagorovej vety vypocita jeho vzdialenost od vchodu. Pracuje sa tu s pomocnou premennou, do ktorej sa priebezne budu tieto vzdialenosti ukladat. Ak sa najde kontajner s mensou vzdialenostou, ako predosly kontajner, pomocna premenna sa aktualizuje s novou vzdialenostou a zaroven sa zaznamena ID noveho najblizsieho kontajnera.

Po tom, co sa prejdu vsetky kontajnery pre aktualne iterovanu adresu, zisti sa, ci je vypocitana vzdialenost mensia ako 10 km. Ak je vacsia, program na to upozorni.

Nasledne sa k aktualne iterovanej adrese pripisu dva kluce: jeden obsahuje hodnotu najblizsej vzdialenosti ku kontajneru, druhy obsahuje ID najblizsieho kontajnera. Takto upravena adresa sa vlozi do zoznamu, ktory sa po iterovani vsetkych adries dumpne do vystupu.

### VYSTUP

Vystupom programu je subor *adresy_kontejnery.geojson*, ktory obsahuje vsetky adresy zo vstupneho subory *adresy.geojson* doplnene o ID najblizsieho kontajneru a jeho vzdialenost od vchodu.