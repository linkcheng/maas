# """
# 用户模块

# 这是一个使用FastAPI和SQLAlchemy 2.0实现的用户管理模块，基于领域驱动设计(DDD)的思想构建。
# 实现了用户的CRUD操作，以及登录、登出、修改密码等功能。
# 使用JWT+OAuth2实现认证，支持单点登录。
# """

# from .api.router import router as user_router
# from .application.services import UserService
# from .domain.entities import User
# from .domain.value_objects import Password, UserCredentials, UserProfile

# __all__ = [
#     'user_router',
#     'UserService',
#     'User',
#     'Password',
#     'UserCredentials',
#     'UserProfile',

# ]

