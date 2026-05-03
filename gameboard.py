import os
import csv
import random
from PIL import Image, ImageEnhance

def load_hints():
    hints = {}
    with open('Hints.Csv', mode='r', encoding='utf-8') as f:
        # Using DictReader is cleaner if your CSV has headers
        reader = csv.DictReader(f)
        for row in reader:
           hints[row['ImageID']] = row
    return hints

def reveal_hidden(image_path, guess_count):
    """
    Makes the hidden bits more visible. 
    Level 1 (0 guesses): Original image
    Level 4 (Final guess): High contrast/stretched bits
    """
    img = Image.open(image_path)
    if guess_count == 0:
        return img
    
    # Simple trick: multiply the pixel values to bring the low 4 bits 
    # into the visible range. 
    # Since hidden bits are 0-15, multiplying by (16 * progress) 
    # pushes them into the 0-255 range.
    enhanced = img.point(lambda p: (p & 0x0F) * (guess_count * 15))
    return enhanced

def play_game():
    hints_db = load_hints()
    
    # Read the icons used in the last session from get.py
    try:
        with open("current_session.txt", "r") as f:
            selected_icons = f.read().strip().split(",")
    except FileNotFoundError:
        print("Error: current_session.txt not found. Please run get.py first!")
        return

    # Choose the target item from the ACTUAL images hidden in new.jpg
    target_file = random.choice(selected_icons)
    
    # 1. Get the ID from the filename
    target_id = target_file.replace(".jpg", "")

    # 2. Retrieve the dictionary entry FIRST
    target_data = hints_db.get(target_id)

    # 3. NOW you can safely access 'Hints' and 'DisplayName'
    if target_data:
        target_hint = target_data.get('Hints')
        target_name = target_data.get('DisplayName', "Unknown Item")
    else:
        print(f"Warning: No data found for {target_id}")
        return  
        
    color_hint = target_hint.split('(')[1].split(')')[0]
    
    print("--- Welcome to iSpy---")
    print(f"I spy something: {color_hint}") # First part of hint
    print("You have 4 guesses to find the hidden item.")
    print("With every wrong guess, you'll get a hint and the hidden images will become clearer in 'new.jpg'!")

    for attempt in range(1, 5):
        guess = input(f"\nAttempt {attempt}/4 - What do you think it is? ").strip().lower()
        
        if guess == target_name.lower():
            print(f"Correct! You found the {target_name}!")
            break
        else:
            if attempt < 4:
                print("Not quite. Revealing more detail...")
                # Update the visual for the user
                revealed_img = reveal_hidden("new.jpg", attempt)
                revealed_img.save("new.jpg") 
                # Show the next part of the hint
                hints_split = target_hint.split('"')
                if len(hints_split) > attempt * 2:
                    print(f"Hint: {hints_split[attempt * 2]}")
            else:
                print(f"Game Over! The item was: {target_name}")

if __name__ == "__main__":
    play_game()
