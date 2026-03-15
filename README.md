# Picture-viewer teljesítményteszt és skálázódás

## Megvalósítás
### Skálázódás
Az automatikus skálázódás megvalósításához a Heroku beépített funkciói mellett a Hirefire szolgáltatást alkalmaztam. 
Ez az eszköz zökkenőmentesen integrálódik a Herokuval: folyamatosan monitorozza az alkalmazáshoz beérkező HTTP kérések számát, 
és amint a terhelés elér egy előre definiált küszöbértéket, automatikusan felskálázza a rendszert.

A skálázási folyamat az alábbi képen látható:
![](report/scaling.png)
### Terhelés szimuláció
A terhelés szimulálásához a Python-alapú Locust keretrendszert használtam. A teszteseteket a [locustfile.py](locustfile.py) fájlban definiáltam, amely a következő lépéseket tartalmazza:

1. Felhasználói bejelentkezés.
2. Fényképek listázása és lekérése.
3. Új fénykép feltöltése.
4. A feltöltött fénykép törlése.

A tesztkörnyezet futtatásához a Locust futtatásához szükséges kódot is a Heroku platformra telepítettem, és a terheléses tesztet ebből a környezetből indítottam el. 

**A teszt lefolyása:**
A szimuláció kezdetben 1 egyidejű felhasználóval indult, majd a terhelés fokozatosan 15 felhasználóig növekedett, végül pedig visszacsökkent az eredeti állapotra (1 felhasználó). A megnövekedett forgalom hatására a rendszer automatikusan 2 Dynóra (podra) skálázta fel az alkalmazást, majd a terhelés enyhülésével sikeresen visszaskálázta 1 Dynóra.

A futás részletes eredményei megtekinthetők a [Locust-report.html](report/Locust-report.html) jelentésben.