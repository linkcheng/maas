from datetime import datetime

from fastapi import status
from typing import Union, Optional, Literal, Any
from pydantic import BaseModel


class ResponseBase(BaseModel):

    code: int = 200
    err_msg: Optional[str] = None
    status: str = "success"
    model_config = {    
        "json_encoders": {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }
    }


class ResponseModel(ResponseBase):
    data: Any = None


class PaginationResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: list


class ResponseBuilder:
    @classmethod
    def success(cls, *, data: Any = None, code: int = status.HTTP_200_OK) -> ResponseModel:
        return ResponseModel(code=code, status="success", data=data)

    @classmethod
    def failure(cls, *, err_msg: Optional[str] = None, code: int = status.HTTP_500_INTERNAL_SERVER_ERROR) -> ResponseModel:
        return ResponseModel(code=code, status="failure", err_msg=err_msg)

    @classmethod
    def pagination(cls, total: int, page: int, limit: int, data: list):
        pagination_data = PaginationResponse(
            total=total,
            page=page,
            limit=limit,
            data=data
        )
        return ResponseBuilder.success(data=pagination_data.model_dump())
