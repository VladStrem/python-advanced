import random
import time
import threading


def generate_list(n):
    return [random.randint(-20, 20) for _ in range(n)]


def calculate_sum(numbers, result):
    total_sum = sum(numbers)
    result['sum'] = total_sum


def calculate_product(numbers, result):
    total_product = 1
    for num in numbers:
        if num == 0:
            total_product = 0
            break
        total_product *= num
    result['product'] = total_product


def main_multithreaded(n):
    numbers = generate_list(n)
    result = {}

    start_time = time.time()

    thread1 = threading.Thread(target=calculate_sum, args=(numbers, result))
    thread2 = threading.Thread(target=calculate_product, args=(numbers, result))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    total_sum = result.get('sum', 0)
    total_product = result.get('product', 1)

    end_time = time.time()

    print(f"Сума елементів: {total_sum}")
    print(f"Добуток елементів: {total_product}")
    print(f"Час виконання: {end_time - start_time} сек")


if __name__ == "__main__":
    n = int(input("Введіть розмір списку: "))
    main_multithreaded(n)
