import cloudscraper # very similar to requests
import random
from PIL import Image

scraper = cloudscraper.create_scraper()

response = scraper.get("https://randomwordgenerator.com/json/pictures.json")
# go directly to the JSON file the
#website uses behind the scenes to load images
data = response.json() # index data into a dictionary

random_image = random.choice(data["data"]) # pick a random key in this dictionary
image_url = "https://randomwordgenerator.com/img/picture-generator/" + random_image["image_url"]

# Download and save temporarily, then open with PIL
img_data = scraper.get(image_url).content
with open("temp.jpg", "wb") as f:
    f.write(img_data)

# Open with PIL and save
image = Image.open("temp.jpg")
image.save("scraped_image.jpg")

print("Description:", random_image["description"])
print("Saved as scraped_image.jpg!")
