from string import ascii_letters

from fastapi import HTTPException
from pydantic import BaseModel, field_validator


class UserSchema(BaseModel):
    name: str
    password: str
    telegram_id: int

    @field_validator('name')
    def name_v(value: str):

        if len(value) > 32:
            raise HTTPException(
                status_code=400,
                detail='username cannot be longer than 32 symbols'
            )
        elif len(value) < 4:
            raise HTTPException(
                status_code=400,
                detail='username cannot be shorter than 4 symbols'
            )
        
        for s in value:
            if (s not in ascii_letters) and (s != ' '):
                raise HTTPException(
                    status_code=400,
                    detail='username can only containt ASCII letters (a-z) and spaces'
                )

        return value
