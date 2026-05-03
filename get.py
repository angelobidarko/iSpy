import cloudscraper
import random
from PIL import Image, ImageFilter
import os

# def blur_white_background(image_path, output_path, threshold=230):
#     img = Image.open(image_path).convert("RGBA")
    
#     # Create a mask where white/near-white pixels are selected
#     data = img.getdata()
#     mask = Image.new("L", img.size, 0)
    
#     new_mask_data = []
#     for item in data:
#         if item[0] > threshold and item[1] > threshold and item[2] > threshold:
#             new_mask_data.append(255)
#         else:
#             new_mask_data.append(0)
#     mask.putdata(new_mask_data)

#     blurred_img = img.filter(ImageFilter.GaussianBlur(radius=10))
    
#     # Composite and save
#     final_img = Image.composite(blurred_img, img, mask)
#     final_img.convert("RGB").save(output_path)

# # --- Batch Processing Logic ---

# input_folder = "img_sized"
# output_folder = "img_blurred"

# # Create the output directory if it doesn't exist
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# # Loop through all files in the img_sized directory
# for filename in os.listdir(input_folder):
#     if filename.lower().endswith((".jpg", ".jpeg", ".png")):
#         input_path = os.path.join(input_folder, filename)
#         output_path = os.path.join(output_folder, filename)
        
#         blur_white_background(input_path, output_path)

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
# print("Description:", random_image["description"])
# print("Saved as scraped_image.jpg!")
# print(image.size)


all_icons = [f for f in os.listdir('img_blurred') if f.endswith(".jpg")]
selected_icons = random.sample(all_icons, 5)

def boxes_overlap(box1, box2):
     """
     box = (x, y, w, h)
     returns True if boxes overlap
     """
     x1, y1, w1, h1 = box1
     x2, y2, w2, h2 = box2

     return not (
         x1 + w1 <= x2 or  # box1 right <= box2 left
         x2 + w2 <= x1 or  # box2 right <= box1 left
         y1 + h1 <= y2 or  # box1 bottom <= box2 top
         y2 + h2 <= y1     # box2 bottom <= box1 top
     )


def find_non_overlapping_position(bg_w, bg_h, fg_w, fg_h, existing_boxes, max_tries=1000):
     """
     Try random (x, y) positions until we find a non-overlapping one
     or give up after max_tries.
     """
     for _ in range(max_tries):
         x = random.randint(0, max(0, bg_w - fg_w))
         y = random.randint(0, max(0, bg_h - fg_h))
         new_box = (x, y, fg_w, fg_h)

#         # Check against all existing boxes
         if all(not boxes_overlap(new_box, b) for b in existing_boxes):
             return x, y

     return None  # couldn't find a spot


def blend(envelope, hidden_images):
    '''Blend 5 hidden images into envelope at random, non-overlapping positions'''
    blended = envelope.copy()
    e_w, e_h = envelope.size
    placed_boxes = []  # To track (x, y, width, height)

    for hidden in hidden_images:
        h_w, h_h = hidden.size
        
        # Use your helper function to find a valid spot
        pos = find_non_overlapping_position(e_w, e_h, h_w, h_h, placed_boxes)
        
        if pos:
            start_x, start_y = pos
            placed_boxes.append((start_x, start_y, h_w, h_h))
            
            # Perform the pixel blending at the found position
            for x in range(h_w):
                for y in range(h_h):
                    er, eg, eb = envelope.getpixel((start_x + x, start_y + y))
                    hr, hg, hb = hidden.getpixel((x, y))
                    
                    new_r = combine_16bit(er, hr)
                    new_g = combine_16bit(eg, hg)
                    new_b = combine_16bit(eb, hb)
                    
                    blended.putpixel((start_x + x, start_y + y), (new_r, new_g, new_b))
        else:
            print("Warning: could not find non-overlapping position for an image.")
            
    return blended


def combine_16bit(v1, v2):
    '''Combine two 8-bit values into a single 16-bit value
    
       e.g., combine_16bit(32, 255) should produce 8447 or 0b0010000011111111
       v1 becomes the upper 8 bits, v2 becomes the lower 8 bits
    '''
    # return (v1 << 8) | v2
    return v2

envelope = Image.open("scraped_image.jpg")
hidden_images = [Image.open(os.path.join("img_blurred", f)) for f in selected_icons]

result = blend(envelope, hidden_images)
result.save("new.jpg")
print("Open new.jpg to play game!")
