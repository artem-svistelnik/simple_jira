from typing import TypeVar

from pydantic import BaseConfig, BaseModel

ModelT = TypeVar("ModelT")


class BaseSchemaModel(BaseModel):
    class Config(BaseConfig):
        from_attributes = True

    def update_model(self, model, exclude_fields=None):
        if exclude_fields is None:
            exclude_fields = []
        for key, value in self.dict(exclude_unset=True).items():
            if key not in exclude_fields:
                setattr(model, key, value)
        return model
