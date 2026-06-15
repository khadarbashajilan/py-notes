from pydantic import BaseModel, field_validator

class AddCred(BaseModel):
    service_name:str
    username : str | None = None
    password : str 
    notes : str | None = None

    @field_validator("service_name", "password")
    @classmethod
    def check_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Field cannot be Empty")
        return v.strip()

class UpdateCred(BaseModel):
    service_name:str | None = None
    username : str | None = None
    password : str | None = None
    notes : str | None = None

    @field_validator("service_name", "password")
    @classmethod
    def check_empty(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("Field cannot be Empty")
        return v.strip() if v else v

class CredResponse(BaseModel):
    service_name:str
    username : str | None = None
    password : str 
    notes : str | None = None

