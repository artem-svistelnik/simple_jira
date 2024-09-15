from dependency_injector.wiring import Provide

from fastapi import APIRouter
from containers.users import UserDI
from jwt_auth.auth_handler import create_access_token
from jwt_auth.schemas import TokenSchema
from routes.depends import get_service
from schemas.user_schemas import LoginSchema
from schemas.user_schemas import SignUpSchema, UserSchema
from services.user_service import UserService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/sign-up", response_model=UserSchema)
async def sign_up(
    user_dta: SignUpSchema, service: UserService = get_service(Provide[UserDI.service])
):
    user = await service.create_user(user_dta)
    return UserSchema.from_orm(user)


@auth_router.post("/login", response_model=TokenSchema)
async def login(
    login_dta: LoginSchema, service: UserService = get_service(Provide[UserDI.service])
):
    user = await service.authenticate_user(login_dta)
    token = create_access_token(data={"user_id": user.id, "role": user.role.value})
    return TokenSchema(access_token=token)
