import valuecheck as vc

import math
import random
import primality
import utility

#--- Trial Division ---#

# Algoritmus postupného dělení k nalezení dělitele
# Vstup: number - číslo na rozklad, (stop) - nejvyšší vyzkoušený dělitel
# Výstup: int - dělitel, NEBO -1, pokud dělitel nebyl nalezen

def trial_division(number: int, stop: int = None) -> bool:
    
    if not stop:
        stop = number

    if number % 2 == 0:
        return 2
    
    step, current = 2,3
    while current <= stop and current * current <= number:
        if number % current == 0:
            return current
        current += step
    return -1

# Algoritmus postupného dělení k faktorizaci celého čísla
# Vstup: number - číslo na rozklad, (stop) - nejvyšší vyzkoušený dělitel
# Výstup: list[int] - seznam dělitelů, kde poslední není nutně prvočíslo

def trial_division_factors(number: int, stop: int = None):
    factors = []
    while True:
        if primality.bailie_psw(number):
            factors.append(number)
            return sorted(factors)
        factor = trial_division(number, stop)
        if factor == -1:
            if number != 1:
                factors.append(number)
            break
        factors.append(factor)
        number //= factor
    return sorted(factors)

#--- Pollard Rho ---#

# Algoritmus pollard rho k rozkladu celého čísla
# Vstup: integer - číslo na rozklad, (stop) - maximální počet cyklů algoritmu
# Výstup: int[list] - seznam dělitelů, kde poslední není nutně prvočíslo

def pollard_rho(integer: int, stop: int = None) -> list[int]:
    stack = [integer]
    factors = []

    while stack:
        current = stack.pop()
        if current % 2 == 0:
            factors.append(2)
            stack.append(current // 2)
        else:
            stack.append(current)
            break

    while stack:
        current = stack.pop()
        factor = pr_remove_factor(current, stop)
        if factor == 1:
            continue
        if current == factor:
            factors.append(current)
        else:
            stack.append(factor)
            stack.append(current  // factor)
    return sorted(factors)

# Algoritmus pollard rho k nalezení dělitele
# Vstup: integer - číslo na rozklad, (stop) - maximální počet cyklů algoritmu
# Výstup: int - dělitel, (který nutně není? prvočíslem)

def pr_remove_factor(integer: int, stop: int = None) -> int:
    if primality.bailie_psw(integer) == True or integer == 1:
        return integer
    if is_square(integer):
        return int(math.sqrt(integer))
    
    seed = 2
    head = seed
    trail = seed
    cofactor = integer

    count = 0

    while cofactor == integer:
        cofactor = 1
        while cofactor == 1:
            if stop is not None and count >= stop:
                return integer
            count += 1
            head = pol_functor(head, integer)
            trail = pol_functor(pol_functor(trail, integer), integer)
            cofactor = math.gcd(abs(head-trail),integer)
        seed += 1
        head = seed
        trail = seed
    return cofactor

def pol_functor(x, mod):
    return ((x*x) + 1) % mod 

# Naivní algoritmus na ověření perfektního čtverce pomocí Heronovy metody
# Vstup: number - zkoumané číslo
# Výstup: bool - True pokud je číslo druhou mocninou jiného přirozeného číslo, False pokud ne

def is_square(number: int) -> bool:
    
    vc.check_bounds(number, 0, None, int, strict=True)

    root = math.isqrt(number)
    return (root*root) == number

# Efektivní prvočíselné síto pro n > 6
# Vstup: n - horní mez číselného síta
# Výstup: list[int] - seznam prvočísel do horní meze
# pozn: Autorem algoritmu je uživatel stackoverflow.com s přezdívkou Robert William Hanks


def primes_below(n):
    n, correction = n-n%6+6, 2-(n%6>1)
    sieve = [True] * (n//3)
    for i in range(1,int(n**0.5)//3+1):
      if sieve[i]:
        k=3*i+1|1
        sieve[      k*k//3      ::2*k] = [False] * ((n//6-k*k//6-1)//k+1)
        sieve[k*(k-2*(i&1)+4)//3::2*k] = [False] * ((n//6-k*(k-2*(i&1)+4)//6-1)//k+1)
    return [2,3] + [3*i+1|1 for i in range(1,n//3-correction) if sieve[i]]

# Třída reprezentující bod na el. křivce za pomocí montgomeryho (projektivní) reprezentace
# Součástí třídy jsou odpovídající metody na součet dvou bodů a násobení bodu celým číslem
# Návrh třídy a algoritmů dle článku:
# Montgomery curves and their arithmetic - The case of large characteristic fields

class Point:
    
    def __init__(self, x, z, m, a):
        self.x = x
        self.z = z
        self.m = m
        self.a = a

    def add(self, other, diff):
        p = (self.x - self.z) * (other.x + other.z)
        q = (self.x + self.z) * (other.x - other.z)
        

        plus = p + q
        minus = p - q
        
        x_new = ((diff.z) * plus * plus ) % self.m
        z_new = ((diff.x) * minus * minus ) % self.m

        return Point(x_new, z_new, self.m, self.a)
    
    def double(self):
        p = ((self.x + self.z) * (self.x + self.z)) % self.m
        q = ((self.x - self.z) * (self.x - self.z)) % self.m

        minus = p - q

        x_new = (p * q) % self.m
        z_new = ((q + ((self.a) * minus)) * minus) % self.m

        return Point(x_new, z_new, self.m, self.a)
    
    def mult(self, k):

        r0 = Point(self.x, self.z, self.m, self.a)
        r1 = Point(self.x, self.z, self.m, self.a).double()

        for inst in "{0:b}".format(k)[1:]:

            if inst == '0':
                r1 = r0.add(r1, self)
                r0 = r0.double()
            else:
                r0 = r1.add(r0, self)
                r1 = r1.double()

        return r0

# Algoritmus lenstrových eliptických křivek na rozklad čísla na prvočinitele
# Vstup: n - rozkládané číslo, smooth1 - hladkost první fáze, max - maximální počet zkoušených křivek
# Výstup: int[list] - seznam dělitelů, kde poslední není nutně prvočíslo
# Design algoritmu dle knihy prime numbers: a computational perspective, kapitola 7.4

def lecm(n, smooth1 = None, max = None):
    factors = []
    while primality.bailie_psw(n) != True:
        f = ecm_remove_factor(n, smooth1, max)
        factors.extend(lecm(f))
        n = n // f
    factors.append(n)
    return sorted(factors)

# Algoritmus lenstrových eliptických křivek na nalezení dělitele
# Vstup: n - rozkládané číslo, smooth1 - hladkost první fáze, max - maximální počet zkoušených křivek
# Výstup: int - prvočíselný dělitel čísla

def ecm_remove_factor(n, smooth1 = None, max = None):
    
    low_fac = trial_division(n,1000000)
    if low_fac != -1:
        return low_fac
    
    if smooth1 is None:
        bit_factor = math.ceil(math.log2(n)) // 2
        if bit_factor <= 40:
            smooth1 = 1629
        elif bit_factor <= 55:
            smooth1 = 12820
        elif bit_factor <= 65:
            smooth1 = 24433
        elif bit_factor <= 70:
            smooth1 = 32918
        elif bit_factor <= 75:
            smooth1 = 64703
        elif bit_factor <= 80:
            smooth1 = 76620
        elif bit_factor <= 90:
            smooth1 = 183849
        else:
            smooth1 = 445657
    if smooth1 & 1 != 0:
        smooth1 -= 1

    smooth2 = 100*smooth1
    d = math.ceil(math.sqrt(smooth2))
    primes = primes_below(smooth2 + 4*d)
    k = 1
    for prime in primes:
        if prime >= smooth1:
            break
        k *= pow(prime, int(math.log(smooth1, prime)))
    deltalist = []

    lower = 0
    for r in range(smooth1,smooth2,2*d):
        deltas = set()
        for i in range(lower,len(primes)):
            if primes[i] < r+2:
                lower = i
                continue
            if primes[i] >= r + 2*d:
                break
            deltas.add((abs(primes[i]-r)) //2) 
        deltalist.append(list(deltas))

    # Parametrizace dle
    # https://inria.hal.science/inria-00070192v1/document
    
    curve = 0
    while True:
        curve += 1
        if max is not None and curve > max:
            return n
        sig = random.randint(6,n-1)
        u = (sig*sig - 5) % n
        v = (4 * sig) % n
        minus = v - u
        x0 = utility.modular_exponentiation(u,3,n)
        z0 = utility.modular_exponentiation(v,3,n)
    

        # we need to divide by this monstrosity (i think)
        a = None
        c = utility.get_inverse(4*x0*v,n)
        if c == -1:
            a = math.gcd((4*x0*v),n)
        else:
            t1 = utility.modular_exponentiation(minus,3,n)
            t2 = (3*u+v)
            t3 = utility.get_inverse(4*x0*v,n) 
            a = (((t1*t2*t3)) - 2) % n
    
        
        four = utility.get_inverse(4,n)
        a24 = ((a+2)*four) % n

        point = Point(x0, z0, n, a24)
        point = point.mult(k)
        g = math.gcd(n,point.z)

        if g != n and g != 1:
            return g
        
        if g == n:
            continue
        
        blist = [0] * math.ceil(d+1)
        plist = [0] * math.ceil(d+1)
        
        plist[1] = point.double()
        plist[2] = plist[1].double()

        blist[1] = (plist[1].x * plist[1].z) % n
        blist[2] = (plist[2].x * plist[2].z) % n

        for cd in range(3,d+1):
            plist[cd] = plist[cd - 1].add(point.double(),plist[cd-2])
            blist[cd] = (plist[cd].x * plist[cd].z) % n
        
        g = 1
        T = point.mult(smooth1 - 2*d)
        R = point.mult(smooth1)

        for deltas in deltalist:
            alpha = (R.x*R.z) % n
            for delta in deltas:
                g = (g*((R.x - plist[delta].x) * (R.z + plist[delta].z) - alpha + blist[delta])) % n
            R,T = R.add(plist[d],T), R

        g = math.gcd(g,n)
        
        if g != 1 and g != n:   
            return g

#--- General Factoring ---#

# Rychlý algoritmus na rozklad celého čísla na prvočinitele
# Vstup: n - rozkládané číslo
# Výstup: list[int] - seznam prvočíselných dělitelů

def factor_integer(number: int):
    factors = []
    while True:
        res = trial_division(number, 100_000)
        if res == -1:
            break
        factors.append(res)
        number = number // res
    if primality.bailie_psw(number) or number == 1:
        if not number == 1:
            factors.append(number)
        return sorted(factors)
    else:
        factors.extend(pollard_rho(number,1_500_000))
        if primality.bailie_psw(factors[-1]):
            return sorted(factors)
        else:
            factors.extend(lecm(factors.pop()))
            return sorted(factors)