# # import requests
# # import base64
# # import random
# # from io import BytesIO
# # from PIL import Image


# # def place_images_on_background(
# #     background: Image.Image,
# #     save_path="output.png",
# #     max_attempts=100,
# #     save_individual=False
# # ):
# #     URLS = {
# #         "stock1": "https://picsum.photos/200/300",
# #         "stock2": "https://picsum.photos/300/300",
# #         "stock3": "https://picsum.photos/250/300",
# #         "stock4": "https://picsum.photos/300/200",
# #         "stock5": "https://picsum.photos/400/300",
# #     }

# #     # --- helper: overlap check ---
# #     def overlaps(box1, box2):
# #         x1, y1, w1, h1 = box1
# #         x2, y2, w2, h2 = box2

# #         return not (
# #             x1 + w1 <= x2 or
# #             x1 >= x2 + w2 or
# #             y1 + h1 <= y2 or
# #             y1 >= y2 + h2
# #         )

# #     bg_w, bg_h = background.size
# #     placed_boxes = []
# #     images = []

# #     # --- load images ---
# #     for name, url in URLS.items():
# #         response = requests.get(url)
# #         img_bytes = response.content

# #         if save_individual:
# #             Image.open(BytesIO(img_bytes)).save(f"{name}.png")

# #         encoded = base64.b64encode(img_bytes)
# #         decoded = base64.b64decode(encoded)
# #         img = Image.open(BytesIO(decoded)).convert("RGBA")

# #         images.append(img)

# #     # --- place images ---
# #     for img in images:
# #         w, h = img.size

# #         for _ in range(max_attempts):
# #             x = random.randint(0, bg_w - w)
# #             y = random.randint(0, bg_h - h)

# #             new_box = (x, y, w, h)

# #             if not any(overlaps(new_box, box) for box in placed_boxes):
# #                 background.paste(img, (x, y), img)
# #                 placed_boxes.append(new_box)
# #                 break

# #     # --- save result ---
# #     background.convert("RGB").save(save_path)

# #     return background



# # compose_on_bg.py
# import random
# from PIL import Image
# from sophie import bg_im

# def boxes_overlap(box1, box2):
#     """
#     box = (x, y, w, h)
#     returns True if boxes overlap
#     """
#     x1, y1, w1, h1 = box1
#     x2, y2, w2, h2 = box2

#     return not (
#         x1 + w1 <= x2 or  # box1 right <= box2 left
#         x2 + w2 <= x1 or  # box2 right <= box1 left
#         y1 + h1 <= y2 or  # box1 bottom <= box2 top
#         y2 + h2 <= y1     # box2 bottom <= box1 top
#     )

# def find_non_overlapping_position(bg_w, bg_h, fg_w, fg_h, existing_boxes, max_tries=1000):
#     """
#     Try random (x, y) positions until we find a non-overlapping one
#     or give up after max_tries.
#     """
#     for _ in range(max_tries):
#         x = random.randint(0, max(0, bg_w - fg_w))
#         y = random.randint(0, max(0, bg_h - fg_h))
#         new_box = (x, y, fg_w, fg_h)

#         # Check against all existing boxes
#         if all(not boxes_overlap(new_box, b) for b in existing_boxes):
#             return x, y

#     return None  # couldn't find a spot

# def compose_images_on_background(
#     foreground_paths,
#     output_path="final_composite.jpg"
# ):
#     # 1. Create / get scraped background
#     bg_path = bg_im()  # "scraped_image.jpg" by default
#     background = Image.open(bg_path).convert("RGBA")
#     bg_w, bg_h = background.size

#     # 2. Open and resize foreground images
#     foregrounds = []
#     for path in foreground_paths:
#         img = Image.open(path).convert("RGBA")

#         # Example resize: each image ~ 1/4 of bg width
#         target_width = bg_w // 4
#         w, h = img.size
#         scale = min(1.0, target_width / w)  # avoid upscaling too much
#         new_size = (int(w * scale), int(h * scale))
#         img = img.resize(new_size, Image.LANCZOS)
#         foregrounds.append(img)

#     # 3. Place each image at a random non-overlapping position
#     placed_boxes = []  # list of (x, y, w, h)
#     for fg in foregrounds:
#         fg_w, fg_h = fg.size

#         pos = find_non_overlapping_position(bg_w, bg_h, fg_w, fg_h, placed_boxes)
#         if pos is None:
#             print("Warning: could not find non-overlapping position for one image.")
#             continue

#         x, y = pos
#         placed_boxes.append((x, y, fg_w, fg_h))

#         background.alpha_composite(fg, dest=(x, y))

#     # 4. Save result
#     background = background.convert("RGB")
#     background.save(output_path)
#     print(f"Saved final composite as {output_path}!")

# if __name__ == "__main__":

#     foreground_urls = {
#         "img1": "https://example.com/path/to/image1.png",
#         "img2": "https://example.com/path/to/image2.jpg",
#         "img3": "https://example.com/path/to/image3.png",
#         "img4": "https://example.com/path/to/image4.jpg",
#         "img5": "https://example.com/path/to/image5.png",
#     }
#     compose_images_on_background(foreground_urls)


# compose.py
# import random
# from io import BytesIO
# import cloudscraper
# from PIL import Image
# # sophie import bg_im

# scraper = cloudscraper.create_scraper()




# def bg_im(output_path="scraped_image.jpg"):
#     #scraper = cloudscraper.create_scraper()

#     response = scraper.get("https://randomwordgenerator.com/json/pictures.json")
#     # go directly to the JSON file the
#     #website uses behind the scenes to load images
#     data = response.json() # index data into a dictionary

#     random_image = random.choice(data["data"]) # pick a random key in this dictionary
#     image_url = "https://randomwordgenerator.com/img/picture-generator/" + random_image["image_url"]

#     # Download and save temporarily, then open with PIL
#     img_data = scraper.get(image_url).content
#     with open("temp.jpg", "wb") as f:
#         f.write(img_data)

#     # Open with PIL and save
#     image = Image.open("temp.jpg").convert('RGB')
#     image.save("output_path")

#     print("Description:", random_image["description"])
#     print("Saved as {output_path}!")
#     return output_path



# def boxes_overlap(box1, box2):
#     """
#     box = (x, y, w, h)
#     returns True if boxes overlap
#     """
#     x1, y1, w1, h1 = box1
#     x2, y2, w2, h2 = box2

#     return not (
#         x1 + w1 <= x2 or  # box1 right <= box2 left
#         x2 + w2 <= x1 or  # box2 right <= box1 left
#         y1 + h1 <= y2 or  # box1 bottom <= box2 top
#         y2 + h2 <= y1     # box2 bottom <= box1 top
#     )


# def find_non_overlapping_position(bg_w, bg_h, fg_w, fg_h, existing_boxes, max_tries=1000):
#     """
#     Try random (x, y) positions until we find a non-overlapping one
#     or give up after max_tries.
#     """
#     for _ in range(max_tries):
#         x = random.randint(0, max(0, bg_w - fg_w))
#         y = random.randint(0, max(0, bg_h - fg_h))
#         new_box = (x, y, fg_w, fg_h)

#         # Check against all existing boxes
#         if all(not boxes_overlap(new_box, b) for b in existing_boxes):
#             return x, y

#     return None  # couldn't find a spot


# def download_image_from_url(url: str) -> Image.Image:
#     resp = scraper.get(url)
#     resp.raise_for_status()
#     return Image.open(BytesIO(resp.content)).convert("RGBA")


# def compose_images_on_background(
#     foreground_urls: dict,
#     output_path: str = "final_composite.jpg",
# ):
#     # 1. Create / get scraped background
#     bg_path = bg_im()  # returns "scraped_image.jpg" by default
#     background = Image.open(bg_path).convert("RGBA")
#     bg_w, bg_h = background.size

#     # 2. Download and resize foreground images
#     foregrounds = []  # list of PIL Images
#     for name, url in foreground_urls.items():
#         try:
#             img = download_image_from_url(url)

#             # Resize: each image ~ 1/4 of bg width (tweak as you like)
#             target_width = bg_w // 4
#             w, h = img.size
#             scale = min(1.0, target_width / w)  # avoid huge upscaling
#             new_size = (int(w * scale), int(h * scale))
#             img = img.resize(new_size, Image.LANCZOS)

#             foregrounds.append(img)
#         except Exception as e:
#             print(f"Failed to load {name} from {url}: {e}")

#     # 3. Place each image at a random non-overlapping position
#     placed_boxes = []  # list of (x, y, w, h)
#     for fg in foregrounds:
#         fg_w, fg_h = fg.size

#         pos = find_non_overlapping_position(bg_w, bg_h, fg_w, fg_h, placed_boxes)
#         if pos is None:
#             print("Warning: could not find non-overlapping position for one image.")
#             continue

#         x, y = pos
#         placed_boxes.append((x, y, fg_w, fg_h))

#         background.alpha_composite(fg, dest=(x, y))

#     # 4. Save result
#     background = background.convert("RGB")
#     background.save(output_path)
#     print(f"Saved final composite as {output_path}!")


# if __name__ == "__main__":
#     # Replace these URLs with your real ones
#     foreground_urls = {
#         "img1": "https://example.com/path/to/image1.png",
#         "img2": "https://example.com/path/to/image2.jpg",
#         "img3": "https://example.com/path/to/image3.png",
#         "img4": "https://example.com/path/to/image4.jpg",
#         "img5": "https://example.com/path/to/image5.png",
#     }

#     compose_images_on_background(foreground_urls)



import random
from io import BytesIO
import cloudscraper
from PIL import Image

scraper = cloudscraper.create_scraper()


def bg_im(output_path="scraped_image.jpg"):
    response = scraper.get("https://randomwordgenerator.com/json/pictures.json")
    data = response.json()

    random_image = random.choice(data["data"])
    image_url = (
        "https://randomwordgenerator.com/img/picture-generator/"
        + random_image["image_url"]
    )

    # Download and save temporarily, then open with PIL
    img_data = scraper.get(image_url).content
    with open("temp.jpg", "wb") as f:
        f.write(img_data)

    # Open with PIL and save
    image = Image.open("temp.jpg").convert("RGB")
    image.save(output_path)  # <-- use the variable, not the string literal

    print("Description:", random_image["description"])
    print(f"Saved as {output_path}!")  # <-- f-string
    return output_path               # <-- this path now actually exists


#Prior to is sophies part with the added output_path that is a variable thats equal to scrapped_image.jpg


def boxes_overlap(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return not (
        x1 + w1 <= x2 or
        x2 + w2 <= x1 or
        y1 + h1 <= y2 or
        y2 + h2 <= y1
    )


def find_non_overlapping_position(bg_w, bg_h, fg_w, fg_h, existing_boxes, max_tries=1000):
    for _ in range(max_tries):
        x = random.randint(0, max(0, bg_w - fg_w))
        y = random.randint(0, max(0, bg_h - fg_h))
        new_box = (x, y, fg_w, fg_h)
        if all(not boxes_overlap(new_box, b) for b in existing_boxes):
            return x, y
    return None


def download_image_from_url(url: str) -> Image.Image:
    resp = scraper.get(url)
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content)).convert("RGBA")


def compose_images_on_background(
    foreground_urls: dict,
    output_path: str = "final_image.jpg",
):
    # 1. Create / get scraped background
    bg_path = bg_im()  # now really points to a saved file
    background = Image.open(bg_path).convert("RGBA")
    bg_w, bg_h = background.size

    # 2. Download and resize foreground images
    foregrounds = []
    for name, url in foreground_urls.items():
        try:
            img = download_image_from_url(url)

            target_width = bg_w // 4
            w, h = img.size
            scale = min(1.0, target_width / w)
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.LANCZOS) ##LANCZOS Tells python how to shrink

            foregrounds.append(img)
        except Exception as e:
            print(f"Failed to load {name} from {url}: {e}")

    # 3. Random non-overlapping placement
    placed_boxes = []
    for fg in foregrounds:
        fg_w, fg_h = fg.size
        pos = find_non_overlapping_position(bg_w, bg_h, fg_w, fg_h, placed_boxes)
        if pos is None:
            print("Warning: could not find non-overlapping position for one image.")
            continue

        x, y = pos
        placed_boxes.append((x, y, fg_w, fg_h))
        background.alpha_composite(fg, dest=(x, y))

    # 4. Save result
    background.convert("RGB").save(output_path)
    print(f"Saved final composite as {output_path}!")


if __name__ == "__main__":
    foreground_urls = { #Call stock data {Url : }
                        "Image1": "https://picsum.photos/200/300",
                        "Image2": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Red_crystal.jpg",
                        "Image3": "https://media.istockphoto.com/id/624179406/photo/six-of-diamonds.jpg?s=612x612&w=0&k=20&c=5XRwH63549MscCdZ-jJE0B4YOw5jVGn436cdG6Urekk=",
                        "Image4": "https://upload.wikimedia.org/wikipedia/commons/4/4f/US_100_dollar_bill_series_2009.jpg",
                        "Image5": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Blue_pen.jpg",
    }
    compose_images_on_background(foreground_urls)
###GOnna ask george
