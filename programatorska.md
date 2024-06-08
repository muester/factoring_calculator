# Programátorská dokumentace

## (1.0) Popis programu a využité algoritmy

### Obecné informace

Myšlenka programu je umožnit provádět prvočíselný rozklad i u "o něco větších" čísel, než dovolují naivní algoritmy. Přesněji, program je schopný v poměrně svižném čase rozložit RSA čísla do 150 bitů, v čase řádově pomalejším RSA čísla až do 200 bitů.

Program se dělí na konzolovou a grafickou část, která by se z principu měla opírat o stejné funkce, čímž je zamezeno nekonzistentnímu chování.

### Využité algoritmy a datové struktury

Program nevyužívá žádné složité datové struktury, kromě případu Montgomeryho reprezentace bodu na eliptické křivce u algoritmu LECM.

Z algoritmů se program děli na dvě části, část ověřující prvočíselnost (Miller-Rabinův test, Lucasův test, BAILIE-PSW test) a část provádějící rozklad na prvočinitele (Trial division, pollard-rho, Lenstra elliptic-curve factorization method). Implementace těchto algoritmů je standardní odpovídající jejich teoretickému návrhu v pseudokodu, bez většího množství optimalizací.

Jednotlivé algoritmy se dělí na více funkcí, které by z principy měly vždy fungovat jako samostatné jednotky a měly by být konzistentní s jejich teoretickým návrhem, t.j formát výstupu by neměl být zbytečně modifikován uvnitř algoritmu.

## (1.1) Modul `main.py` a `graphical.py`

### `Obecný popis funkčnosti`

Tyto moduly zodpovídají za samotné volání funkcí a (grafickou) funkčnost programu.
Narozdíl od zbytku modulů, které spíše přípomínají "knihovnu" na rozklad celých čísel slouží tyto dva moduly k volání funkcí ze zbytku modulů na základě uživatelského vstupu.

Nutno poznamenat, že tyto moduly jsou IO blokující, což v případě grafického rozhraní způsobuje zamrznutí okna při vstupech nad schopnost kvality implementace knihovny pod povrchem.


## (1.2) Modul `primality.py`

### `trial_division(number: int, stop: int = None) -> bool`

#### Přehled funkce:

- Naivní algoritmus na testování prvočíselnosti
- Funkce přijímá jeden povinný a jeden nepovinný parametr
- Funkce vrací výsledek prvočíselného testu

#### Parametry:

1. `number` <-> číslo, které dělíme
2. `stop` <-> nejvyšší testovaný dělitel

#### Chování funkce:

- V případě že do zadaného počtu kroků nalezne funkce dělitele, je navrácena hodnota False
- V opačném případě je vrácena hodnota True

### `get_primes(count: int) -> list[int]`

#### Přehled funkce:

- Naivní algoritmus k získání n prvních prvočísel
- Funkce přijímá jeden povinný parametr
- Funkce vrací seznam prvních n prvočísel

#### Parametry:

1. `count` <-> žádaný počet prvočísel

#### Chování funkce:

- Funkce vrátí prvních n prvočísel

### `miller_rabin(subject: int, bases: int) -> bool`

#### Přehled funkce:

- Miller rabinův probabilistický test prvočíselnosti
- Funkce přijímá dva povinné parametry
- Funkce vrací výsledek prvočíselného testu

#### Parametry:

1. `subject` <-> číslo, jež testujeme
2. `bases` <-> počet vyzkoušených základů

#### Chování funkce:

- Pokud je číslo pravděpodobným prvočíslem - True
- V opačném případě je navrácena hodnota False

### `calc_jacobi(numerator: int, denominator: int) -> int`

#### Přehled funkce:

- Algoritmus na určení hodnot Jacobiho symbolů
- Funkce přijímá dva povinné parametry
- Funkce vrací výsledek prvočíselného testu

#### Parametry:

1. `numerator` <-> čitatel jacobiho symbolu
2. `denominator` <-> jmenoatel jacobiho symbolu

#### Chování funkce:

- Funkce vždy navrátí funkci zadaného jacobiho symbolu

### `lucas_test(subject: int) -> bool`

#### Přehled funkce:

- Lucasův probabilistický test prvočíselnosti
- Funkce přijímá jeden povinný parametr
- Funkce vrací výsledek prvočíselného testu

#### Parametry:

1. `numerator` <-> číslo, jež testujeme

#### Chování funkce:

- Pokud je číslo pravděpodobným prvočíslem - True
- V opačném případě je navrácena hodnota False

### `bailie_psw(subject: int) -> bool`

#### Přehled funkce:

- Bailie-PSW algoritmus na určení prvočíselnosti čísla
- Funkce přijímá jeden povinný parametr
- Funkce vrací výsledek prvočíselného testu

#### Parametry:

1. `numerator` <-> číslo, jež testujeme

#### Chování funkce:

- Pokud je číslo prvočíslem - True
- V opačném případě je navrácena hodnota False

## (1.3) Modul `factorization.py`

### `trial_division(number: int, stop: int = None) -> bool`

#### Přehled funkce:

- Algoritmus postupného dělení k nalezení prvočíselného dělitele
- Funkce přijímá jeden povinný a jeden nepovinný parametr
- Funkce vrací prvočíselného dělitele

#### Parametry:

1. `number` <-> číslo, které dělíme
2. `stop` <-> maximální počet iterací algoritmu

#### Chování funkce:

- V případě že do zadaného počtu kroků nalezne funkce prvočíselného dělitele, je navrácen
- V opačném případě je vrácena hodnota -1 signalizující chybu

### `trial_division_factors(number: int, stop: int = None)`

#### Přehled funkce:

- Algoritmus postupného dělení k faktorizaci celého čísla
- Funkce přijímá jeden povinný a jeden nepovinný parametr
- Funkce vrací seznam prvočíselných dělitelů čísla

#### Parametry:

1. `number` <-> číslo, které dělíme
2. `stop` <-> maximální počet iterací vnitřního algoritmu

#### Chování funkce:

- V případě že do zadaného počtu kroků nalezne funkce prvočíselného dělitele, je přidán do seznamu
- V opačném případě je vrácen seznam doposud nalezených dělitelů

### `pollard_rho(integer: int, stop: int = None) -> list[int]`

#### Přehled funkce:

- Algoritmus pollard rho k rozkladu celého čísla
- Funkce přijímá jeden povinný a jeden nepovinný parametr
- Funkce vrací seznam prvočíselných dělitelů čísla

#### Parametry:

1. `integer` <-> číslo, které rozkládáme
2. `stop` <-> maximální počet iterací vnitřního algoritmu

#### Chování funkce:

- V případě že do zadaného počtu kroků nalezne funkce prvočíselného dělitele, je přidán do seznamu
- V opačném případě je vrácen seznam doposud nalezených dělitelů

### `pr_remove_factor(integer: int, stop: int = None) -> int`

#### Přehled funkce:

- Algoritmus pollard rho k nalezení dělitele
- Funkce přijímá jeden povinný a jeden nepovinný parametr
- Funkce vrací seznam prvočíselných dělitelů čísla

#### Parametry:

1. `integer` <-> číslo, které rozkládáme
2. `stop` <-> maximální počet iterací vnitřního algoritmu

#### Chování funkce:

- V případě že do zadaného počtu kroků nalezne funkce dělitele, je navrácen
- V opačném případě je vráceno původní vstup

### `is_square(number: int) -> bool`

#### Přehled funkce:

- algoritmus na ověření perfektního čtverce pomocí Heronovy metody
- Funkce přijímá jeden povinný parametr
- Funkce vrací pravdivostní hodnotu testované teze

#### Parametry:

1. `number` <-> číslo, které testujeme

#### Chování funkce:

- V případě že je číslo perfektním čtvercem, vrátí funkce hodnotu True
- V opačném případě je vrácena hodnota False

### `primes_below(n)`

#### Přehled funkce:

- Efektivní prvočíselné síto pro n > 6
- Funkce přijímá jeden povinný parametr
- Funkce vrací seznam prvočísel menších než n

#### Parametry:

1. `n` <-> číslo, které rozkládáme

#### Chování funkce:

- Funkce vždy navrátí seznam prvočísel menších než n

### `pr_remove_factor(integer: int, stop: int = None) -> int`

#### Přehled funkce:

- Algoritmus pollard rho k nalezení dělitele
- Funkce přijímá jeden povinný a jeden nepovinný parametr
- Funkce vrací seznam prvočíselných dělitelů čísla

#### Parametry:

1. `integer` <-> číslo, které rozkládáme
2. `stop` <-> maximální počet iterací vnitřního algoritmu

#### Chování funkce:

- V případě že do zadaného počtu kroků nalezne funkce dělitele, je navrácen
- V opačném případě je vráceno původní vstup

### `lecm(n, smooth1 = None, max = None)`

#### Přehled funkce:

- Algoritmus lenstrových eliptických křivek na rozklad čísla na prvočinitele
- Funkce přijímá jeden povinný a dva nepovinné parametry
- Funkce vrací seznam prvočíselných dělitelů čísla

#### Parametry:

1. `n` <-> číslo, které rozkládáme
2. `smooth1` <-> první mez hladkosti algoritmu
2. `max` <-> maximální počet iterací vnitřního algoritmu

#### Chování funkce:

- Funkce navrátí seznam prvočíselných dělitelů zadaného čísla

### `ecm_remove_factor(n, smooth1 = None, max = None)`

#### Přehled funkce:

- Algoritmus lenstrových eliptických křivek na nalezení prvočinitele
- Funkce přijímá jeden povinný a dva nepovinné parametry
- Funkce vrací prvočíselného dělitele čísla ze vstupu

#### Parametry:

1. `n` <-> číslo, které rozkládáme
2. `smooth1` <-> první mez hladkosti algoritmu
2. `max` <-> maximální počet iterací vnitřního algoritmu

#### Chování funkce:

- Funkce navrátí vždy prvočíselného dělitele

### `factor_integer(number: int)`

#### Přehled funkce:

- Rychlý algoritmus na rozklad celého čísla na prvočinitele
- Funkce přijímá jeden povinný parametr
- Funkce vrací seznam prvočinitelé zadaného čísla

#### Parametry:

1. `n` <-> číslo, které rozkládáme na prvočinitele

#### Chování funkce:

- Funkce navrátí seznam prvočinitelů zadaného čísla





## (1.4) Modul `utility.py`

### `modular_exponentiation(base: int, exponent: int, mod: int) -> int`

#### Přehled funkce:

- Funkce zajišťuje efektivní mocnění nad modulem pro celá čísla
- Funkce přijímá tři povinné parametry
- Funkce vrací výsledek modulárního mocnění

#### Parametry:

1. `base` <-> Základ mocnění
2. `exponent` <-> Exponent mocnění
3. `mod` <-> Modulo nad kterým počítáme

#### Chování funkce:

- V případě že je nějaká z hodnot nesprávné hodnoty či typu, vyvolá funkce příslušnou výjimku
- V případě správnosti parametrů je navrácena hodnota `base**exponent % mod`

### `bezout(x, y) -> list[int]`

#### Přehled funkce:

- Funkce vypočítá bézoutovy koeficienty dvou přirozených čísel x, y
- Funkce příjímá dva povinné parametry
- Funkce vrací seznam délky dva, ve kterém jsou uloženy odpovídající bézoutovy koeficienty

#### Parametry:

1. `x` <-> Jedno z čísel, pro které koeficienty počítáme
2. `y` <-> Druhé z čísel, pro které koeficienty počítáme

#### Chování funkce:

- V případě že je nějaká z hodnot nesprávné hodnoty či typu, vyvolá funkce příslušnou výjimku
- V případě správnosti parametrů jsou navráceny bézoutovy koeficienty vstupních parametrů

### `get_inverse(number, mod)`

#### Přehled funkce:

- Funkce spočítá inverzní prvek k zadanému číslu nad daným modulem
- Funkce příjímá dva povinné parametry
- Funkce vrací vypočtený inverzní prvek, nebo návratovou hodnotu indikující chybu

#### Parametry:

1. `number` <-> Číslo ke kterému hledáme jeho inverzní prvek
2. `mod` <-> Modulo nad kterým pracujeme

#### Chování funkce:

- V případě že je nějaká z hodnot nesprávné hodnoty či typu, vyvolá funkce příslušnou výjimku
- V případě že je čísla `number` a `mod` soudělná, vrátí funkce hodnotu -1
- Ve zbylých případech je vrácen inverzní prvek k číslu `number` nad modulem `mod`

## (1.5) Modul `valuecheck.py`

### `check_condition(subject, condition)`

#### Přehled funkce:

- Funkce kontroluje správnost hodnoty na základě poskytnuté lambda funkce
- Funkce přijímá dva povinné parametry
- Funkce nevrací žádnou hodnotu

#### Parametry:

1. `subject` <-> Testovaná proměnná
2. `condition` <-> Funkce, která přijímá jednu hodnotu a vrací hodnotu boolean

#### Chování funkce:


- V případě, že `subject` === `None` vyvolá funkce výjimku `ValueError`
- V případě, že `condition(subject)` === `False` vyvolá funkce výjimku `ValueError`
- V ostatních případech nenastane nic

### `check_bounds(subject, min = None, max = None, type = None, strict = False)`

#### Přehled funkce:
- Funkce kontroluje, zda-li leží testovaná funkce uvnitř zadaných mezí a zda-li je testovaná funkce správného typu
- Funkce přijímá jeden povinný a čtyři nepovinné parametry
- Funkce nevrací žádnou hodnotu

#### Parametry:

1. `subject` <-> Testovaná hodnota
2. `min` <-> Dolní mez pro hodnotu `subject`
3. `max` <-> Horní mez pro hodnotu `subject`
4. `type` <-> Vyžadovaný typ hodnoty `subject`
5. `strict` <-> Boolean vylučující platnost typu `None`

#### Chování funkce:
- V případě že `strict` === `True` a `subject` === `None`, funkce vyvolá výjimku `ValueError`
- V případě že hodnota `subject` neleží mezi `min` a `max` vyvolá funkce výjimku `ValueError`
- V případě že hodnota `subject` není typu `type` funkce vyvolá výjimku `ValueError`
- V ostatních případech nenastane nic
