import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.text_cleaner import TextCleaner


def test_text_cleaning():
    raw_text = """
    PAGE 1

    This    is   a    SAMPLE   text!!!
    $$$ With special ### characters ###
    """

    cleaner = TextCleaner()
    cleaned_text = cleaner.clean_text(raw_text)

    print("----- BEFORE -----")
    print(raw_text)

    print("\n----- AFTER -----")
    print(cleaned_text)


if __name__ == "__main__":
    test_text_cleaning()
