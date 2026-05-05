import cloudscraper
import random
from PIL import Image

scraper = cloudscraper.create_scraper()

def get_image():
    response = scraper.get("https://randomwordgenerator.com/json/pictures.json")
    data = response.json()

    random_image = random.choice(data["data"])
    image_url = "https://randomwordgenerator.com/img/picture-generator/" + random_image["image_url"]

    img_data = scraper.get(image_url).content
    with open("temp.jpg", "wb") as f:
        f.write(img_data)

    image = Image.open("temp.jpg")
    return image, random_image

image, random_image = get_image()  
image.save("scraped_image.jpg") 
print("Saved as scraped_image.jpg")   
print("Description:", random_image["description"])
print(image.size)