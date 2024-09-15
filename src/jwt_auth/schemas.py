from schemas.base import BaseSchemaModel


class TokenSchema(BaseSchemaModel):
    access_token: str
