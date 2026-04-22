target "server" {
    target = "server"
    dockerfile = "Dockerfile"
    tags = [
           "docker.io/danilaworker/prov-docs:1.0.0"
           ]
    platforms = ["linux/amd64", "linux/arm64"]
}
