import random
import csv
import cloudscraper
from PIL import Image
import numpy as np


scraper = cloudscraper.create_scraper()

# ─────────────────────────────────────────────
#  CSV LOADING
# ─────────────────────────────────────────────

def load_items_from_csv(csv_path: str) -> list[dict]:
    """Load image items from CSV with columns: Names, h0, h1, h2, h3, image."""
    items = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append({
                "name":   row["Names"].strip(),
                "hints":  [row["h0"], row["h1"], row["h2"], row["h3"]],
                "image":  row["image"].strip(),
            })
    return items


# ─────────────────────────────────────────────
#  BACKGROUND SCRAPING
# ─────────────────────────────────────────────


def image_brightness(img):
    """Return the mean pixel brightness (0=black, 255=white)."""
    arr = np.array(img.convert("L"))
    return arr.mean()

def bg_im(brightness_threshold=150):
    """Scrape a random image, only keeping it if it's dark enough."""
    while True:
        response = scraper.get("https://randomwordgenerator.com/json/pictures.json")
        data = response.json()
        random_image = random.choice(data["data"])
        image_url = (
            "https://randomwordgenerator.com/img/picture-generator/"
            + random_image["image_url"]
        )
        img_data = scraper.get(image_url).content
        with open("temp.jpg", "wb") as f:
            f.write(img_data)
        image = Image.open("temp.jpg").convert("RGB")
        brightness = image_brightness(image)
        if brightness < brightness_threshold:
            image.save('scraped_image.jpg')
            return 'scraped_image.jpg'


# ─────────────────────────────────────────────
#  PLACEMENT HELPERS
# ─────────────────────────────────────────────

def boxes_overlap(box1, box2):
    """Return True if two (x, y, w, h) boxes overlap."""
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return not (
        x1 + w1 <= x2 or
        x2 + w2 <= x1 or
        y1 + h1 <= y2 or
        y2 + h2 <= y1
    )
##3 Checks to see if two boxes overlap, boxes have an x y width and height
# Checks to see if the boxes are separated, if they are its returning false by return not
def find_non_overlapping_position(bg_w, bg_h, fg_w, fg_h, existing_boxes, max_tries=1000):
    """Find a random position for a foreground image that doesn't overlap existing boxes."""
    for _ in range(max_tries):
        x = random.randint(0, max(0, bg_w - fg_w))
        y = random.randint(0, max(0, bg_h - fg_h))
        new_box = (x, y, fg_w, fg_h)
        if all(not boxes_overlap(new_box, b) for b in existing_boxes):
            return x, y
            ### Finding positions with the background and foreground width and heights
    #and checking to see if new X and Y variables are within this existinf boxes list. 
    # for the bboxes in eexsisting boxes if they dont overallap we return the new x and y.
    return None


# ─────────────────────────────────────────────
#  WHITE BACKGROUND REMOVAL
# ─────────────────────────────────────────────

def remove_white_background(img, threshold=200):
    """Convert white and near-white pixels to transparent."""
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    for r, g, b, a in data:
        if r > threshold and g > threshold and b > threshold:
            new_data.append((r, g, b, 0))  # transparent
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    return img


# ─────────────────────────────────────────────
#  STEGANOGRAPHY — BIT MERGING
# ─────────────────────────────────────────────

def merge_pixel(bg_val, hidden_val):
    bg_top     = bg_val & 0b11111000      # keep top 5 bits of background
    hidden_bot = (hidden_val & 0b11100000) >> 5  # only top 3 bits of hidden
    return bg_top | hidden_bot

def blend_hidden_onto_background(background, hidden_img, position):
    """
    Steganographically embed a hidden image into the background at (x, y).
    Transparent pixels in the hidden image are skipped.
    Modifies background in place.
    """
    hidden_img = hidden_img.convert("RGBA")
    x_off, y_off = position
    fg_w, fg_h = hidden_img.size
    for x in range(fg_w):
        for y in range(fg_h):
            bx, by = x + x_off, y + y_off
            if bx >= background.size[0] or by >= background.size[1]:
                continue
            r1, g1, b1 = background.getpixel((bx, by))
            r2, g2, b2, a2 = hidden_img.getpixel((x, y))
            if a2 == 0:
                continue  # skip transparent pixels
            background.putpixel((bx, by), (
                merge_pixel(r1, r2),
                merge_pixel(g1, g2),
                merge_pixel(b1, b2)
            ))


# ─────────────────────────────────────────────
#  REVEAL — EXTRACT HIDDEN BITS ON WRONG GUESS
# ─────────────────────────────────────────────

def reveal_step(original_blended, wrong_guesses):
    """
    Progressively reveal hidden images by extracting their bits from the background.
    The more wrong guesses, the more the hidden images emerge.
      wrong_guesses=0 → background fully visible, hidden images invisible
      wrong_guesses=4 → hidden images fully apparent
    """
    fade = wrong_guesses / 4.0
    result = original_blended.copy()
    width, height = original_blended.size

    for x in range(width):
        for y in range(height):
            r, g, b = original_blended.getpixel((x, y))

            # Extract background (top 4 bits) and hidden image (bottom 4 bits)
            bg_r = r & 0b11110000
            bg_g = g & 0b11110000
            bg_b = b & 0b11110000

            # Repeat the 4 hidden bits into both halves for full 8-bit color range
            hid_r = (r & 0b00001111) << 4 | (r & 0b00001111)
            hid_g = (g & 0b00001111) << 4 | (g & 0b00001111)
            hid_b = (b & 0b00001111) << 4 | (b & 0b00001111)

            # Lerp: fade=0 → background only, fade=1 → hidden image fully visible
            final_r = int(bg_r * (1 - fade) + hid_r * fade)
            final_g = int(bg_g * (1 - fade) + hid_g * fade)
            final_b = int(bg_b * (1 - fade) + hid_b * fade)

            result.putpixel((x, y), (final_r, final_g, final_b))

    return result


# ─────────────────────────────────────────────
#  REVEAL CORRECT — PASTE ORIGINAL AT ITS POSITION
# ─────────────────────────────────────────────

def reveal_correct(original_blended, correct_item, images_dir, item_positions):
    """
    On a correct guess, paste the full original image at the exact position
    it was steganographically embedded at.
    """
    img_path = f"{images_dir}/{correct_item['image']}"
    img = Image.open(img_path).convert("RGBA")
    result = original_blended.copy()
    bg_w, bg_h = result.size

    # Resize the same way it was resized during embedding
    target_width = bg_w // 4
    w, h  = img.size
    scale = min(1.0, target_width / w)
    img   = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    x, y = item_positions[correct_item["name"]]
    result.paste(img, (x, y), img)  # use alpha channel as mask
    result.save("gameboard.jpg")
    result.show()


# ─────────────────────────────────────────────
#  HINT DISPLAY
# ─────────────────────────────────────────────

def show_hints(target_item: dict, wrong_guesses: int):
    """Print hints for the target item, revealing one more per wrong guess."""
    print("\n── Hints ──────────────────────────────")
    revealed = target_item["hints"][:wrong_guesses + 1]
    locked   = ["???"] * (4 - wrong_guesses - 1)
    hint_str = " | ".join(revealed + locked)
    print(f"  {hint_str}")
    print("────────────────────────────────────────\n")


# ─────────────────────────────────────────────
#  MAIN COMPOSE + GAME LOOP
# ─────────────────────────────────────────────

def compose_and_play(csv_path: str, images_dir: str = "."): # why specify that they're strings?
    # 1. Load all items from CSV, pick 5 at random to embed
    all_items = load_items_from_csv(csv_path)
    selected  = random.sample(all_items, min(5, len(all_items)))
    target    = random.choice(selected)

    # 2. Scrape and load background
    bg_path    = bg_im()
    background = Image.open(bg_path).convert("RGB")
    bg_w, bg_h = background.size

    # 3. Load, remove white background, resize, and steganographically embed all 5 images
    placed_boxes   = []
    loaded_items   = []
    item_positions = {}

    for item in selected:
        img_path = f"{images_dir}/{item['image']}"
        try:
            img = Image.open(img_path).convert("RGBA")
            img = remove_white_background(img)
        except FileNotFoundError:
            print(f"Warning: could not find {img_path}, skipping.")
            continue

        target_width = bg_w // 4
        w, h  = img.size
        scale = min(1.0, target_width / w)
        img   = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

        fg_w, fg_h = img.size
        pos = find_non_overlapping_position(bg_w, bg_h, fg_w, fg_h, placed_boxes)
        if pos is None:
            print(f"Warning: no room for {item['name']}, skipping.")
            continue

        placed_boxes.append((pos[0], pos[1], fg_w, fg_h))
        blend_hidden_onto_background(background, img, pos)
        loaded_items.append(item)
        item_positions[item["name"]] = pos

    if not loaded_items:
        print("No images could be loaded. Exiting.")
        return

    if target not in loaded_items:
        target = random.choice(loaded_items)

    # 4. Freeze the blended image for use as the reveal base
    original_blended = background.copy()
    original_blended.save("gameboard.jpg")
    print("\nInitial blended image saved as gameboard.jpg")

    # 5. Game loop — user guesses the target item, hidden images revealed on wrong guesses
    wrong_guesses = 0

    print(f"\nCan you find the hidden image?")
    print("Hidden images will emerge with each wrong guess.\n")

    while wrong_guesses <= 4:
        current_image = reveal_step(original_blended, wrong_guesses)
        current_image.save("gameboard.jpg")
        current_image.show()

        show_hints(target, wrong_guesses)

        if wrong_guesses == 4:
            print(f"Out of guesses! The hidden item was: '{target['name']}'")
            reveal_correct(original_blended, target, images_dir, item_positions)
            break

        guess = input("Guess the hidden object: ").strip().lower()

        if guess == target["name"].lower():
            print(f"✓ Correct! You found the '{target['name']}'!")
            reveal_correct(original_blended, target, images_dir, item_positions)
            break
        else:
            wrong_guesses += 1
            print(f"✗ Wrong! ({wrong_guesses}/{4} wrong guesses)")


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    compose_and_play(
        csv_path="hints.csv",
        images_dir="img_sized",
    )
