import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_DB: str = os.getenv("DB_DB")
    DB_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}"

    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY_ID: str = os.getenv("AWS_SECRET_ACCESS_KEY_ID")
    AWS_REGION: str = os.getenv("AWS_REGION")
    AWS_S3_BUCKET_NAME: str = os.getenv("AWS_S3_BUCKET_NAME")

    KAKAO_CLIENT_ID: str = os.getenv("KAKAO_CLIENT_ID")
    KAKAO_CLIENT_SECRET: str = os.getenv("KAKAO_CLIENT_SECRET")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    NAVER_CLIENT_ID: str = os.getenv("NAVER_CLIENT_ID")
    NAVER_CLIENT_SECRET: str = os.getenv("NAVER_CLIENT_SECRET")
    FACEBOOK_CLIENT_ID: str = os.getenv("FACEBOOK_CLIENT_ID")
    FACEBOOK_CLIENT_SECRET: str = os.getenv("FACEBOOK_CLIENT_SECRET")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")


settings = Settings()

__all__ = [settings]
