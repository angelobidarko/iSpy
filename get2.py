import cloudscraper
import random
import string
from io import BytesIO
from PIL import Image, ImageFilter
import difflib
from nltk.corpus import wordnet as wn

# ---------- Helper functions for matching ----------

def get_lemmas(word):
    """Return a set of lemma names (synonyms) for a word from WordNet."""
    word = word.lower()
    lemmas = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            lemmas.add(lemma.name().replace("_", " ").lower())
    return lemmas

def similar_enough(a, b, threshold=0.8):
    """
    Fuzzy similarity between two strings using difflib.
    threshold in [0,1]; higher = stricter.
    """
    a = a.lower()
    b = b.lower()
    if not a or not b:
        return False
    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    return ratio >= threshold

def words_match(guess_word, description_words, shown_words):
    """
    Return True if guess_word matches a description word or its synonyms,
    provided it hasn't been used as a hint already.
    """
    guess_word = guess_word.lower().strip()
    if not guess_word:
        return False
    
    # 1. Create a set of "forbidden" words (synonyms of words already hinted)
    # This prevents the user from guessing a word that the game already told them.
    forbidden_words = set()
    for shown in shown_words:
        shown_lower = shown.lower()
        forbidden_words.add(shown_lower)
        # Use your existing get_lemmas function
        forbidden_words.update(get_lemmas(shown_lower))

    # If the user guessed a word that is already a hint (or a synonym of one), reject it
    if guess_word in forbidden_words:
        return False

    # 2. Check if the guess matches any description word or its synonyms
    for desc_word in description_words:
        desc_word = desc_word.lower()
        
        # Don't check against description words that are already shown
        if desc_word in shown_words:
            continue
            
        # Get all acceptable synonyms for this description word
        acceptable_synonyms = get_lemmas(desc_word)
        acceptable_synonyms.add(desc_word)
        
        # Check for exact match in synonyms or direct word
        if guess_word in acceptable_synonyms:
            return True
            
        # Check for fuzzy match against the description word itself
        # Note: Ensure your similar_enough function accepts the 'threshold' argument
        if similar_enough(guess_word, desc_word):
            return True
            
    return False

# ---------- Fetch data and image ----------
scraper = cloudscraper.create_scraper()
response = scraper.get("https://randomwordgenerator.com/json/pictures.json")
response.raise_for_status()
data = response.json()

# Pick an item that actually has a description
while True:
    random_image = random.choice(data["data"])
    full_description = random_image.get("description", "").strip()
    if full_description:
        break

# Clean description for matching guesses
clean_description = full_description.lower().translate(
    str.maketrans('', '', string.punctuation)
)
description_words = clean_description.split()
if not description_words:
    description_words = ["object"]

# Download image
image_url = "https://randomwordgenerator.com/img/picture-generator/" + random_image["image_url"]
img_resp = scraper.get(image_url)
img_resp.raise_for_status()
img_data = img_resp.content

# Keep the original (clear) image ONLY in memory
base_img = Image.open(BytesIO(img_data)).convert("RGB")

# This file will ALWAYS be the current blurred image
IMAGE_FILE = "guess_image.jpg"

# ---------- Hint / game setup ----------
hint_words = full_description.split()          # words to reveal
description_length = len(hint_words)           # number of words
revealed_hint = []
game_won = False

print("--- Welcome to iSpy Progressive Reveal! ---")
print(f"(Description length: {description_length} words)")

# Max guesses = description_length - 1 (at least 1)
max_guesses = max(1, description_length - 1)

while True:
    try:
        user_guesses = int(input(f"How many guesses do you want? (max {max_guesses}): "))
        if user_guesses <= 0:
            print("Please choose at least 1 guess.")
            continue
        break
    except ValueError:
        print("Please enter a valid number.")

if user_guesses > max_guesses:
    print(f"You chose {user_guesses}, but the maximum allowed is {max_guesses}.")
    user_guesses = max_guesses

print(f"You have {user_guesses} guesses. With each guess, guess_image.jpg will get clearer and you'll get one more hint word.")

# ---------- Image blur settings ----------
max_blur = 10  # blurry start
min_blur_during_game = 3  # still a little blur on the last guess

# We go from max_blur down to min_blur_during_game over user_guesses turns
if user_guesses == 1:
    blur_step = 0
else:
    blur_step = (max_blur - min_blur_during_game) / (user_guesses - 1)

# ---------- Game loop ----------
for turn in range(user_guesses):
    # Reveal next hint word if any left
    if turn < len(hint_words):
        revealed_hint.append(hint_words[turn])

    # Compute blur for this turn
    current_blur = max_blur - blur_step * turn
    current_blur = max(min_blur_during_game, current_blur)

    # Apply blur and overwrite guess_image.jpg
    blurred_img = base_img.filter(ImageFilter.GaussianBlur(radius=current_blur))
    blurred_img.save(IMAGE_FILE)

    print(f"\nGuess {turn + 1} of {user_guesses}")
    print(f"Current hint: {' '.join(revealed_hint)}...")
    print(f"(Open '{IMAGE_FILE}' to see the current blurred image.)")

    guess = input("What is it? ").strip().lower()
    guess_clean = guess.translate(str.maketrans('', '', string.punctuation))
    guess_words = guess_clean.split()

    # Words already revealed in the hint (normalized)
    shown_words = [
        w.lower().translate(str.maketrans('', '', string.punctuation))
        for w in revealed_hint
    ]

    # 1) Block guesses that are already in the hint
    if any(gw in shown_words for gw in guess_words):
        print("You can't guess a word that's already been revealed in the hint!")
        continue

    # 2) Win if ANY guessed word matches/synonym/fuzzy-matches a description word
    if any(words_match(gw, description_words, shown_words) for gw in guess_words):
        print(f"Correct! It was: {full_description}")
        game_won = True
        break
    else:
        print("Not quite, try again.")

# ---------- After the game: reveal the fully clear image ----------
base_img.save(IMAGE_FILE)
print(f"\nThe image is now fully revealed in '{IMAGE_FILE}'.")

if not game_won:
    print("Out of guesses!")
    print(f"The correct answer was: {full_description}")
