from pathlib import Path 
from urllib import request
import json
from concurrent.futures import ThreadPoolExecutor

API_KEY = "vwLBysKKKT8CJcyUZXqRzhuztETQnLaSQLkPfEUE"
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
Path(Path(__file__).parent / 'output-images').mkdir(exist_ok=True)
OUTPUT_IMAGES = Path(Path(__file__).parent / 'output-images')

def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    return request.urlopen(f"{APOD_ENDPOINT}/?api_key={api_key}&start_date={start_date}&end_date={end_date}" if end_date else f"{APOD_ENDPOINT}/?api_key={api_key}&date={start_date}".encode('utf-8'))
    
def download_apod_image(meta):
    if meta["media_type"] == 'image':
            title = meta["title"].replace(" ","_").replace(":","_") + ".jpg"
            request.urlretrieve(url=meta["hdurl"], filename=Path(OUTPUT_IMAGES / title))

def download_apod_images(metadata: list):
    metadata = json.loads(metadata)
    with ThreadPoolExecutor(5) as exec:
        for meta in metadata: exec.submit(download_apod_image, meta)

def main():
    metadata = get_apod_metadata(
        start_date='2021-08-01',
        end_date='2021-09-30',
        api_key=API_KEY,
    ).read().decode()
    download_apod_images(metadata)

if __name__ == '__main__':
    main()
