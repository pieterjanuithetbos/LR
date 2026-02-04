# Vastleggen van intervallen met steeds stijgende LR

## Doel van het programma
De invoer is (i) specificiteit (FPR), (ii) sensitiviteit (TPR) en de (iii) gekoppelde thresholds. 

Voor een grafiek van de sensitiveit in functie van de specificiteit (ook wel ROC curve), valt de LR interpreteren als een **richtingsafgeleide**. Aangezien het moeilijk is om een continue fit te vinden voor de meetdata, kunnen we de richtingsafgeleide enkel benaderend berekenen als de gemiddelde richtingsafgeleide over een inverval. 

Voor een 'perfecte' ROC curve is de richtingsafgeleide steeds dalend. De bedoeling van dit programmaatje is om een selectie te maken uit de meetdata, zodat de LR (richtingsafgeleide) voor de weerhouden intervallen steeds daalt. 

De implementatie zal de data echter 'achterstevoren' lezen en een steeds stijgende LR zoeken. Zo vermijdt het dat negatieve LR's ook toegelaten worden.


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
