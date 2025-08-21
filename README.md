# LR
Elk van de volgende drie functies correspondeert met een .py-file in deze repository.

1. kies_functie maakt een selectie van meetdata. De functie geeft een lijst terug van de indices die corresponderen met unieke koppels in de gegeven dataset.

  _nadeel_: de selectie is niet uniek. Er kunnen andere selecties bestaan met evenveel elementen, maar vermoedelijk niet met meer elementen (ik heb het nog niet sluitend kunnen aantonen).

2. kleinste_interval_backtracking vindt de verdeling met het grootst aantal intervallen, zodat de gemiddelde LR binnen het interval steeds kleiner is dan die in het vorige interval.
Controleer met brute kracht alle mogelijke intervallen binnen de getrimde lijst waarvoor de LR daalt, en kies de verdeling het met meeste intervallen. Gezien de exponentiële tijdscomplexiteit, zoekt het algoritme enkel naar intervallen die maximaal 7 indices groot zijn.

  _nadelen_:
  - duurt lang,
  - niet alle intervallen worden overlopen (max 7 breed).
  - de verdeling is niet noodzakelijk gelijk verdeeld.

3. schrijf de gevonden resultaten naar excel in to_excel.

zie afzonderlijke functies voor meer uitleg.
