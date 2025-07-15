from pydantic import BaseModel
from config.settings import settings

class ErrorCode(BaseModel):
    code: str
    message: str

# 系统/common 模块报错
INTERNAL_SERVER_ERROR = ErrorCode(code="10000", message="Internal Server Error")
NOT_AUTHENTICATED_ERROR = ErrorCode(code="10001", message="未提供认证信息")
INVALID_AUTH_SCHEMA_ERROR = ErrorCode(code="10002", message="无效认证格式")
INVALID_TOKEN_ERROR = ErrorCode(code="10003", message="无效认证")
TOKEN_EXPIRED_ERROR = ErrorCode(code="10004", message="认证已过期")
USER_NOT_ACTIVE_ERROR = ErrorCode(code="10005", message="用户未激活")
AUTHENTICATION_ERROR = ErrorCode(code="10006", message="认证失败")

# user 模块错误
USERNAME_MIN_LENGTH_ERROR = ErrorCode(code="20001", message=f"用户名长度不能小于{settings.USERS.USERNAME_MIN_LENGTH}个字符")
USERNAME_MAX_LENGTH_ERROR = ErrorCode(code="20002", message=f"用户名长度不能大于{settings.USERS.USERNAME_MAX_LENGTH}个字符")
PASSWORD_MIN_LENGTH_ERROR = ErrorCode(code="20003", message=f"密码长度不能小于{settings.USERS.PASSWORD_MIN_LENGTH}个字符")
PASSWORD_MAX_LENGTH_ERROR = ErrorCode(code="20004", message=f"密码长度不能大于{settings.USERS.PASSWORD_MAX_LENGTH}个字符")
USERNAME_EXISTS_ERROR = ErrorCode(code="20005", message=f"用户名已存在")
USER_NOT_FOUND_ERROR = ErrorCode(code="20006", message=f"用户不存在")
JWT_ERROR = ErrorCode(code="20007", message=f"无效的认证凭据")
USERNAME_PASSWORD_ERROR = ErrorCode(code="20008", message=f"用户名或密码错误")
PASSWORD_ERROR = ErrorCode(code="20009", message=f"密码错误")
USER_FORBIDDEN_ERROR = ErrorCode(code="20010", message=f"用户被禁用")