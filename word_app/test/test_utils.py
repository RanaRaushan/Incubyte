import string
import random


class TestUtils:
    @staticmethod
    def get_new_word_create_response(word: str = None):
        default_word = ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))
        if not word:
            word = default_word

        word_response = {
            "word": word,
        }
        return word_response

    @staticmethod
    def get_new_updated_response(word_id: str, word: str = None):
        default_word = "updated"+''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        if not word:
            word = default_word

        word_response = {
            "id": word_id,
            "updated_word": word,
        }
        return word_response
