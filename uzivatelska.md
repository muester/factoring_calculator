# Uživatelská dokumentace

## Obecné pojednání o softwaru

Program je určen k rozkladu celých čísel na prvočísla. Program je poskytován jako konzolová utilita, tak i grafický program si intuitivním ovládáním.

- Přestože je možný výběr faktorizačního algoritmu, v případě jinak nespecifikovaném je doporučeno používat základní vyhodnocovací algoritmus na výběr nejefektivnějšího řešení, čímž se vyvarujeme situacím, kde je číslo pro daný algoritmus obtížné na rozklad.

## Konzolové rozhraní

Program funguje jako konzolová utilita - příkaz, který je schopen rozložit jedno číslom, navrátit tento rozklad a posléze ukončit svůj běh.

Syntaxe příkazu je následující:

`py main.py <číslo> [arg]`

- <číslo> je povinný parametr, za který dosazujeme číslo, které chceme rozkládat

- [arg] je nepovinný parametr, který slouží k výběru algoritmu, který bude číslo rozkládat. Existují následujicí možné argumenty:
    1. `t` - bude použit algoritmus **Trial Division**
    2. `p` - bude použit algoritmus **Pollard Rho**
    3. `e` - bude použit algoritmus **LECM**
    4. `b` - bude použit "nejvhodnější" algoritmus\
    *(Ve skutečnosti jsou nejdříve mocí algoritmu **Trial Division** s jistou efektivní fixně danou horní hranicí odstraněny menší dělitele, následně pomocí **Pollard Rho** "středně velké" dělitelé, a zbytek je již rozkládán identicky jako u algoritmu **LECM**)*
    5. Pokud není poskytnut, využije funkce defaultní hodnotu `b`

Příklad použití:
```
> py main.py 123456789 t
Factorization of 123456789: 
[3, 3, 3607, 3803]
```
```
> py main.py 965089610498837851706543 p
Factorization of 993503055724876736575909: 
[512125251221, 1939961080529]
```
```
> py main.py 995467299549013926977643495882345920497
Factorization of 995467299549013926977643495882345920497: 
[14717496696710310791, 67638357260275322567]
```
```
> py main.py -8                                     
Error: incorrect input format!
> py main.py two
Error: incorrect input format!
> py main.py 77 4
Error: unrecognized argument!
```


## Grafické rozhraní

Grafické rozhraní poskytuje stejnou funkčnost jako utilita z příkazového řádku, ovšem s možností vícero vstupů mezi jednotlivým spuštěním programu.

Syntaxe otebvření grafického rozhraní je následující:

`py main.py`

Grafické okno se zkládá z následujících komponent:

- **Textové pole** - do tohoto textového pole zadává uživatel vstup, tedy právě jedno celé číslo na prvočíselný rozklad

- **Rozbalovací seznam** - v seznamu jsou vypsány názvy jednotlivých algoritmů, které uživatel může kliknutím zvolit. Zvolený algoritmus bude následně použit v případě rozkladu zadaného čísla.

- **Tlačítko Factor!** - po zmáčknutí tlačítka proběhne rozklad čísla v textovém poli za pomocí zvoleného algoritmu. Výsledek bude zobrazen v textovém štítku níže.

- **Textový štítek** - začíná prázdný, jeho hodnota je upravena po zmáčknutí tlačítka výše. Slouží přimárně k zobrazení výsledného rozkladu, ale také k vyrozumění uživatele s případnou chybou běhu programu.


**Upozornění!** - V případě, že výpočet rozkladu trvá dobu delší než sekundu (což nastává pouze u čísel k rozkladu obtížných) dojde k "zamrznutí" aplikace. Aplikace se navrátí k normálnímu chodu po ukončení výpočtu.