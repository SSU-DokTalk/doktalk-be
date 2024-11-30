import os
import requests

from app.core.config import settings
from app.enums import PROVIDER
from app.oauth.oauthSchema import oAuthLoginInfo


KAKAO_CLIENT_ID = settings.KAKAO_CLIENT_ID
KAKAO_CLIENT_SECRET = settings.KAKAO_CLIENT_SECRET
GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
NAVER_CLIENT_ID = settings.NAVER_CLIENT_ID
NAVER_CLIENT_SECRET = settings.NAVER_CLIENT_SECRET
FACEBOOK_CLIENT_ID = settings.FACEBOOK_CLIENT_ID
FACEBOOK_CLIENT_SECRET = settings.FACEBOOK_CLIENT_SECRET


def auth_kakao(code: str, redirect_uri: str):
    try:
        # request access token to kakao
        token_url = f"https://kauth.kakao.com/oauth/token?client_id={KAKAO_CLIENT_ID}&client_secret={KAKAO_CLIENT_SECRET}&code={code}&grant_type=authorization_code&redirect_uri={redirect_uri}/kakao"
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
    except Exception as e:
        print(e)
        raise Exception("Kakao auth error")

    info = user_response.json()
    return oAuthLoginInfo(
        uid=str(info.get("id")),
        name=info.get("kakao_account").get("profile").get("nickname"),
        email=info.get("kakao_account").get("email"),
        profile=info.get("kakao_account").get("profile").get("profile_image_url"),
        provider=PROVIDER.KAKAO.name,
    )


def auth_google(code: str, redirect_uri: str):
    try:
        # request access token to google
        token_url = f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}&client_secret={GOOGLE_CLIENT_SECRET}&code={code}&grant_type=authorization_code&redirect_uri={redirect_uri}/google"
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
    except Exception as e:
        print(e)
        raise Exception("Google auth error")

    info = user_response.json()
    return oAuthLoginInfo(
        uid=str(info.get("id")),
        name=info.get("name"),
        email=info.get("email"),
        profile=info.get("picture"),
        provider=PROVIDER.GOOGLE.name,
    )


def auth_naver(code: str, redirect_uri: str, state: str):
    try:
        # request access token to naver
        token_url = f"https://nid.naver.com/oauth2.0/token?client_id={NAVER_CLIENT_ID}&client_secret={NAVER_CLIENT_SECRET}&code={code}&grant_type=authorization_code&state={state}"
        token_response = requests.post(token_url)
        if token_response.status_code != 200:
            raise Exception

        # request user info
        access_token = token_response.json()["access_token"]
        user_info = f"https://openapi.naver.com/v1/nid/me"
        headers = {"Authorization": "Bearer " + access_token}
        user_response = requests.post(user_info, headers=headers)
        if user_response.status_code != 200:
            raise Exception
    except Exception as e:
        print(e)
        raise Exception("naver oauth error")

    info = user_response.json()
    return oAuthLoginInfo(
        uid=info.get("response").get("id"),
        name=info.get("response").get("nickname"),
        email=info.get("response").get("email"),
        profile=info.get("response").get("profile_image"),
        provider=PROVIDER.NAVER.name,
    )


def auth_facebook(code: str, redirect_uri: str):
    try:
        # request user access token to facebook
        token_url = f"https://graph.facebook.com/v21.0/oauth/access_token?client_id={FACEBOOK_CLIENT_ID}&redirect_uri={redirect_uri}/facebook&client_secret={FACEBOOK_CLIENT_SECRET}&code={code}"
        token_response = requests.get(token_url)
        if token_response.status_code != 200:
            raise Exception

        # request user info
        access_token = token_response.json()["access_token"]
        user_info_url = f"https://graph.facebook.com/me?access_token={access_token}&fields=id,name,email,picture"
        user_info_response = requests.get(user_info_url)
        if user_info_response.status_code != 200:
            raise Exception
    except Exception as e:
        print(e)
        raise Exception("facebook oauth error")

    info = user_info_response.json()
    return oAuthLoginInfo(
        uid=info.get("id"),
        name=info.get("name"),
        email=info.get("email"),
        profile=info.get("picture").get("data").get("url"),
        provider=PROVIDER.FACEBOOK.name,
    )
