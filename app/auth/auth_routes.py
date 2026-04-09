from authlib.integrations.starlette_client import OAuth

from fastapi import APIRouter, Request

from app.settings import settings


oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration"
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/google")
async def auth_google(request: Request):
    return await oauth.google.authorize_redirect(
        request, redirect_uri=f"{request.base_url}auth/google/callback")


@router.get("/google/callback")
async def google_auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get("userinfo")
    print("token: ", token)
    print("user_info: ", user)
    if user:
        request.session["user"] = dict(user)
    return {"user": user}