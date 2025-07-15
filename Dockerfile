FROM python:3.12.9

WORKDIR /app

# 设置环境变量
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 复制项目文件
COPY pyproject.toml .
COPY uv.lock .

# 安装Python依赖
RUN pip install --no-cache-dir -U pip && \
    pip install uv && \
    uv pip install --system -e .

# 复制源代码
COPY src .

# 创建非root用户并设置权限
RUN addgroup --system app && adduser --system --group app \
    && chown -R app:app /app

# 切换到非root用户
USER app

# 运行应用
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# 暴露端口
EXPOSE 8000 