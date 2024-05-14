import random
import time
import threading


def generate_list(n):
    return [random.randint(-20, 20) for _ in range(n)]


def sum_and_product(numbers, result):
    total_sum = sum(numbers)
    total_product = 1
    for num in numbers:
        total_product *= num
    result.append((total_sum, total_product))


def main_multithreaded(n):
    numbers = generate_list(n)
    result = []
    start_time = time.time()
    thread1 = threading.Thread(target=sum_and_product, args=(numbers, result))
    thread2 = threading.Thread(target=sum_and_product, args=(numbers, result))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    total_sum = sum(res[0] for res in result)
    total_product = 1
    for res in result:
        total_product *= res[1]
    end_time = time.time()
    print(f"Сума елементів: {total_sum}")
    print(f"Добуток елементів: {total_product}")
    print(f"Час виконання: {end_time - start_time} сек")


n = int(input("Введіть розмір списку: "))
main_multithreaded(n)
