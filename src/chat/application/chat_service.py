from typing import List, Optional, Tuple, Dict, Any, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from ..domain.models.chat import (
    ChatEntity, 
    ChatDataEntity, 
    ChatToolEntity,
    SourceEntity,
    PromptEntity,
    ChatToolConfig
)
from ..domain.models.enums import ContentType, PromptType, Role
from ..domain.services.chat_service import ChatDomainService
from ..domain.services.llm_service import LLMDomainService
from ...infra.database import UnitOfWork
from ..infrastructure.repositories import (
    ChatRepository,
    ChatDataRepository,
    ChatToolRepository,
    SourceRepository,
    PromptRepository,
    ToolRepository
)

class ChatApplicationService:
    """聊天应用服务，协调领域服务和仓储"""
    
    def __init__(
        self, 
        mcp_server_url: str, 
        model: str, 
        api_key: str, 
        api_base: str
    ):
        self.mcp_server_url = mcp_server_url
        self.model = model
        self.api_key = api_key
        self.api_base = api_base
    
    def _create_chat_domain_service(self, session: AsyncSession) -> ChatDomainService:
        """创建聊天领域服务"""
        chat_repo = ChatRepository(session)
        chat_data_repo = ChatDataRepository(session)
        chat_tool_repo = ChatToolRepository(session)
        source_repo = SourceRepository(session)
        prompt_repo = PromptRepository(session)
        
        return ChatDomainService(
            chat_repo=chat_repo,
            chat_data_repo=chat_data_repo,
            chat_tool_repo=chat_tool_repo,
            source_repo=source_repo,
            prompt_repo=prompt_repo
        )
    
    def _create_llm_domain_service(self, session: AsyncSession) -> LLMDomainService:
        """创建LLM领域服务"""
        chat_domain_service = self._create_chat_domain_service(session)
        
        return LLMDomainService(
            mcp_server_url=self.mcp_server_url,
            model=self.model,
            api_key=self.api_key,
            api_base=self.api_base,
            chat_domain_service=chat_domain_service
        )
    
    async def create_chat(
        self, 
        session: AsyncSession,
        name: str,
        user_id: int,
        source_id: int,
        extra: Optional[Dict[str, Any]] = None
    ) -> Tuple[ChatEntity, Optional[ChatDataEntity]]:
        """
        创建聊天会话
        
        Args:
            session: 数据库会话
            name: 聊天名称
            user_id: 用户ID
            source_id: 源ID
            extra: 额外参数
            
        Returns:
            聊天实体和可能的欢迎消息
        """
        chat_service = self._create_chat_domain_service(session)
        return await chat_service.create_chat(
            name=name,
            user_id=user_id,
            source_id=source_id,
            extra=extra
        )
    
    async def send_message(
        self,
        session: AsyncSession,
        chat_id: str,
        message_content: str
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        发送消息
        
        Args:
            session: 数据库会话
            chat_id: 聊天ID
            message_content: 消息内容
            
        Yields:
            响应内容
        """
        chat_service = self._create_chat_domain_service(session)
        llm_service = self._create_llm_domain_service(session)
        
        # 获取聊天实体
        chat = await chat_service.get_chat_by_chat_id(chat_id)
        if not chat:
            return
        
        # 创建用户消息
        await chat_service.create_message(
            chat_id=chat.id,
            content=message_content,
            role=Role.USER
        )
        
        # 获取聊天历史
        messages = await chat_service.get_messages(chat_id)
        
        # 与LLM对话
        async for response in llm_service.chat(chat, messages):
            yield response
    
    async def create_chat_tool(
        self,
        session: AsyncSession,
        chat_id: str,
        tool_id: int,
        parameters: Dict[str, Any]
    ) -> ChatToolEntity:
        """
        为聊天添加工具
        
        Args:
            session: 数据库会话
            chat_id: 聊天ID
            tool_id: 工具ID
            parameters: 参数
            
        Returns:
            聊天工具实体
        """
        chat_service = self._create_chat_domain_service(session)
        
        # 获取聊天实体
        chat = await chat_service.get_chat_by_chat_id(chat_id)
        if not chat:
            return None
        
        # 创建聊天工具
        return await chat_service.create_tool(
            chat_id=chat.id,
            tool_id=tool_id,
            parameters=parameters
        )
    
    async def list_messages(
        self,
        session: AsyncSession,
        chat_id: str
    ) -> List[ChatDataEntity]:
        """
        获取聊天消息列表
        
        Args:
            session: 数据库会话
            chat_id: 聊天ID
            
        Returns:
            聊天消息列表
        """
        chat_service = self._create_chat_domain_service(session)
        return await chat_service.get_messages(chat_id)
    
    async def list_user_chats(
        self,
        session: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[ChatEntity]:
        """
        获取用户的所有聊天
        
        Args:
            session: 数据库会话
            user_id: 用户ID
            skip: 跳过条数
            limit: 限制条数
            
        Returns:
            聊天列表
        """
        chat_repo = ChatRepository(session)
        return await chat_repo.get_chats_by_user(user_id, skip, limit)
    
    # 源、提示词、工具相关方法也可以类似实现 