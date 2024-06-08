import valuecheck as vc

import utility

# Naivní algoritmus na testování prvočíselnosti
# Vstup: number - číslo na otestování, (stop) - nejvyšší vyzkoušený dělitels
# Výstup: bool - True když je číslo prvočíslem, False pokud složené

def trial_division(number: int, stop: int = None) -> bool:
     
    vc.check_bounds(stop, 1, None, int, strict=False)
    vc.check_bounds(number, 1, None, int, strict=True)
    
    if not stop:
        stop = number

    if number % 2 == 0:
        return False
    
    step, current = 2,3
    while current <= stop and current * current <= number:
        if number % current == 0:
            return False
        current += step
    return True

# Naivní algoritmus k získání n prvních prvočísel
# Vstup: n - žádaný počet prvočísel
# Výstup: list[int] - seznam prvních n prvočísel

def get_primes(count: int) -> list[int]:

    vc.check_bounds(count, 1, None, int, strict=True)

    primes = [2]
    count, guess = count-1, 1
    while count != 0:
        guess += 2
        for prime in primes:
            if guess % prime == 0:
                break
        else:
            primes.append(guess)
            count -= 1
    return primes

# Miller rabinův probabilistický test prvočíselnosti
# Vstup: subject - číslo, u kterého testujeme prvočíselnost, bases - počet základů, u kterých testujeme prvočíselnost
# Výstup: bool - True, když je číslo pravděpodobným prvočíslem, False pokud je číslo složené

def miller_rabin(subject: int, bases: int) -> bool:
    
    vc.check_bounds(subject, 1, None, int, strict=True)
    vc.check_bounds(bases, 1, None, int, strict=True)
    
    if subject < 2 or subject % 2 == 0:
        return False
    
    exponent, rounds = subject-1, 0
    while exponent % 2 == 0:
        exponent = exponent >> 1
        rounds += 1
    
    baselist = get_primes(bases)
    
    for base in baselist:
        a = utility.modular_exponentiation(base,exponent,subject)
        for _ in range(rounds):
            b = (a*a) % subject
            if a != 1 and b == 1 and a != subject-1:
                return False
            a = b
        if b != 1:
            return False
    return True

# Algoritmus na určení hodnot Jacobiho symbolů
# Vstup: numerator - čitatel Jacobiho symbolu, denominator - jmenovatel Jacobiho symbolu
# Výstup: int - hodnota Jacobiho symbolu numerator / denominator

def calc_jacobi(numerator: int, denominator: int) -> int:
    
    vc.check_bounds(numerator, None, None, int, strict=True)
    vc.check_bounds(denominator, 1, None, int, strict=True)
    vc.check_condition(denominator, lambda p: p % 2)

    sign = 1
    
    numerator %= denominator
    
    while numerator != 0:

        while numerator % 2 == 0:
            numerator = numerator >> 1
            if (denominator % 8) in (3,5):
                sign *= -1
        
        (numerator, denominator) = (denominator, numerator)
        if (numerator % 4) == 3 == (denominator % 4):
            sign *= -1
        
        numerator %= denominator
    
    if denominator == 1:
        return sign
    return 0

# Algoritmus na výběr vhodného Jacobiho symbolu pro sestavení Lucasovy posloupnosti
# Vstup: denominator - jmenovatel Jacobiho symbolu, pro který hledáme čitatel
# Výstup: int - čitatel takový, že čitatel a jmenovatel dávají Jacobiho symbol s hodnotou -1

def get_lucas_jacobi(denominator: int) -> int:

    sign, numerator = 1, 5

    while True:
        
        if calc_jacobi(sign*numerator,denominator) == -1:
            return numerator*sign
        
        numerator += 2
        sign *= -1

# Algoritmus na generování pořádí kroků Lucasovy sekvence
# Vstup: goal - číslo, pro jehož index chceme sestrojit Lucasovu sekvenci
# Výstup: list[int] - seznam kroků kde 0 = zvýšení indexu o 1, 1 = zdvojnásobení indexu

def get_lucas_sequence(goal: int) -> list[int]:

    vc.check_bounds(goal, 1, None, int, strict=True)

    sequence = []
    for c in "{0:b}".format(goal)[1:]:
        sequence.append(1)
        if c == '1':
            sequence.append(0)
    return sequence

# Lucasův probabilistický test prvočíselnosti
# Vstup: subject - číslo, u kterého testujeme prvočíselnost
# Výstup: bool - True, když je číslo pravděpodobným prvočíslem, False pokud je číslo složené 

def lucas_test(subject: int) -> bool:
    
    seedzero = get_lucas_jacobi(subject)
    seedone = 1
    seedtwo = (1-seedzero) >> 2

    index = 1
    first = 1
    second = 1
    for step in get_lucas_sequence(subject+1):
        if step == 1:
            first = first*second
            second = second*second - 2*utility.modular_exponentiation(seedtwo,index,subject)
            
            index *= 2
        else:
            firstterm = seedone*first + second
            secondterm = seedzero*first + seedone*second

            if firstterm % 2 == 0:
                first = firstterm >> 1
            else:
                first = (firstterm+subject) >> 1
            
            if secondterm % 2 == 0:
                second = secondterm >> 1
            else:
                second = (secondterm+subject) >> 1
            
            index += 1
        
        first %= subject
        second %= subject
    
    return first == 0

# Bailie-PSW (probabilistický?) algoritmus na určení prvočíselnosti čísla
# Vstup: subject - číslo, u kterého testujeme prvočíselnost
# Výstup: bool - True, když je číslo (pravděpodobným?) prvočíslem, False pokud je číslo složené 

def bailie_psw(subject: int) -> bool:
    if subject == 1:
        return False
    if subject == 2:
        return True
    return miller_rabin(subject, 1) and lucas_test(subject)