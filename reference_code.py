import random
from pathlib import Path

# Find the folder where this script is saved
script_dir = Path(__file__).parent

# Build full path to eff_large_wordlist.txt
file_path = script_dir / "eff-large-wordlist.txt"

words = []

# Read the word list (right column only)
with open(file_path, "r") as file:
    for line in file:
        # Split each line into index and word
        parts = line.split()

        # Ensure the line contains at least two elements
        if len(parts) >= 2:
            words.append(parts[1])

# Alternative one-liner using a list comprehension:
# words = [line.split()[1] for line in file if len(line.split()) >= 2]

# Create a cryptographically secure random generator
secure_random = random.SystemRandom()

# Select 6 unique random words without modifying the list
selected_words = secure_random.sample(words, 6)

# Join the words with spaces for a human-friendly passphrase
passphrase = " ".join(selected_words)

# Output the generated passphrase
print(passphrase)
