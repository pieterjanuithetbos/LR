# Vastleggen van intervallen met steeds stijgende LR
## Introductie

Onderstaand documentje biedt een kort overzicht van de werking van `main.py`.

## Doel van het programma
De invoer is (i) specificiteit (FPR), (ii) sensitiviteit (TPR) en de (iii) gekoppelde thresholds. 

Voor een grafiek van de sensitiveit in functie van de specificiteit (ook wel ROC curve), valt de LR interpreteren als een richtingsafgeleide. Aangezien het moeilijk is om een continue fit te vinden voor de meetdata, kunnen we de richtingsafgeleide enkel benaderend berekenen als de gemiddelde richtingsafgeleide over een inverval. 

Voor een 'perfecte' ROC curve is de richtingsafgeleide steeds dalend. De bedoeling van dit programmaatje is om een selectie te maken uit de meetdata, zodat de LR (richtingsafgeleide) voor de weerhouden intervallen steeds daalt.


## Randvoorwaarden

Er zijn enkele essentiële randvoorwaarden:
- In elke verdeling komt de het eerste én laatste element van de meetdata voor,
- de maximaal onderzochte breedte van intervallen is geplafonneerd: in sommige gevallen zijn ze hoogstens 8 breed, in andere hoogstens 11 (dat wil zeggen dat het eind punt maximaal 11 stapjes verwijderd is van het beginpunt).
- 'fijnste verdeling' is hier geïnterpreteerd als 'verdeling met het grootste aantal intervallen'.
- het programmaatje past het backtracking-algoritme toe, dat voor grote datasets extreem traag is. Dat is meteen de praktische verklaring voor de limiet op intervalbreedtes.
- het is niet noodzakelijk zo dat de gevonden verdeling gelijkmatig verspreid is.


## Opbouw van de code
### Voorbereidend werk

+ `indexmachine`

  De indexmachine krijgt als parameter een lijst mee en geeft een even lange lijst terug. De uitvoer bevat op elke positie de index van het laatst voorgekomen _unieke_ element op de corresponderende positie in de opgegeven lijst. 

  De gemaakte selectie is #highlight[niet uniek].

+ `kies_indices`
  
  `kies_indices` gaat aan de slag met de uitvoer van de `indexmachine`. Hij vergelijkt de indexlijsten van de sensitiviteit en de specificiteit en geeft een nieuwe lijst terug met de 'overlap'. In de nieuwe lijst, komen *enkel* unieke elementen voor.

+ `trim`

  Deze functie krijgt als invoer twee lijsten: een invoerlijst en een lijst met zinvolle indices. De uitvoer is een verkorte versie van de invoerlijst, die enkel de elementen op de opgegeven indices weerhoudt.

## Backtracking
+ extend

  Breidt de partiële oplossing uit tot nieuwe oplossingen, maar stelt nooit intervallen voor die groter zijn dan de ingestelde maximale breedte.
  
+ examine

  Geeft aan dat de oplossing volledig is wanneer de laatste index in de partiële oplossing gelijk is aan het laatste datapunt. Zowel het eerste als het laatste datapunt moeten dus in de oplossing zitten, wat een #underline[belangrijke beperking] is!
  
+ solve

  Onderzoekt alle mogelijke oplossingen en selecteert degene met het grootst aantal intervallen. Een 'fijne' verdeling interpreteren we hier dus als een verdeling met zo veel mogelijk intervallen.

## Likelihood berekenen

+ `likelihood_helper`

  Gegeven de sensitiviteit en de specificiteit, samen met een startindex en een eindindex, berekent `likelihood_helper` de de richtingsafgeleide over het interval bepaald door de start- en eindindex.

+ `bereken_likelihood` 

  Deze functie berekent de LR tussen de gevonden intervallen en geeft ze terug in lijstvorm, in de volgorde waarin de intervallen voorkomen.

Verder geeft het programma een lijst met de thresholds die overeenkomen met de indices die de gevonden intervallen definiëren. De lijst met thresholds telt dus #text(fill: red, [één element]) meer dan de lijst met LR's.
#pagebreak()

## Wat meer over de uitvoer
### Excel

Op het einde schrijft het programma volgende resultaten naar excel:
- tabblad 1: 
  de getrimde lijsten van 
  + sensitiviteit, 
  + specificiteit en 
  + thresholds.
- tabblad 2:
  + de indices die de intervallen definiëren,
  + de thresholds die de intervallen definiëren,
  + `inf`, gevolgd door de LR's tussen de intervallen (`inf` om ervoor te zorgen dat alle lijsten even lang zijn).

## Kanttekeningen

De inleiding vermeldt dat de het programmaatje een verdeling zoekt waarvoor de LR (richtingsafgeleide) steeds daalt. 'Maar wat als ze negatief wordt, en de ROC-curve begint te dalen?', zal de oplettende lezer zich afvragen. Toch is dat geen probleem.

De verklaring is dat de invoerlijsten de data weergeven van hoge naar lage threshold. Lage TPR- en FPR-waarden komen overeen met hoge thresholds en vice versa. Dus als je de grafiek van TPR in functie van FPR van hoge naar lage threshold wil lezen, moet je dat van rechts naar links doen. 

Het programmaatje krijgt de data 'achterstevoren' binnen en leest de data dus effectief van rechts naar links. Het zoekt een verdeling zodat de LR steeds groter wordt.

Een mogelijke manier om de uitvoer de visualiseren, is om de LR als functie van de threshold te plotten. We moeten ons ervan bewust zijn dat de thresholds dan wél van klein naar groot gaan. De curve van LR in functie van threshold is stijgend, niet dalend.



Elk van de volgende functies correspondeert met een .py-file in deze repository.

1. kies_functie maakt een selectie van meetdata. De functie geeft een lijst terug van de indices die corresponderen met unieke koppels in de gegeven dataset.

  _nadeel_: de selectie is niet uniek. Er kunnen andere selecties bestaan met evenveel elementen, maar vermoedelijk niet met meer elementen (dat heb ik nog niet sluitend kunnen aantonen).

2. kleinste_interval_backtracking vindt de verdeling met het grootst aantal intervallen, zodat de gemiddelde LR binnen het interval steeds kleiner is dan die in het vorige interval.
Controleert met brute kracht alle mogelijke intervallen binnen de getrimde lijst waarvoor de LR daalt, en kies de verdeling het met meeste intervallen. Gezien de exponentiële tijdscomplexiteit, zoekt het algoritme enkel naar intervallen die maximaal 7 indices groot zijn.

  _nadelen_:
  - duurt lang,
  - niet alle intervallen worden overlopen (max 7 breed),
  - de verdeling is niet noodzakelijk gelijk verdeeld.

Zie afzonderlijke functies voor meer uitleg.
