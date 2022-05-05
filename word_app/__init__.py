from fastapi import FastAPI

from word_app.exception import exception_2_handler


def add_word_exception_handlers(app: FastAPI):
    for exception, handler in exception_2_handler.items():
        app.add_exception_handler(exception, handler)