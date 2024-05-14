import threading


def write_even_numbers(filename, numbers):
    even_numbers = [str(num) for num in numbers if num % 2 == 0]
    with open(filename, mode='w') as file:
        file.write('\n'.join(even_numbers))


def write_odd_numbers(filename, numbers):
    odd_numbers = [str(num) for num in numbers if num % 2 != 0]
    with open(filename, mode='w') as file:
        file.write('\n'.join(odd_numbers))


def main():
    file_path = input("Введіть шлях до файлу: ")

    with open(file_path) as file:
        numbers = [int(num) for num in file.read().split()]

    even_thread = threading.Thread(target=write_even_numbers, args=('even_numbers.txt', numbers))
    odd_thread = threading.Thread(target=write_odd_numbers, args=('odd_numbers.txt', numbers))

    even_thread.start()
    odd_thread.start()

    even_thread.join()
    odd_thread.join()

    even_count = sum(1 for num in numbers if num % 2 == 0)
    odd_count = sum(1 for num in numbers if num % 2 != 0)

    print(f"Кількість парних чисел: {even_count}")
    print(f"Кількість непарних чисел: {odd_count}")


if __name__ == "__main__":
    main()
