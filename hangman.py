"""Console Hangman game with six incorrect guesses and duplicate protection."""
import random

WORDS = ["robotics", "sensor", "python", "motor", "encoder", "circuit", "battery"]

HANGMAN_STAGES = [
    r"""
     +---+
     |   |
         |
         |
         |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
         |
         |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========""",
]


def play(word=None):
    """Play one round. Optional word parameter makes the game easy to test."""
    secret = (word or random.choice(WORDS)).lower()
    guessed = set()
    wrong = set()
    max_wrong = 6

    print("=== HANGMAN ===")
    while len(wrong) < max_wrong:
        print(HANGMAN_STAGES[len(wrong)])
        display = " ".join(letter if letter in guessed else "_" for letter in secret)
        print(f"\nWord: {display}")
        print(f"Wrong guesses ({len(wrong)}/{max_wrong}): {', '.join(sorted(wrong)) or 'none'}")

        if all(letter in guessed for letter in secret):
            print("You won! The word was:", secret)
            return True

        guess = input("Guess one letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter exactly one alphabetic letter.")
            continue
        if guess in guessed or guess in wrong:
            print("You already guessed that letter. No penalty.")
            continue
        if guess in secret:
            guessed.add(guess)
            print("Correct!")
        else:
            wrong.add(guess)
            print("Not in the word.")

    print(HANGMAN_STAGES[max_wrong])
    print(f"Game over! The word was: {secret}")
    return False


if __name__ == "__main__":
    try:
        play()
    except (EOFError, KeyboardInterrupt):
        print("\nGame ended.")
