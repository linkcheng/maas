import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml


def get_config_path(env: Optional[str] = None) -> str:
    
    # 优先从CONFIG_PATH环境变量中获取
    config_path = os.environ.get("CONFIG_PATH")
    if config_path:
        return config_path
    
    # 从项目根目录下的config目录中获取
    root_dir = get_project_root()
    config_dir = root_dir / "config"
    
    # 如果存在特定环境的配置文件，则使用它
    env_config_path = config_dir / f"config.{env}.yaml"
    if env_config_path.exists():
        return env_config_path
    
    # 否则使用默认配置文件
    default_config_path =config_dir / "config.yaml"
    if default_config_path.exists():
        return default_config_path
    
    raise FileNotFoundError(f"配置文件不存在: {default_config_path}")


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    if config_path is None:
        config_path = get_config_path()
    return load_yaml_config(config_path)


def get_project_root() -> Path:
    """获取项目根目录"""
    return Path(__file__).parent.parent


def load_yaml_config(file_path: str|Path) -> Dict[str, Any]:
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

