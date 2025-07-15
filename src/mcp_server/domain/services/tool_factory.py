"""
工具工厂 - 创建和管理工具实体
"""
from typing import Dict, Any, List, Callable, Set, Optional, Type
import logging
from functools import wraps

from ..models.tool import ToolEntity

logger = logging.getLogger(__name__)

class ToolRegistry:
    """工具注册表 - 管理所有可用工具"""
    _tools: Dict[str, Type[ToolEntity]] = {}
    
    @classmethod
    def register(cls, name: str, description: str = "", tags: List[str] = None):
        """工具注册装饰器"""
        logger.info(f"注册工具: {name}")
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            tool = ToolEntity(
                name=name,
                description=description,
                function=wrapper,
                tags=tags or []
            )
            cls._tools[name] = tool
            return wrapper
        return decorator
    
    @classmethod
    def get_tool(cls, name: str) -> Optional[ToolEntity]:
        """获取指定工具"""
        return cls._tools.get(name)
    
    @classmethod
    def get_all_tools(cls) -> List[ToolEntity]:
        """获取所有工具"""
        return list(cls._tools.values())
    
    @classmethod
    def get_tools_by_tag(cls, tag: str) -> List[ToolEntity]:
        """根据标签获取工具"""
        return [tool for tool in cls._tools.values() if tag in tool.tags]
