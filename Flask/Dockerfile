# 使用基于Ubuntu的官方Python Docker镜像作为基础镜像
FROM ubuntu:20.04

# 设置时区为东八区（中国时间）
ENV TZ=Asia/Shanghai

# 更换apt源为清华大学镜像源
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list \
    && sed -i 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

# 更新apt并安装系统依赖，包括Python、pip、gcc和python3-dev
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    gcc \
    python3-dev \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libgl1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

# 设置pip镜像源为清华大学镜像源
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 将工作目录设置为/app
WORKDIR /app

# 将当前目录下的所有文件复制到容器的工作目录中
COPY . .

# 安装Python依赖
RUN pip3 install --no-cache-dir -r requirements.txt

# 暴露应用程序的端口（如果有必要）
EXPOSE 5000

# 定义容器启动时运行的命令
CMD ["python3", "app.py"]
