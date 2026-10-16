from fastapi import APIRouter, Cookie, Response, HTTPException, status,Header

router = APIRouter(
    prefix="/cookies",
    tags=["Cookies"]
)

@router.post("/preferences")
def set_preference(response: Response):
    response.set_cookie(
        key="currency",
        value="INR",
        max_age=3600,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )
    return {
        "message": "Currency preference cookie created",
        "currency": "INR"
    }


@router.get("/preferences")
def get_preference(currency: str | None = Cookie(default=None)):
    if currency is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Currency cookie not found. Set it first."
        )
    return {
        "currency": currency
    }


@router.delete("/preferences")
def delete_preference(response: Response):
    response.delete_cookie(key="currency",path="/")
    return {
        "message": "Currency preference cookie deleted"
    }

@router.get("/response")
def response_header(response: Response):
    response.headers["X-App-Name"] = "Income Management API"
    return {
        "message": "Custom response header added"
    }
