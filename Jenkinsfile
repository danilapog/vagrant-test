import groovy.transform.Field

@Field Map stageStats = [:] 

// ———————————————————————— helpers ————————————————————————
void setStageStats(int status, String stageName = env.STAGE_NAME) {
  stageStats[stageName] = status
}

pipeline {
  agent any
  environment {
    COMPANY_NAME = 'ONLYOFFICE'
    BUILD_VERSION = "9.1.0"
    BUILD_NUMBER = "45"
  }
  parameters {
    booleanParam(name: 'server_ee', defaultValue: true,  description: 'Edition EE')
    booleanParam(name: 'server_de', defaultValue: false, description: 'Edition DE')

    booleanParam(name: 'linux_x86_64_ok', defaultValue: true,  description: 'Consider x86_64 like success')
    booleanParam(name: 'linux_aarch64_ok', defaultValue: true, description: 'Consider aarch64 like success')

    string(name: 'branch_name', defaultValue: 'develop', description: 'ref for gh')
    string(name: 'tag',         defaultValue: '9.1.0.1', description: 'build tag')
    string(name: 'version',     defaultValue: '9.1.0-1',  description: 'version для workflow')

    booleanParam(name: 'docs_utils',       defaultValue: true,  description: 'build utils')
    booleanParam(name: 'docs_balancer',    defaultValue: true,  description: 'build balancer')
    booleanParam(name: 'docs_non_plugins', defaultValue: false, description: 'build non-plugins')
  }

  stages {
    stage('Simulate Linux x86_64') {
      steps {
        script {
          setStageStats(params.linux_x86_64_ok ? 0 : 2, 'Linux x86_64')
          echo "Linux x86_64 status = ${stageStats['Linux x86_64']}"
        }
      }
    }

    stage('Simulate Linux aarch64') {
      steps {
        script {
          setStageStats(params.linux_aarch64_ok ? 0 : 2, 'Linux aarch64')
          echo "Linux aarch64 status = ${stageStats['Linux aarch64']}"
        }
      }
    }

    stage('Trigger Docker-Docs workflow') {
      steps {
        script {
          buildDockerDocs()
        }
      }
    }
  }
}

void buildDockerDocs() {

  if (!(stageStats['Linux x86_64'] == 0 || stageStats['Linux aarch64'] == 0))
    return
  if (!(params.server_ee || params.server_de))
    return
  try {
    String edition = [
      params.server_ee ? 'ee' : null,
      params.server_de ? 'de' : null
    ].findAll { it }.join(',')

    // платформы — по факту статусов этапов (как в buildDocker)
    boolean amd64 = (stageStats['Linux x86_64'] == 0)
    boolean arm64 = (stageStats['Linux aarch64'] == 0)

    withCredentials([
      string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')
    ]) {
      sh label: 'DOCKER DOCS BUILD', script: """
        repo=danilapog/Docker-Docs
        ref='release/v9.1.0'
        gh workflow run build.yaml \
          --repo \$repo \
          --ref \$ref \
          -f amd64=${stageStats['Linux x86_64'] == 0} \
          -f arm64=${stageStats['Linux aarch64'] == 0} \
          -f edition='${edition}' \
          -f docs-utils=true \
          -f docs-balancer=true \
          -f docs-non-plugins=false \
          -f tag=\$BUILD_VERSION.\$BUILD_NUMBER \
          -f version=\$BUILD_VERSION-\$BUILD_NUMBER \
          -f package-url='s3' \
          -f test-repo=false
      """
    }
  } catch (err) {
    echo err.toString()
    stageStats['Linux Docker Docs'] = 2
  } finally {
    if (!stageStats['Linux Docker-Docs']) stageStats['Linux Docker-Docs'] = 0
  }
}
