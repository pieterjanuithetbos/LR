# Vastleggen van intervallen met steeds stijgende LR

## Doel van het programma
Voor een grafiek van de sensitiveit in functie van de specificiteit (ook wel ROC curve), valt de LR interpreteren als een richtingsafgeleide. Voor een 'perfecte' ROC curve is de richtingsafgeleide steeds dalend. 

De bedoeling van dit programmaatje is om een selectie te maken uit de meetdata, zodat de **LR** (richtingsafgeleide) voor de weerhouden intervallen **steeds daalt**. 

De implementatie zal de data echter '**achterstevoren**' lezen en een steeds stijgende LR zoeken. Zo vermijden we dat negatieve LR's ook toegelaten worden.


## Randvoorwaarden

Er zijn enkele essentiële randvoorwaarden:
- In elke verdeling komt de het **eerste én laatste element** van de meetdata voor,
- de maximaal onderzochte **breedte** van intervallen is **geplafonneerd**,
- '**fijnste** verdeling' is hier geïnterpreteerd als 'verdeling met het **grootste aantal intervallen**'.
- het programmaatje past een **backtracking**-algoritme toe. Dat betekent: **exponentiële tijdscomplexiteit**.
- het is **niet** noodzakelijk zo dat de gevonden verdeling **gelijkmatig** verspreid is.

### invoerdata:

1. specificiteit (FPR),
2. sensitiviteit (TPR) en de
3. gekoppelde thresholds
4. totaal aantal besmette en niet-besmette patiënten



## Opbouw van de code
### Voorbereidend werk

+ `indexmachine`

De indexmachine krijgt als parameter een lijst mee en geeft een even lange lijst terug. Elk element van de lijst correspondeert met de index van het laatst voorgekomen unieke element in de opgegeven lijst. 

De gemaakte selectie is *niet uniek*. Wanneer een element bv. vier keer na elkaar voorkomt, zal de indexmachine de index van het eerste voorkomen vier keer weergeven.

+ `kies_indices`
  
  `kies_indices` gaat aan de slag met de uitvoer van de `indexmachine`. Hij vergelijkt de indexlijsten van de sensitiviteit en de specificiteit en geeft een nieuwe lijst terug met de 'overlap'. In de nieuwe lijst, komen *enkel* unieke elementen voor.

+ `trim`

Deze functie krijgt als invoer twee lijsten: een invoerlijst en een lijst met zinvolle indices. De uitvoer is een verkorte versie van de invoerlijst, die enkel de elementen op de opgegeven indices weerhoudt.

## Backtracking
+ extend

Breidt de partiële oplossing uit tot nieuwe oplossingen, maar stelt nooit intervallen voor die groter zijn dan de ingestelde maximale breedte.
  
+ examine

  Geeft aan dat de oplossing volledig is wanneer de laatste index in de partiële oplossing gelijk is aan het laatste datapunt. Zowel het eerste als het laatste datapunt moeten dus in de oplossing zitten, wat een belangrijke beperking is!
  
+ solve

  Onderzoekt alle mogelijke oplossingen en selecteert degene met het grootst aantal intervallen. Een 'fijne' verdeling interpreteren we hier dus als een verdeling met zo veel mogelijk intervallen.

## Likelihood berekenen

+ `likelihood_helper`

  Gegeven de sensitiviteit en de specificiteit, samen met een startindex en een eindindex, berekent `likelihood_helper` de de richtingsafgeleide over het interval bepaald door de start- en eindindex.

+ `bereken_likelihood`

Deze functie berekent de LR tussen de gevonden intervallen en geeft ze terug in lijstvorm, in de volgorde waarin de intervallen voorkomen.

Verder geeft het programma een lijst met de thresholds die overeenkomen met de indices die de gevonden intervallen definiëren. De lijst met thresholds telt dus één element meer dan de lijst met LR's.
