pipeline {
  agent any

  environment {
    BRANCH_NAME = "release/v9.1.0"
    BUILD_NUMBER = "195"
    BUILD_VERSION = "99.99.99"
  }

  stages {
    stage('Build') {
      parallel {
        stage('Linux x86_64') {
          steps {
            echo "=== START Linux x86_64 build (stub) ==="
            sleep time: 3, unit: 'SECONDS'
            echo "=== Linux x86_64 build complete ==="
          }
          post {
            success {
              echo "Post success for x86_64"
              node('built-in') { script { ghaDocsDockerArm64() } }
            }
          }
        }

        stage('Linux aarch64') {
          steps {
            echo "=== START Linux aarch64 build (stub) ==="
            sleep time: 5, unit: 'SECONDS'
            echo "=== Linux aarch64 build complete ==="
          }
          post {
            success {
              echo "Post success for aarch64"
              node('built-in') { script { ghaDocsDockerArm64() } }
            }
          }
        }
      }
    }
  }
}

void ghaDocsDockerAmd64() {
  echo ">>> [ghaDocsDockerAmd64] AMD64..."
  try {
    withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
      sh label: 'DOCKER DOCS BUILD AMD64', script: """
        repo=danilapog/Docker-DocumentServer
        gh workflow run 4testing-build.yml \
          --repo \$repo \
          --ref \$BRANCH_NAME \
          -f build=\$BUILD_NUMBER \
          -f amd64=${stageStats['Linux x86_64'] == 0} \
          -f community=${params.server_ce} \
          -f enterprise=${params.server_ee} \
          -f developer=${params.server_de}
      """
    }
  } catch (err) {
    echo err.toString()
  }
  echo ">>> [ghaDocsDockerAmd64] Done!"
}

void ghaDocsDockerArm64() {
  echo ">>> [ghaDocsDockerArm64] ARM64..."
  try {
    withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
      sh label: 'DOCKER DOCS BUILD ARM64', script: """
        repo=danilapog/Docker-DocumentServer
        gh workflow run 4testing-build.yml \
          --repo \$repo \
          --ref \$BRANCH_NAME \
          -f build=\$BUILD_NUMBER \
          -f arm64=${stageStats['Linux aarch64'] == 0} \
          -f community=${params.server_ce} \
          -f enterprise=${params.server_ee} \
          -f developer=${params.server_de}
      """
    }
  } catch (err) {
    echo err.toString()
  }
  echo ">>> [ghaDocsDockerArm64] Done!"
}
