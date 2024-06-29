import re
from collections import defaultdict

class SpamFilter:
    def __init__(self):
        self.spam_words = defaultdict(int)
        self.ham_words = defaultdict(int)
        self.spam_emails = 0
        self.ham_emails = 0

    def train(self, email, is_spam):
        words = self._extract_words(email)
        if is_spam:
            self.spam_emails += 1
            for word in words:
                self.spam_words[word] += 1
        else:
            self.ham_emails += 1
            for word in words:
                self.ham_words[word] += 1

    def classify(self, email):
        words = self._extract_words(email)
        spam_prob = self._calculate_probability(words, self.spam_words, self.spam_emails)
        ham_prob = self._calculate_probability(words, self.ham_words, self.ham_emails)
        return spam_prob > ham_prob

    def _extract_words(self, email):
        return re.findall(r'\b\w+\b', email.lower())

    def _calculate_probability(self, words, word_counts, total_emails):
        prob = 1.0
        for word in words:
            word_prob = (word_counts[word] + 1) / (total_emails + 2)  # Laplace smoothing
            prob *= word_prob
        return prob * (total_emails / (self.spam_emails + self.ham_emails))

# Example usage
spam_filter = SpamFilter()

# Training
spam_filter.train("Get rich quick! Buy now!", True)
spam_filter.train("Hello, how are you?", False)
spam_filter.train("Claim your prize money now!", True)
spam_filter.train("Meeting at 3 PM tomorrow", False)

# Testing
with open('spam.txt', 'r') as file:
    content = file.readline()
    is_spam = spam_filter.classify(content)
    print(f"The email '{content}' is classified as: {'Spam' if is_spam else 'Not Spam'}")