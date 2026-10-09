from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.models import Role


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=3, max_length=120)
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).lower().strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not any(char.isupper() for char in value) or not any(char.islower() for char in value) or not any(char.isdigit() for char in value):
            raise ValueError("La contraseña debe incluir mayúscula, minúscula y número.")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).lower().strip()


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=10, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, value: str) -> str:
        if not any(char.isupper() for char in value) or not any(char.islower() for char in value) or not any(char.isdigit() for char in value):
            raise ValueError("La contraseña debe incluir mayúscula, minúscula y número.")
        return value


class UserRoleUpdateRequest(BaseModel):
    role: Role


class CustomerCreate(BaseModel):
    full_name: str = Field(min_length=3, max_length=120)
    email: EmailStr
    phone: str = Field(min_length=8, max_length=25)


class EntityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int

class RoleDefinitionRequest(BaseModel):
    name: str = Field(min_length=3, max_length=60)
    description: str | None = Field(default=None, max_length=250)

class RoleStatusRequest(BaseModel):
    status: bool

class WorkshopRequest(BaseModel):
    name: str = Field(min_length=3, max_length=160)
    rfc: str = Field(min_length=12, max_length=13, pattern=r"^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$")
    email: EmailStr
    street_number: str = Field(min_length=3, max_length=180)
    neighborhood: str = Field(min_length=2, max_length=100)
    postal_code: str = Field(pattern=r"^\d{5}$")
    state: str = Field(min_length=2, max_length=80)
    municipality: str = Field(min_length=2, max_length=100)
    photo_url: str | None = Field(default=None, max_length=500)

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str = Field(min_length=20, max_length=200)
    new_password: str = Field(min_length=10, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: str
    role: Role
    is_active: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

