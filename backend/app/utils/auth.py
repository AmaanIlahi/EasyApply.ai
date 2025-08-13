from fastapi import Request, HTTPException
#from firebase_admin import auth
import app.routes.auth

async def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if token:
        try:
            decoded_token = app.routes.auth.verify_token(request)
            print("Decoded token - ", decoded_token)
            request.state.user = decoded_token
        except:
            raise HTTPException(status_code=401, detail="Invalid auth token")
    else:
        raise HTTPException(status_code=401, detail="Missing auth token")

