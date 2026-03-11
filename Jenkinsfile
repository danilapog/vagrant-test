pipeline {
  agent none
  parameters {
    string(name: 'version', defaultValue: '99.99.99', description: 'Package version')
    string(name: 'build',   defaultValue: '1',        description: 'Package build')
  }
  stages {
    stage('Test') {
      steps {
        node('built-in') {
          echo "Waiting for cleanup stage..."
        }
      }
    }
  }
  post {
    cleanup {
      node('built-in') {
        ghaDocsTest()
        deleteDir()
      }
    }
  }
}

void ghaDocsTest() {
  ghaWorkflowRun(
    'danilapog/vagrant-test',
    'Docs-CI.yaml',
    'master',
    [
      'version': params.version,
      'build':   params.build
    ]
  )
}

void ghaWorkflowRun(
  String repo, String workflow, String ref = 'master', Map fields = [:]
) {
  ArrayList args = [workflow, "--repo", repo, "--ref", ref]
  fields.each { key, value ->
    args += ["--raw-field", key + "=" + value]
  }

  withCredentials([
    string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')
  ]) {
    sh label: "GITHUB ACTION: ${repo} - ${workflow}", script: """
      gh workflow run ${args.join(' ')}
    """
  }
}
