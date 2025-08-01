target "mynginx" {
    target = "mynginx"
    dockerfile = "Dockerfile"
    tags = [
           "docker.io/danilaworker/nginx-test:1.0.0"
           ]
    platforms = ["linux/amd64", "linux/arm64"]
}
