# 使用一个 Nginx 镜像作为基础
FROM nginx:alpine

# 将本地的静态文件复制到 Nginx 默认的静态文件目录
COPY dist/ /usr/share/nginx/html

# 暴露 Nginx 默认的端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
