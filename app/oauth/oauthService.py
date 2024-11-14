import os
import requests
from app.oauth.oauthSchema import *

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")
KAKAO_CALLBACK_URI = os.getenv("OAUTH_REDIRECT_URI") + "/kakao"

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_CALLBACK_URI = os.getenv("OAUTH_REDIRECT_URI") + "/google"


def auth_kakao(code: str):
    try:
        # request access token to kakao
        token_url = f"https://kauth.kakao.com/oauth/token?client_id={KAKAO_CLIENT_ID}&client_secret={KAKAO_CLIENT_SECRET}&code={code}&grant_type=authorization_code&redirect_uri={KAKAO_CALLBACK_URI}"
        headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}
        token_response = requests.post(token_url, headers=headers)
        if token_response.status_code != 200:
            raise Exception

        # request user info
        access_token = token_response.json()["access_token"]
        user_info = f"https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        user_response = requests.post(user_info, headers=headers)
        if user_response.status_code != 200:
            raise Exception
    except:
        raise Exception("Kakao auth error")

    info = user_response.json()
    return oAuthLoginInfo(
        uid=info.get("id"),
        name=info.get("kakao_account").get("profile").get("nickname"),
        email=info.get("kakao_account").get("email"),
        profile=info.get("kakao_account").get("profile").get("profile_image_url"),
        provider=PROVIDER.KAKAO.name,
    )


def auth_google(code: str):
    try:
        # request access token to google
        token_url = f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}&client_secret={GOOGLE_CLIENT_SECRET}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}"
        token_response = requests.post(token_url)
        if token_response.status_code != 200:
            raise Exception

        # request user info
        access_token = token_response.json()["access_token"]
        user_info = (
            f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}"
        )
        user_response = requests.get(user_info)
        if user_response.status_code != 200:
            raise Exception
    except:
        raise Exception("Google auth error")

    info = user_response.json()
    return oAuthLoginInfo(
        uid=info.get("id"),
        name=info.get("name"),
        email=info.get("email"),
        profile=info.get("picture"),
        provider=PROVIDER.GOOGLE.name,
    )
