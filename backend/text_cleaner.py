import re
import unicodedata


class TextCleaner:

    def remove_extra_whitespace(self, text):
        return re.sub(r"\s+", " ", text).strip()

    def remove_special_characters(self, text):
        return re.sub(r"[^\w\s.,!?]", "", text)

    def remove_headers_footers(self, text):
        lines = text.split("\n")
        return "\n".join([l for l in lines if not l.strip().isdigit()])

    def normalize_text(self, text):
        return unicodedata.normalize("NFKD", text).lower()

    def clean_text(self, text):
        if not text or not text.strip():
            return ""

        text = self.remove_headers_footers(text)
        text = self.remove_special_characters(text)
        text = self.remove_extra_whitespace(text)
        text = self.normalize_text(text)

        return text
