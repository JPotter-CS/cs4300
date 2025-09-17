def check_number_sign(num):
    # I dont think this needs comments
    if num > 0:
        return "positive"
    elif num < 0:
        return "negative"
    else:
        return "zero"

def first_10_primes():
    primes = []
    candidate = 2
    # Continues while loop until all 10 prime numbers are put into the primes list
    while len(primes) < 10:
        # Initializing is_prime to true
        is_prime = True
        # while i is in range of 2 up to the square root of the canidate
        for i in range(2, int(candidate ** 0.5) + 1):
            # Checks in canidate is perfectly divisible by i. If it is it is not a prime
            if candidate % i == 0:
                is_prime = False
        # If it reaches here it is a prime
        if is_prime:
            # Appends canidate to primes
            primes.append(candidate)
        # INC canidate
        candidate += 1
        
    return primes       

def sum_1_to_100():
    # Init total var to track total sum
    total = 0
    # Init i to 1
    i = 1
    # iterate to 100
    while i <= 100:
        # Add i to total
        total += i
        # INC i
        i += 1
    return total
