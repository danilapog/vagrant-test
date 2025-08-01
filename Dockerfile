FROM nginx:alpine as mynginx

RUN apk update && apk add --no-cache \
    curl \
    git \
    htop
    
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
