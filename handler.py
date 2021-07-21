import base64
import json
import re
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from PIL import Image

def send_file(path):
    with open(path, 'rb') as image_processed:
        image_processed_data = image_processed.read()
    image_64_encode = base64.b64encode(image_processed_data)

    image_string = image_64_encode.decode('utf-8')

    return {
        "statusCode": "200",
        "body": image_string,
        "headers": {
            "Content-Type": "image/gif",
        },
        "isBase64Encoded": "true"
    }

def main(event, context):

    page_link = 'http://www.bom.gov.au/products/IDR503.loop.shtml'

    locations_link = 'http://www.bom.gov.au/products/radar_transparencies/IDR503.locations.png'
    topography_link = 'http://www.bom.gov.au/products/radar_transparencies/IDR503.topography.png'
    range_link = 'http://www.bom.gov.au/products/radar_transparencies/IDR503.range.png'
    background_link = 'http://www.bom.gov.au/products/radar_transparencies/IDR503.background.png'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }

    page_response = requests.get(page_link, headers=headers)
    soup = BeautifulSoup(page_response.text, features='html.parser')
    # print(soup)
    image_names = soup.find_all("script")[11]
    p = re.compile(r'theImageNames\[[0-9]{1,3}\] = "(.*?)";')
    gif_links = p.findall(str(image_names))

    gif_images = []

    for link in gif_links:
        response = requests.get("http://www.bom.gov.au" + link, headers=headers)
        gif_images.append(Image.open(BytesIO(response.content)).convert("RGBA"))

    response = requests.get(range_link, headers=headers)
    range_image = Image.open(BytesIO(response.content)).convert("RGBA")

    response = requests.get(locations_link, headers=headers)
    locations_image = Image.open(BytesIO(response.content)).convert("RGBA")

    response = requests.get(topography_link, headers=headers)
    topography_image = Image.open(BytesIO(response.content)).convert("RGBA")

    response = requests.get(background_link, headers=headers)
    background_image = Image.open(BytesIO(response.content)).convert("RGBA")

    created_images = []

    for image in gif_images:
        new_image = Image.alpha_composite(background_image, topography_image)
        new_image = Image.alpha_composite(new_image, image)
        new_image = Image.alpha_composite(new_image, range_image)
        new_image = Image.alpha_composite(new_image, locations_image)
        
        created_images.append(new_image)

    created_images[0].save('/tmp/radar.gif',
                save_all=True,
                append_images=created_images[1:],
                duration=400,
                loop=0)

    return send_file('/tmp/radar.gif')

if __name__ == "__main__":
    main("", "")