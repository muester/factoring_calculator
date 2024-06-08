import valuecheck as vc

# Algoritmus k rychlému mocnění s modulem
# Vstup: base - základ mocnění, exponent - exponent mocnění, mod - modulo nad kterým pracujeme
# Výstup: int - výsledek modulárního mocnění

def modular_exponentiation(base: int, exponent: int, mod: int) -> int:
    
    vc.check_bounds(base, None, None, int, strict=True)
    vc.check_bounds(exponent, 1, None, int, strict=True)
    vc.check_bounds(mod, 1, None, int, strict=True)
    
    res = 1
    while exponent > 0:
        if exponent % 2 == 1:
            res = (res*base) % mod
        exponent = exponent >> 1
        base = (base*base) % mod
    return res

# Algoritmus na výpočet bezoutových koeficientů dvou přirozených čísel 
# Vstup: x,z - hodnoty, pro které počítáme bezoutovy koeficienty
# Výstup: list[int] dvouprvkový seznam odpovídajících koeficientů

def bezout(x,y) -> list[int]:

    vc.check_bounds(x, 0, None, int, strict=True)
    vc.check_bounds(y, 0, None, int, strict=True)

    rev = False
    if y < x:
        (x,y) = (y,x)
        rev = True
    ap, ac = 1,0
    bp, bc = 0,1
    while y != 0:
        r = x // y
        (x,y) = (y, x % y)
        (ap,ac) = (ac, ap-r*ac)
        (bp,bc) = (bc, bp-r*bc)
    if rev:
        return [bp,ap]
    return [ap,bp]

# Algoritmus na výpočet inverzního prvku nad modulem 
# Vstup: number - prvek, ke kterému hledáme inverz, mod - dané modulo
# Výstup: int - inverzní prvek, NEBO -1 v případě, že inverzní prvek neexistuje

def get_inverse(number, mod):

    vc.check_bounds(number, 0, None, int, strict=True)
    vc.check_bounds(mod, 2, None, int, strict=True)

    if number % mod == 0 or mod % number == 0:
        return -1
    return bezout(number, mod)[0] % mod
