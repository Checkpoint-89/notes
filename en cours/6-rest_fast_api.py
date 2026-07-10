"""
FastAPI fournit surtout :
- le routage
- la lecture et la conversion des données de la requête
- la validation des entrées
- la sérialisation des réponses
- la génération automatique de la documentation OpenAPI

L'application est créée avec :
app = FastAPI()

Le routage est déclaré par un décorateur, par exemple :
@app.get("/route/path", response_model=ModelOut, status_code=200)

Les paramètres et le body sont décrits dans la signature :
def route_handler(input: ModelIn, offset: int = Query(ge=0)):
    ...

Les dépendances sont injectées via Depends().
"""
import time
from itertools import count, islice
from collections import defaultdict
from fastapi import FastAPI, Request, Response, Query, Path, Depends, APIRouter
from fastapi.responses import JSONResponse
from  pydantic import BaseModel, Field
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

VALID_TOKENS = {"secret-token-1": "alice", "secret-token-2": "bob"}

app = FastAPI()
router_v1 = APIRouter(prefix="/v1")
router_v2 = APIRouter(prefix="/v2")
app.include_router(router_v1)
app.include_router(router_v2)

counter = count(1)
bib = {}
id2key = {}
http_requests=defaultdict(list)

security = HTTPBearer(auto_error=False) # Pour désactiver 403 par defaut si Header absent.

def rate_limiter(request: Request, window=60, max_requests=10):
    cur_time = time.time()
    ip = request.client.host
    recent = [t for t in http_requests[ip] if cur_time - t < window]
    if len(recent) >= max_requests:
        raise RateError()
    recent.append(cur_time)
    http_requests[ip] = recent
    

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if credentials is None:
        raise TokenNotFound()
    token = credentials.credentials
    if token not in VALID_TOKENS:
        raise TokenNotFound()
    return VALID_TOKENS[token]


class BookToInsert(BaseModel):
    title: str
    author: str


class BookToInsertV2(BookToInsert):
    status: str = Field(default="pending")


class BookInBib(BaseModel):
    id: int
    title: str
    author: str


class BookInBibV2(BookInBib):
    status: str = Field(default="pending")


class BookList(BaseModel):
    total: int
    offset: int
    limit: int
    items: list[BookInBib]


class BookListV2(BookList):
    items: list[BookInBibV2]


class BookNotFound(Exception):
    pass


class TokenNotFound(Exception):
    pass


class RateError(Exception):
    pass


async def _handle(request, exc):
    if isinstance(exc, BookNotFound):
        return JSONResponse(status_code=404, content={"error": "Book not found"})
    elif isinstance(exc, TokenNotFound):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    elif isinstance(exc, RateError):
        return JSONResponse(status_code=429, content={"error": "Too many requests"})
    else:
        raise Exception("Unknwon error")
app.add_exception_handler(BookNotFound, _handle)
app.add_exception_handler(TokenNotFound, _handle)
app.add_exception_handler(RateError, _handle)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
    

def _insert_book(title: str, author: str, id: int, status: str = "pending") -> BookInBibV2:
    key = f"{title}-{author}"
    book = BookInBibV2(id=id, title=title, author=author, status=status)
    bib[key] = book
    id2key[id] = key
    return book

def _create_book(
    book: BookToInsertV2,
    response: Response,
):
    key = f"{book.title}-{book.author}"
    if not key in bib:
        response.status_code = 201
        return _insert_book(book.title, book.author, book.status, next(counter))
    else: 
        response.status_code = 200
        return bib[key]

@router_v1.post("/books", response_model=BookInBib,)
def create_book_v1(book: BookToInsert, response: Response, _=Depends(verify_token), __=Depends(rate_limiter)):
    return _create_book(BookToInsertV2(**book.model_dump()), response)
    
@router_v2.post("/books", response_model=BookInBibV2,)
def create_book_v2(book: BookToInsertV2, response: Response, _=Depends(verify_token), __=Depends(rate_limiter)):
    return _create_book(book, response)


def _get_book_list(
    offset: int,
    limit: int,
):
    items = list(islice(bib.values(), offset, offset + limit))
    return {
        "total": len(bib),
        "offset": offset,
        "limit": limit,
        "items": items
    }

@router_v1.get("/books", response_model=BookList,)
def get_book_list_v1(
    offset: int=Query(default=0, ge=0),
    limit: int=Query(default=10, ge=1, le=100),
    __ = Depends(rate_limiter),
):
    return _get_book_list(offset, limit)

@router_v2.get("/books", response_model=BookListV2,)
def get_books_list_v2(
    offset: int=Query(default=0, ge=0),
    limit: int=Query(default=10, ge=1, le=100),
    __ = Depends(rate_limiter),
):
    return _get_book_list(offset, limit)


def _get_book(id: int):
    if id not in id2key:
        raise BookNotFound()
    key = id2key[id]
    return bib[key]

@router_v1.get("/books/{id}", response_model=BookInBib)
def get_book_v1(id: int, __ = Depends(rate_limiter)):
    return _get_book(id)

@router_v2.get("/books/{id}", response_model=BookInBibV2)
def get_book_v2(id: int, __ = Depends(rate_limiter)):
    return _get_book(id)


def _update_book(
    id: int, 
    book: BookToInsertV2, 
):
    if id not in id2key:
        raise BookNotFound()
    key = id2key[id]
    id2key.pop(id, None)
    bib.pop(key, None)
    return _insert_book(book.title, book.author, book.status, id)

@router_v1.put("/books/{id}",
    response_model=BookInBib,
    summary="Update a book",
    description="Updates book fields. If the new title/author combination matches an existing book, that entry is overwritten.")
def update_book_v1(id: int, book: BookToInsert, _=Depends(verify_token), __ = Depends(rate_limiter),):
    return _update_book(id, BookToInsertV2(**book.model_dump()))

@router_v2.put("/books/{id}",
    response_model=BookInBibV2,
    summary="Update a book",
    description="Updates book fields. If the new title/author combination matches an existing book, that entry is overwritten.")
def update_book_v2(id: int, book: BookToInsertV2, _=Depends(verify_token), __ = Depends(rate_limiter),):
    return _update_book(id, book)

@app.delete("/v{version}/books/{id}", status_code=204)
def delete_book(
    id: int,
    version: str = Path(pattern="^[12]$"),
    _=Depends(verify_token),
    __ = Depends(rate_limiter),
):
    if id not in id2key:
        raise BookNotFound()
    key = id2key[id]
    id2key.pop(id, None)
    bib.pop(key, None)
    return
