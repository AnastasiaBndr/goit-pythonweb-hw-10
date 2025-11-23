class Config:
    DB_URL = "postgresql+asyncpg://admin:admincontacts@localhost:5432/contacts_db"
    JWT_SECRET="Keyyyya"
    JWT_ALGORITHM="HS256"
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
    ACCESS_TOKEN_EXPIRE_MINUTES = 15

config = Config
