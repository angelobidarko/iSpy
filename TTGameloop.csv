# ── Data ────────────────────────────────────────────────────────────────────
Hints = {}

def load_data(filepath="Hints.csv"):
    """Load the CSV into Hints dict. Each entry's hints list:
       index 0 → list of colors
       index 1 → hint 1
       index 2 → hint 2
       index 3 → hint 3
    """
    if not os.path.exists(filepath):
        print(f"Error: Could not find '{filepath}'.")
        return False

    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            Hints[i] = {
                "Names": row["Names"],
                "image": row["image"],          # ← image filename e.g. "butterfly_resized.jpg"
                "hints": [
                    row["h0"].split(","),   # index 0 → colors e.g. ["black", "white"]
                    row["h1"],              # index 1 → hint 1
                    row["h2"],              # index 2 → hint 2
                    row["h3"],              # index 3 → hint 3
                ]
            }
    return True


# ── Game logic ───────────────────────────────────────────────────────────────
def play_entry(entry):
    """Play one round, revealing one hint at a time until correct or out of hints."""
    colors = ", ".join(entry["hints"][0])
    print(f"\n🔍 I spy with my computer eyes something... [{colors}]")

    for hint_index in range(1, len(entry["hints"])):
        hint = entry["hints"][hint_index]
        guess = input(f"   Hint {hint_index}: {hint}\n   Your guess: ").strip()

        if guess.lower() == entry["Names"].strip().lower():
            print(f"   ✅ Correct! It was: {entry['Names']}")
            print(f"   🖼️  Image: {entry['image']}\n")
            return True
        else:
            if hint_index < len(entry["hints"]) - 1:
                print("   ❌ Wrong! Here's another hint...")
            else:
                print(f"   ❌ Out of hints! The answer was: {entry['Names']}")
                print(f"   🖼️  Image: {entry['image']}\n")
    return False


def play_game():
    """Pick one random entry and play a single round."""
    if not Hints:
        print("No hints loaded. Check your CSV file.")
        return

    print("=" * 45)
    print("          🕵️  I SPY — COMPUTER EDITION 🕵️")
    print("=" * 45)

    index = random.randint(0, len(Hints) - 1)
    entry = Hints[index]
    correct = play_entry(entry)

    print("=" * 45)
    if correct:
        print("  🎉 You got it!")
    else:
        print("  Better luck next time!")
    print("=" * 45)


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if load_data("Hints.csv"):
        play_game()
