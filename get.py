import cloudscraper
import random
from PIL import Image
import os

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
while image.size != (640, 426):
    # print(f"Wrong size {image.size}") # debug
    image, random_image = get_image()

image.save("scraped_image.jpg")
print("Description:", random_image["description"])
print("Saved as scraped_image.jpg!")
print(image.size)

all_icons = [f for f in os.listdir('img_sized') if f.endswith(".jpg")]
selected_icons = random.sample(all_icons, 5)

# 4x + 3*128 = 640, x = 64, so the top row has to have blank spaces of 64 pixels
# 3x + 2*128 = 426, x = 56, so vertically they have margins of 14 pixels

def combine_16bit(v1, v2):
    '''Combine two 8-bit values into a single 16-bit value
    
       e.g., combine_16bit(32, 255) should produce 8447 or 0b0010000011111111
       v1 becomes the upper 8 bits, v2 becomes the lower 8 bits
    '''
    return (v1 << 8) | v2

def blend(envelope, hidden_images):
    '''Blend 5 hidden images into envelope in a 3+2 grid configuration'''

    blended = envelope.copy()

    x_incr = 55  # ~85px
    y_incr = 55  # ~55px

    # 3 on top row, 2 on bottom row
    positions = []
    for i in range(3):
        x = x_incr + i * (128 + x_incr)
        y = y_incr
        positions.append((x, y))
    for i in range(2):
        x = x_incr * 3 + i * (128 + x_incr)
        y = y_incr + 128 + y_incr
        positions.append((x, y))

    for hidden, (start_x, start_y) in zip(hidden_images, positions):
        for x in range(hidden.size[0]):
            for y in range(hidden.size[1]):
                er, eg, eb = envelope.getpixel((start_x + x, start_y + y))
                hr, hg, hb = hidden.getpixel((x, y))

                new_r = combine_16bit(er, hr)
                new_g = combine_16bit(eg, hg)
                new_b = combine_16bit(eb, hb)
                blended.putpixel((start_x + x, start_y + y), (new_r, new_g, new_b))

    return blended

envelope = Image.open("scraped_image.jpg")
hidden_images = [Image.open(os.path.join("img_sized", f)) for f in selected_icons]

result = blend(envelope, hidden_images)
result.save("new.jpg")