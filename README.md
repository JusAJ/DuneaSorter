# DuneaSorter

Onderstaande legt uit hoe je het script kan gebruiken. Lees dit goed door!

## Is Python geïnstalleerd?

Eerst is het belangrijk om te weten of Python is geïnstalleerd. Dat doe je op de volgende manier:

- Open een Powershell venster
- Type het volgende in: `python3 --version` en druk op de Enter-toets
- Als Python geïnstalleerd is, is het resultaat in de vorm van: `Python 3.13.5`. Dan kan je het script gebruiken.
- Als Python _niet_ geïnstalleerd is, wordt dat ook getoond. Installeer Python, en probeer bovenstaande opnieuw.

## Gebruik van het script

Eerst moet je het script downloaden en ergens opslaan waar je het makkelijk terug kan vinden. [HIER](https://github.com/JusAJ/DuneaSorter/releases) kan je alle releases vinden. Download altijd de nieuwste.

Om het script te starten voer je het volgende commando uit: `python3 <locatie waar script staat>\sorting.py`.
- Bijvoorbeeld: `python3 C:\Scripts\sorting.py`

Vervolgens wordt om de locatie gevraagd waar het .csv bestand staat wat verwerkt moet worden. Dat kan bijvoorbeeld zijn: `C:\Scripts\hetbestand.csv`. Als je dan op de Enter-toets drukt, wordt het script uitgevoerd. Het resultaat wordt op dezelfde locatie neergezet als het bestand wat verwerkt is.

**! Let op: het resultaat heet altijd `output.csv` !**

Dit betekent dat als je het script 2x achter elkaar uitvoert, de output van de 2e keer de output van de eerste keer overschrijft.