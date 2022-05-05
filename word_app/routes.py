
from fastapi import APIRouter, Depends, Request, Form
from starlette import status
from starlette.responses import RedirectResponse

import main
from word_app.schemas import WordCreate
from word_app.words import get_word_manager, WordManager

router = APIRouter()


@router.post("/create", name="Word:create")
async def create_word(request: Request, word: str = Form(...), word_manager: WordManager = Depends(get_word_manager)):
    await word_manager.create(WordCreate(word=word))
    return RedirectResponse(url="/word", status_code=status.HTTP_302_FOUND)


@router.get("/word", status_code=status.HTTP_200_OK, name="Word:get all")
async def create_word(request: Request, word_manager: WordManager = Depends(get_word_manager)):
    word_schema_list = await word_manager.get_all_word()
    return main.templates.TemplateResponse('HomePage.html', context={'request': request,
                                                                     'wordList': word_schema_list})


@router.get("/word/update", status_code=status.HTTP_200_OK, name="Word:update")
async def update_word(request: Request, id: int):
    return main.templates.TemplateResponse('update_word.html', context={'request': request, "word_id": id})


@router.post("/word/update", status_code=status.HTTP_200_OK, name="Word:update")
async def update_word(request: Request, updated_word: str = Form(...), id: str = Form(...),
                      word_manager: WordManager = Depends(get_word_manager)):
    await word_manager.update(int(id), WordCreate(word=updated_word))
    return RedirectResponse(url="/word", status_code=status.HTTP_302_FOUND)


@router.post("/word/delete/{word_id}", status_code=status.HTTP_200_OK, name="Word:delete")
async def delete_word(request: Request, word_id: str, word_manager: WordManager = Depends(get_word_manager)):
    await word_manager.delete(int(word_id))
    return RedirectResponse(url="/word", status_code=status.HTTP_302_FOUND)

