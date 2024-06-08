# Funkce určená ke kontrole správnosti datového typu a velikosti proměnné
# Vstup: subject - proměnná, jež testujeme, min,max - horní a dolní meze,
# -----: type - žádaný datový typ proměnné, strict - korektnost hodnoty None
# Výstup: Funkce nemá výstup, ale v případu kolize mezi podmínkami a vlastnostmi
# ------: testované hodnoty může vyvolat výjimku.

def check_bounds(subject, min = None, max = None, type=None, strict=False):
    if subject is None:
        if strict:
            raise ValueError("Value cannot be \"None\"!")
        else:
            return
    if type is not None and not isinstance(subject,type):
        raise ValueError("Incorrect value type!")
    if min is not None:
        if min > subject:
            raise ValueError("Value out of bounds!")
    if max is not None:
        if max < subject:
            raise ValueError("Value out of bounds!")

# Funkce určená k vyhodnocení booleovské hodnoty výrazu vzhledem k proměnné
# Vstup: subject - proměnná, která je použita jako vstup booleovského výrazu
# -----: condition - unární booleovská (lambda) funkce
# Výstup: Funkce nemá výstup, ale při False hodnotě zadaného výrazu vznese chybu.

def check_condition(subject, condition):
    if subject is None:
        raise ValueError("Value cannot be \"None\"!")
    if not condition(subject):
        raise ValueError("Input does not satisfy the required conditions!")