import asyncio
import time


async def async_counter(limit):
    for i in range(limit + 1):
        print(f'Counter: {i}')
        await asyncio.sleep(1)


async def main():
    limit_1 = 5
    limit_2 = 3

    await asyncio.gather(
        async_counter(limit_1),
        async_counter(limit_2)
    )


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f'Program completed in {end_time - start_time:.4f} second(s)')
