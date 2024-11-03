import random

# ANSI color codes
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
GRAY = "\033[1;30m"
RESET = "\033[0m"

def load_words(filename):
    """Load words from a file."""
    with open(filename, 'r') as file:
        words = [line.strip().lower() for line in file]
    return words

class WordleAI:
    def __init__(self, words):
        self.words = words
        self.possible_words = words.copy()
    
    def first_guess(self):
        """Start with a high-information word."""
        return "slate"  # Commonly chosen word to start with in Wordle
    
    def make_guess(self):
        """Select a random word from the possible words."""
        return random.choice(self.possible_words)
    
    def filter_words(self, guess, feedback):
        """
        Filter the possible words based on feedback.
        feedback: list of tuples with (char, position, color)
        - "green": correct letter in the correct place
        - "yellow": correct letter in the wrong place
        - "gray": letter not in the word
        """
        new_possible_words = []

        for word in self.possible_words:
            match = True
            for i, (char, pos, color) in enumerate(feedback):
                if color == "green" and word[pos] != char:
                    match = False
                elif color == "yellow" and (word[pos] == char or char not in word):
                    match = False
                elif color == "gray" and char in word:
                    match = False
            if match:
                new_possible_words.append(word)

        self.possible_words = new_possible_words

    def play(self, secret_word):
        """
        Simulate a game of Wordle against a hidden word.
        """
        # print("Starting Wordle AI...\n")
        guesses = []
        for attempt in range(6):
            guess = self.first_guess() if attempt == 0 else self.make_guess()
            guesses.append(guess)

            if guess == secret_word:
                self.print_colored_guess(guess, self.get_feedback(guess, secret_word))
                print(f"Solved in {attempt + 1} guesses!")
                return guesses

            feedback = self.get_feedback(guess, secret_word)
            self.print_colored_guess(guess, feedback)
            self.filter_words(guess, feedback)
        
        print("Failed to guess the word.")
        return guesses

    def get_feedback(self, guess, secret_word):
        """
        Provide feedback for each guess based on the secret word.
        - "green": letter is correct and in the correct place
        - "yellow": letter is in the word but in the wrong place
        - "gray": letter is not in the word
        """
        feedback = []
        for i, char in enumerate(guess):
            if char == secret_word[i]:
                feedback.append((char, i, "green"))
            elif char in secret_word:
                feedback.append((char, i, "yellow"))
            else:
                feedback.append((char, i, "gray"))
        return feedback

    def print_colored_guess(self, guess, feedback):
        """
        Print the guess with colors based on feedback.
        """
        colored_guess = ""
        for char, _, color in feedback:
            if color == "green":
                colored_guess += f"{GREEN}{char.upper()}{RESET} "
            elif color == "yellow":
                colored_guess += f"{YELLOW}{char.upper()}{RESET} "
            else:
                colored_guess += f"{GRAY}{char.upper()}{RESET} "
        # print(colored_guess + "\n")

if __name__ == "__main__":
    # Load words from the file
    words = load_words("words.txt")
    attepmts = 100000
    statistics = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for i in range(attepmts):
        ai = WordleAI(words)
        # Choose a random word as the "secret word" (for testing purposes)
        secret_word = random.choice(words)
        # Run the AI to play the game
        guesses = ai.play(secret_word)
        # print("Guesses made:", guesses)
        statistics[len(guesses)] += 1
    total = 0
    for guesses, count in statistics.items():
        total += guesses * count
        print(f"Guesses: {guesses} - Count: {count}")
    print("Average guesses:", total / attepmts)
