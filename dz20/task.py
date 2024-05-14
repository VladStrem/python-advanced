import multiprocessing
import random
import time


def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True


def count_primes_in_chunk(chunk):
    count = 0
    for num in chunk:
        if is_prime(num):
            count += 1
    return count


if __name__ == "__main__":
    n = 1000000
    num_processes = multiprocessing.cpu_count()
    chunk_size = n // num_processes

    numbers = [random.randint(2, 9999) for _ in range(n)]

    chunks = [numbers[i:i + chunk_size] for i in range(0, n, chunk_size)]

    start_time = time.time()

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(count_primes_in_chunk, chunks)

    total_primes = sum(results)

    end_time = time.time()

    print(f"Total primes: {total_primes}")
    print(f"Time taken: {end_time - start_time} seconds")
