from fastapi import FastAPI, Header

app = FastAPI()


# @app.get("/check-client")
# def check_client(user_agent: str | None = Header(default=None)):
#     return {
#         "client": user_agent
#     }

from fastapi import Header, HTTPException


@app.get("/private")
def private_api(
    authorization: str | None = Header(default=None)
):
    if authorization != "Bearer demo-token":
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing token"
        )

    return {"message": "Access granted"}