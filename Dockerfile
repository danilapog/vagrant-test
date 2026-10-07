FROM nginx:alpine as mynginx-release

ARG COMMIT_SHA
ENV COMMIT_SHA=${COMMIT_SHA}

RUN apk update && apk add --no-cache \
    curl \
    git \
    htop
    
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
