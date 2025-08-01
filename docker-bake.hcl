target "mynginx-release" {
    target = "mynginx-release"
    dockerfile = "Dockerfile"
    tags = [
           "docker.io/danilaworker/nginx-test-release:1.0.0"
           ]
    platforms = ["linux/amd64", "linux/arm64"]
}
