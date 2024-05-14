import time
import os
import requests
from PIL import Image, ImageFilter
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import io

img_urls = [
    'https://images.unsplash.com/photo-1516117172878-fd2c41f4a759',
    'https://images.unsplash.com/photo-1532009324734-20a7a5813719',
    'https://images.unsplash.com/photo-1524429656589-6633a470097c',
    'https://images.unsplash.com/photo-1530224264768-7ff8c1789d79',
    'https://images.unsplash.com/photo-1564135624576-c5c88640f235',
    'https://images.unsplash.com/photo-1541698444083-023c97d3f4b6',
    'https://images.unsplash.com/photo-1522364723953-452d3431c267',
    'https://images.unsplash.com/photo-1513938709626-033611b8cc03',
    'https://images.unsplash.com/photo-1507143550189-fed454f93097',
    'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e',
    'https://images.unsplash.com/photo-1504198453319-5ce911bafcde',
    'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99',
    'https://images.unsplash.com/photo-1516972810927-80185027ca84',
    'https://images.unsplash.com/photo-1550439062-609e1531270e',
    'https://images.unsplash.com/photo-1549692520-acc6669e2f0c'
]


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return


def save_thumbnail(img_data, filename, size=(200, 200), thumb_dir='img'):
    try:
        img = Image.open(io.BytesIO(img_data))
        img.thumbnail(size)
        img.save(f'{thumb_dir}/{os.path.basename(filename)}')
    except Exception as e:
        print(f"Error processing {filename}: {e}")


def multiprocessing_approach():
    start = time.time()
    with ProcessPoolExecutor(max_workers=5) as executor:
        futures = []
        for i, url in enumerate(img_urls):
            img_data = download_image(url)
            futures.append(executor.submit(save_thumbnail, img_data, f'image_{i}.jpg'))
        for future in futures:
            future.result()
    end = time.time()
    print(f'Multiprocessing approach took {end - start:.2f} second(s)')


def main():
    multiprocessing_approach()


if __name__ == "__main__":
    main()
