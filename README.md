# LR

De belangrijke stappen zijn:
1. maak een selectie van weetdata volgens dit selectiecriterium: enkel koppels meetdata die voor het eerst voorkomen in de lijst, blijven behouden.
De methode die kies_functie gebruikt is de volgende: ...
voordelen:
  - ...
nadelen:
  - ...

3. vind de verdeling met het grootst aantal intervallen, zodat de gemiddelde LR binnen het interval steeds kleiner is dan die in het vorige interval
Code voor dit deel vind je in kleinste_interval_backtracking. Het idee het volgende: controleer alle mogelijke intervallen binnen de getrimde lijst waarvoor de LR daalt, en kies de verdeling het met meeste intervallen.

voordelen:
  - alle verdelingen worden overlopen
  - 
nadelen:
  - duurt lang,
  - de verdeling is niet noodzakelijk gelijk verdeeld.

5. schrijf de gevonden resultaten naar excel in to_excel.

ZIE AFZONDERLIJKE FUNCTIES VOOR MEER UITLEG
