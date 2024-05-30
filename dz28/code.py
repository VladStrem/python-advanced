import asyncio
import aiohttp
import aiofiles
import os
import time


async def fetch_image(session, url, filename):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.read()
            async with aiofiles.open(filename, mode='wb') as f:
                await f.write(content)
            print(f'Image saved: {filename}')
    except aiohttp.ClientError as e:
        print(f'Failed to fetch image from {url}: {e}')
    except Exception as e:
        print(f'An error occurred while saving {filename}: {e}')


async def fetch_random_image(session, folder, image_num):
    url = "https://dog.ceo/api/breeds/image/random"
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            image_url = data['message']
            file_extension = image_url.split('.')[-1]
            filename = os.path.join(folder, f'dog_{image_num}.{file_extension}')
            await fetch_image(session, image_url, filename)
    except aiohttp.ClientError as e:
        print(f'Failed to fetch image URL: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')


async def main():
    folder = 'dog_images'
    if not os.path.exists(folder):
        os.mkdir(folder)
    num_images = 33

    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_random_image(session, folder, i) for i in range(num_images)]
        await asyncio.gather(*tasks)

    end_time = time.time()
    print(f'Operation completed: {end_time - start_time:.4f} second(s)')


if __name__ == '__main__':
    asyncio.run(main())
