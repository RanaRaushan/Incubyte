from enum import Enum

from fastapi import Request
from starlette import status
from fastapi.responses import JSONResponse


class WordException(Exception):
    pass


class WordNotFoundException(WordException):
    pass


async def word_doesnt_exists_handler(request: Request, exc: WordNotFoundException):
    return JSONResponse(content={"error_type": ErrorCode.WORD_NOT_FOUND},
                        status_code=status.HTTP_401_UNAUTHORIZED)


class ErrorCode(str, Enum):
    WORD_NOT_FOUND = "WORD_NOT_FOUND"


exception_2_handler = {
    WordNotFoundException: word_doesnt_exists_handler,
}
