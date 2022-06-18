
import multiprocessing
from multiprocessing import Pool
import time
import math

def create_range(from_i, to_i, num_processes):

    n = to_i - from_i
    chunk = (n/num_processes)

    output = []
    for i in range(num_processes):
        output.append((from_i+int(chunk*i), from_i+int(chunk*(i+1))))
    
    return output

def check_prime(n, pool, num_processes, flag):
    from_i = 3
    to_i = int(math.sqrt(n)) + 1
    flag.value = FLAG_CLEAR

    result = check_prime_in_range( (n, (from_i, min(to_i, SERIAL_CHECK_CUTOFF)), flag) )
    if to_i<=SERIAL_CHECK_CUTOFF or result==False:
        return result
    
    from_i = SERIAL_CHECK_CUTOFF
    ranges_to_check = create_range(from_i, to_i, num_processes)
    ranges_to_check = zip(num_processes*[n], ranges_to_check, num_processes*[flag])

    results = pool.map(check_prime_in_range, ranges_to_check)
    if False in results:
        return False
    return True

def check_prime_in_range(n_from_i_to_i_flag):
    (n, (from_i, to_i), flag) = n_from_i_to_i_flag
    if n % 2 == 0:
        return False
    if (from_i % 2 == 0):
        from_i = from_i - 1

    check_freq = CHECK_EVERY
    for i in range(from_i, int(to_i), 2):
        if(i%check_freq==0):
            if(flag.value==FLAG_SET):
                return False
        if n % i == 0:
            flag.value = FLAG_SET
            return False
    return True


SERIAL_CHECK_CUTOFF = 21
CHECK_EVERY = 1000
FLAG_CLEAR = b'0'
FLAG_SET = b'1'

if __name__ == '__main__':
    #[non_prime, non_prime, non_prime, prime, prime]
    test_cases = [112272535095295, 100109100129100369, 100109100129101027, 100109100129100151, 100109100129162907]

    num_of_workers = 4

    primes = []
    manager = multiprocessing.Manager()
    flag = manager.Value(b'c', FLAG_CLEAR) # Setting the initial flag
    
    for n in test_cases:
        pool = Pool(processes=num_of_workers)
        st = time.time()
        print(f'The Value {n} is a prime: {check_prime(n, pool, num_of_workers, flag)} (Took {time.time() - st} seconds)')
        
