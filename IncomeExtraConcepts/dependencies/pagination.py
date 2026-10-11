from fastapi import Query

def pagination_parameters(
        page : int = Query(1,ge=1),
        page_size : int = Query (3,ge=1)
):
    return {
        "page" : page,
        "page_size " : page_size
    }