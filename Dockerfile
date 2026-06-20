FROM python:3.14-slim

WORKDIR /app

# 安装系统依赖（adbutils 底层依赖 adb，这里只装运行库）
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY pyproject.toml uv.lock* ./
RUN pip install --no-cache-dir adbutils>=2.12.0

# 复制源码
COPY main.py .

# 默认环境变量：通过 host.docker.internal 连接宿主机 ADB
ENV ADB_HOST=host.docker.internal
ENV ADB_PORT=5037

CMD ["python", "main.py"]