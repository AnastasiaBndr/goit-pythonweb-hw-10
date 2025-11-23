from pydantic import BaseModel, Field, model_validator, field_validator, ConfigDict
from fastapi import HTTPException, status
from typing import Optional
from datetime import date, datetime


class ContactBase(BaseModel):
    first_name: str = Field(max_length=50)
    second_name: str = Field(max_length=50)
    email: str
    phone_number: str
    birthday: date
    additional_data: Optional[str] = None


class ContactModel(ContactBase):

    @model_validator(mode="before")
    def validate_items(cls, values):
        first_name = values.get("first_name")

        if not first_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required."
            )

        return values

    @field_validator("birthday", mode="before")
    def validate_birthday(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Birthday must be in format YYYY-MM-DD")
        return value


class ContactResponse(ContactBase):
    id: int = Field(ge=1)
    model_config = ConfigDict(from_attributes=True)


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    birthday: Optional[date] = None
    additional_data: Optional[str] = None


# USERS


class UserBase(BaseModel):
    username: str = Field(max_length=50)
    password: str = Field(max_length=8)


class UserModel(UserBase):

    @model_validator(mode="before")
    def validate_items(cls, values):
        username = values.get("username")
        password = values.get("password")

        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username and password are required.",
            )

        return values


class UserResponse(UserBase):
    id: int = Field(ge=1)
    model_config = ConfigDict(from_attributes=True)


# TOKEN


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str
