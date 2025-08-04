FROM nginx:alpine as mynginx-release

RUN apk update && apk add --no-cache \
    curl \
    git \
    htop
    
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
