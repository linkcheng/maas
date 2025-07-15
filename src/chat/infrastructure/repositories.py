from typing import List, Optional, Dict, Any, TypeVar, Generic, Type
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.repositories.chat_repository import (
    IChatRepository, 
    IChatDataRepository, 
    IChatToolRepository,
    ISourceRepository,
    IPromptRepository,
    IToolRepository
)
from ...domain.models.chat import (
    ChatEntity, 
    ChatDataEntity, 
    ChatToolEntity,
    SourceEntity,
    PromptEntity,
    ChatToolConfig
)
from .models import Chat, ChatData, ChatTool, Source, Prompt, Tool

# 类型变量，用于泛型
T = TypeVar('T')
M = TypeVar('M')

class BaseRepository(Generic[T, M]):
    """基础仓储，提供基础的CRUD操作"""
    
    def __init__(self, session: AsyncSession, entity_class: Type[T], model_class: Type[M]):
        self.session = session
        self.entity_class = entity_class
        self.model_class = model_class
    
    def _to_entity(self, model: M) -> T:
        """将ORM模型转换为领域实体"""
        if not model:
            return None
        
        # 获取模型的所有属性
        attrs = {}
        for key in self.entity_class.__annotations__.keys():
            if hasattr(model, key):
                attrs[key] = getattr(model, key)
        
        return self.entity_class(**attrs)
    
    def _to_model(self, entity: T) -> M:
        """将领域实体转换为ORM模型"""
        if not entity:
            return None
        
        # 如果已有ID，则查询现有模型
        if getattr(entity, 'id', None):
            model = self.model_class()
            for key, value in entity.__dict__.items():
                if hasattr(model, key):
                    setattr(model, key, value)
            return model
        
        # 创建新模型
        attrs = {}
        for key, value in entity.__dict__.items():
            if hasattr(self.model_class, key):
                attrs[key] = value
        
        return self.model_class(**attrs)

class ChatRepository(BaseRepository[ChatEntity, Chat], IChatRepository):
    """聊天仓储实现"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, ChatEntity, Chat)
    
    async def create_chat(self, chat: ChatEntity) -> ChatEntity:
        """创建聊天"""
        model = self._to_model(chat)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)
    
    async def get_chat(self, chat_id: int) -> Optional[ChatEntity]:
        """根据ID获取聊天"""
        stmt = select(Chat).where(Chat.id == chat_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model)
    
    async def get_chat_by_chat_id(self, chat_id: str) -> Optional[ChatEntity]:
        """根据chat_id获取聊天"""
        stmt = select(Chat).where(Chat.chat_id == chat_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model)
    
    async def get_chats_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[ChatEntity]:
        """获取用户的所有聊天"""
        stmt = select(Chat).where(
            and_(Chat.user_id == user_id, Chat.is_deleted == False)
        ).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
    
    async def update_chat(self, chat: ChatEntity) -> ChatEntity:
        """更新聊天"""
        stmt = select(Chat).where(Chat.id == chat.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            for key, value in chat.__dict__.items():
                if hasattr(model, key) and key != 'id':
                    setattr(model, key, value)
            
            await self.session.flush()
            await self.session.refresh(model)
            return self._to_entity(model)
        
        return None
    
    async def delete_chat(self, chat_id: int) -> bool:
        """删除聊天(软删除)"""
        stmt = select(Chat).where(Chat.id == chat_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            model.is_deleted = True
            await self.session.flush()
            return True
        
        return False

class ChatDataRepository(BaseRepository[ChatDataEntity, ChatData], IChatDataRepository):
    """聊天数据仓储实现"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, ChatDataEntity, ChatData)
    
    async def create_chat_data(self, chat_data: ChatDataEntity) -> ChatDataEntity:
        """创建聊天数据"""
        model = self._to_model(chat_data)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)
    
    async def get_chat_data(self, chat_id: int, skip: int = 0, limit: int = 100) -> List[ChatDataEntity]:
        """获取聊天数据"""
        stmt = select(ChatData).where(
            ChatData.chat_id == chat_id
        ).order_by(ChatData.created_at).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

class ChatToolRepository(BaseRepository[ChatToolEntity, ChatTool], IChatToolRepository):
    """聊天工具仓储实现"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, ChatToolEntity, ChatTool)
    
    async def create_chat_tool(self, chat_tool: ChatToolEntity) -> ChatToolEntity:
        """创建聊天工具"""
        model = self._to_model(chat_tool)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)
    
    async def get_chat_tools(self, chat_id: int) -> List[ChatToolEntity]:
        """获取聊天工具"""
        stmt = select(ChatTool).where(ChatTool.chat_id == chat_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

class SourceRepository(BaseRepository[SourceEntity, Source], ISourceRepository):
    """源仓储实现"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, SourceEntity, Source)
    
    async def create_source(self, source: SourceEntity) -> SourceEntity:
        """创建源"""
        model = self._to_model(source)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)
    
    async def get_source(self, source_id: int) -> Optional[SourceEntity]:
        """获取源"""
        stmt = select(Source).where(Source.id == source_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model)
    
    async def get_sources(self, skip: int = 0, limit: int = 100) -> List[SourceEntity]:
        """获取所有源"""
        stmt = select(Source).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
    
    async def update_source(self, source: SourceEntity) -> SourceEntity:
        """更新源"""
        stmt = select(Source).where(Source.id == source.id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            for key, value in source.__dict__.items():
                if hasattr(model, key) and key != 'id':
                    setattr(model, key, value)
            
            await self.session.flush()
            await self.session.refresh(model)
            return self._to_entity(model)
        
        return None
    
    async def delete_source(self, source_id: int) -> bool:
        """删除源"""
        stmt = select(Source).where(Source.id == source_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        
        return False

class PromptRepository(BaseRepository[PromptEntity, Prompt], IPromptRepository):
    """提示词仓储实现"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, PromptEntity, Prompt)
    
    async def create_prompt(self, prompt: PromptEntity) -> PromptEntity:
        """创建提示词"""
        model = self._to_model(prompt)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)
    
    async def get_prompt(self, prompt_id: int) -> Optional[PromptEntity]:
        """获取提示词"""
        stmt = select(Prompt).where(Prompt.id == prompt_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model)
    
    async def get_prompts_by_source(self, source_id: int, skip: int = 0, limit: int = 100) -> List[PromptEntity]:
        """获取源的所有提示词"""
        stmt = select(Prompt).where(
            Prompt.source_id == source_id
        ).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

class ToolRepository(BaseRepository[ChatToolConfig, Tool], IToolRepository):
    """工具仓储实现"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, ChatToolConfig, Tool)
    
    async def create_tool(self, tool: ChatToolConfig) -> ChatToolConfig:
        """创建工具"""
        model = self._to_model(tool)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)
    
    async def get_tool(self, tool_id: int) -> Optional[ChatToolConfig]:
        """获取工具"""
        stmt = select(Tool).where(Tool.id == tool_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model)
    
    async def get_tools_by_source(self, source_id: int, skip: int = 0, limit: int = 100) -> List[ChatToolConfig]:
        """获取源的所有工具"""
        stmt = select(Tool).where(
            Tool.source_id == source_id
        ).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models] 