
import multiprocessing
from multiprocessing import Pool
import time
import math

FLAG_ALL_DONE = b"WORK_FINISHED"
FLAG_WORKER_FINISHED_PROCESSING = b"WORKER_FINISHED_PROCESSING"

def check_prime(search_space_queue, verified_primes_queue):

    while True:
        n = search_space_queue.get() # This is a blocking operation.

        if n == FLAG_ALL_DONE:
            # flag that our results have all been pushed to the results queue
            verified_primes_queue.put(FLAG_WORKER_FINISHED_PROCESSING)
            break
        else:
            if n % 2 == 0:
                continue
            for i in range(3, int(math.sqrt(n)) + 1, 2):
                if n % i == 0:
                    break
            else:
                verified_primes_queue.put(n)


if __name__ == '__main__':

    num_of_workers = 4

    primes = []
    manager = multiprocessing.Manager()
    search_space_queue = manager.Queue()
    verified_primes_queue = manager.Queue()

    pool = Pool(processes=num_of_workers)

    # Initializing the child processes.
    processes = []
    for _ in range(num_of_workers):
        p = multiprocessing.Process(target=check_prime, 
                                    args=(  search_space_queue, 
                                            verified_primes_queue)
                                    )
        processes.append(p)
        p.start()

    # Actual calculations begin here!
    t1 = time.time()
    number_range = range(100_000_000, 101_000_000)

    # add jobs to the inbound work queue
    for number in number_range:
        search_space_queue.put(number)

    # add poison pills to stop the remote workers(force to break from the infinite loop)
    for n in range(num_of_workers):
        search_space_queue.put(FLAG_ALL_DONE)

    # Now wait till child processes complete their tasks.
    finished_child_processes = 0
    while True:
        new_result = verified_primes_queue.get() # Wait till a child process put a result to the queue
        if new_result == FLAG_WORKER_FINISHED_PROCESSING:
            finished_child_processes += 1
            if finished_child_processes == num_of_workers:
                break
        else:
            primes.append(new_result)

    assert finished_child_processes == num_of_workers

    print("Took:", time.time() - t1)
    print(len(primes), primes[:10], primes[-10:])
