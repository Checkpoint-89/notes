if __name__ == '__main__':

    from fastapi.testclient import TestClient

    def _print_debug(response):
        print(response.status_code)
        try:
            import json
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        except Exception:
            print(response.text)
            
    client = TestClient(app, raise_server_exceptions=False)

    counter = count(1)
    bib = {}
    id2key = {}

    book1 = BookToInsert(title='mon livre', author='cedric')
    book2 = BookToInsert(title='mon livre 2', author='cedric')
    book3 = BookToInsert(title='le meilleur livre', author='georges')
    book4 = BookToInsert(title='le plus nul livre', author='georges')

    print("\ncreate")
    response = client.post("/books", json=book1.model_dump())
    _print_debug(response)
    response = client.post("/books", json=book2.model_dump())
    _print_debug(response)
    response = client.post("/books", json=book3.model_dump())
    _print_debug(response)
    response = client.post("/books", json=book3.model_dump())
    _print_debug(response)
    for b in bib.values(): print(b)

    print("\nget")
    response = client.get(
        "/books", 
        params={"offset":0, "limit":2})
    print(response.json())

    print("\nupdate")
    response = client.put("/books/3", json=book4.model_dump())
    _print_debug(response)
    for b in bib.values(): print(b)

    print("\ndelete")
    response = client.delete("/books/3")
    _print_debug(response)
    for b in bib.values(): print(b)
    response = client.delete("/books/3")
    _print_debug(response)

    print("\nerrors")
    response = client.get("/error")
    _print_debug(response)
