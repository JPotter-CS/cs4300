def check_number_sign(num):
    if num > 0:
        return "positive"
    elif num < 0:
        return "negative"
    else:
        return "zero"

def first_10_primes():
    primes = []
    candidate = 2
    while len(primes) < 10:
        is_prime = True
        for i in range(2, int(candidate ** 0.5) + 1):
            if candidate % i == 0:
                is_prime = False
        if is_prime:
            primes.append(candidate)
        candidate += 1
        
    return primes       

def sum_1_to_100():
    total = 0
    i = 1
    while i <= 100:
        total += i
        i += 1
    return total
