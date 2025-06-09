# Testovací sada pro Alza.cz s Playwrightem a Pytestem

*Note: English follows*

Sada automatizovaných testů pro web Alza.cz využívající Playwright k interakci s prohlížečem a Pytest jako testovací framework.

## Popis

Tato sada testů ověřuje klíčové funkcionality webu Alza.cz, jako je vyhledávání produktu, kontrola atributů obrázků a stahování souborů. Testy se spouštějí v různých prohlížečích (Chromium, Firefox, WebKit) a poskytují podrobné výpisy za účelem snadného ladění.
V případě, že test narazí na problém (např. prvek není v daném časovém limitu nalezen), automaticky se pořídí snímek obrazovky (screenshot) pro snazší identifikaci chyby. Tyto snímky se ukládají do kořenového adresáře projektu.

## Použité knihovny a verze Pythonu

Tento program vyžaduje **Python 3.10** a novější.

Knihovny nutné ke spuštění programu a testů jsou uvedeny v souboru `requirements.txt`.
K instalaci externích knihoven je vhodné použít virtuální prostředí.
Hlavní knihovny zahrnují `playwright` k automatizaci prohlížeče a `pytest` ke správě a spouštění testů.
Knihovny lze nainstalovat pomocí:
`pip install -r requirements.txt`

## Používání

### Testy (`test_alza.py`)

Testy se spouští pomocí Pytestu z kořenového adresáře projektu. Před spuštěním se ujistěte, že máte nainstalované všechny potřebné knihovny ze souboru `requirements.txt`.
Testy se parametrizují pro spuštění v prohlížečích Chromium, Firefox a WebKit.
Ve výchozím nastavení (viz `test_alza.py`) se testy spouštějí v "headed" režimu (s viditelným oknem prohlížeče) a malým zpomalením (`slow_mo=500`) pro lepší sledovatelnost. Tyto parametry lze upravit v kódu fixture `browser`.

**Poznámka k "headless" režimu:**

Na testy v "headless" režimu (nastavení `headless=True` ve fixture `browser`) web Alza.cz v některých prohlížečích (zejména Chromiu) reaguje detekcí robotů a testy tak nemusí projít. V "headed" režimu by testy měly projít vždy.


**Spuštění testů:**
`pytest` 
Po přidání `-s` se zobrazí výpisy (`print` statements) z testů přímo v terminálu, takže lze přímo sledovat průběh testů.

## Příklad fungování

### Testy

Ukázka výstupu Pytestu:
```
$ pytest
============================= test session starts ==============================
platform win32 -- Python 3.10.X, pytest-7.X.X, pluggy-1.X.X
rootdir: \cesta\k\projektu

collected 9 items
plugins: base-url-2.X.X, playwright-0.X.X
test_alza.py .........                                         [100%]

============================== 9 passed in X.XXs ===============================
```

## Autor
Štěpán Pala

# Test Suite for Alza.cz with Playwright and Pytest

## Description

This test suite verifies key functionalities of the Alza.cz website, such as product search, checking image attributes, and downloading files. The tests are run in different browsers (Chromium, Firefox, WebKit) and provide detailed logs for easy debugging.
If the test encounters a problem (e.g. an element is not found within the time limit), a screenshot is automatically taken to help identify the error. These screenshots are stored in the project root directory.

## Dependencies

This program requires **Python 3.10** or newer.

The packages necessary to run the program are specified in `requirements.txt`.  
Key libraries include `playwright` for browser automation and `pytest` for test management and execution.
A virtual environment is recommended to install external packages.
The dependencies can be installed as follows:
`pip install -r requirements.txt`

## Usage

### Tests (`test_alza.py`)

Tests are run using Pytest from the project's root directory. Before running, ensure you have installed all necessary libraries from `requirements.txt`.
Tests are parameterized to run in Chromium, Firefox, and WebKit browsers.
By default (see `test_alza.py`), tests run in "headed" mode (with a visible browser window) and a slight slowdown (`slow_mo=500`) for better traceability. These parameters can be adjusted in the `browser` fixture code.

**Note on "headless" mode:**

When running tests in "headless" mode (by setting `headless=True` in the `browser` fixture), the Alza.cz website may respond with bot detection in some browsers (especially Chromium), meaning some tests may not pass. In "headed" mode, tests should generally pass.

**Running tests:**
`pytest`
After adding `-s`, the `print` statements from the tests will be displayed directly in the terminal, allowing direct tracking of the test's progress.

## Example

### Tests

Pytest output example:
```
$ pytest
============================= test session starts ==============================
platform win32 -- Python 3.10.X, pytest-7.X.X, pluggy-1.X.X
rootdir: \path\to\project

collected 9 items
plugins: base-url-2.X.X, playwright-0.X.X
test_alza.py .........                                         [100%]

============================== 9 passed in X.XXs ===============================
```

## Author
Štěpán Pala
