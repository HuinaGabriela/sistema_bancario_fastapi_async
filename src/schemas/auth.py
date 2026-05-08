from pydantic import BaseModel, Field

class LoginIn(BaseModel):
    # user_id: str = Field(..., min_length=11)
    cpf: str
    senha: str

class LoginOut(BaseModel):
    access_token: str
