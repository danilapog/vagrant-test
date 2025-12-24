pipeline {
    agent none
    options {
       disableConcurrentBuilds()
       buildDiscarder (logRotator(numToKeepStr: '2', artifactNumToKeepStr: '2'))
    }
  parameters {
    gitParameter  name: 'PIPELINE_BRANCH', 
      type: 'PT_BRANCH',
      branchFilter: '.*',
      listSize: '5',
      defaultValue: '*/master',
      selectedValue: 'DEFAULT',
      sortMode: 'ASCENDING_SMART',
      description: 'Select branch name to pipeline'
    gitParameter  name: 'API_BRANCH', 
      type: 'PT_BRANCH',
      useRepository: 'https://github.com/danilapog/vagrant-test.git',
      branchFilter: '.*',
      listSize: '10',
      defaultValue: '*/master',
      selectedValue: 'DEFAULT',
      sortMode: 'ASCENDING_SMART',
      description: 'Select branch name to build'
    gitParameter  name: 'FRONT_BRANCH', 
      type: 'PT_BRANCH',
      useRepository: 'https://github.com/danilapog/vagrant-test.git',
      branchFilter: '.*',
      listSize: '10',
      defaultValue: '*/master',
      selectedValue: 'DEFAULT',
      sortMode: 'ASCENDING_SMART',
      description: 'Select branch name to build'
    choice(name: 'MODE', choices: ['build','update'], description: 'Set mode. BUILD new image for hub.docker or UPDATE admin-panel in production')
    choice(name: 'API_BUILD', choices: ['false','true'],description: 'Do you want build API?')
    choice(name: 'FRONT_BUILD', choices: ['false','true'],description: 'Do you want build FRONT?')
    string(name: 'API_VERSION', defaultValue: '', description: 'OPTIONAL: Specify image tag (if empty, will be used last pushed version. For example last was 1.0.0-rc3, new will be 1.0.0-rc4)')
    string(name: 'API_RC', defaultValue: '', description: 'OPTIONAL: Specify new rc number (if empty, will be set automaticaly. For example last was rc3 > new will be rc4)')
    string(name: 'FRONT_VERSION', defaultValue: '', description: 'OPTIONAL: Specify image tag (if empty, will be set automaticaly. For example last was 1.0.0-rc3, new will be 1.0.0-rc4)')
    string(name: 'FRONT_RC', defaultValue: '', description: 'OPTIONAL: Specify new rc number (if empty, will be set automaticaly. For example last was rc3 > new will be rc4)')
    choice(name: 'Execute', choices: ['false','true'],description: 'Execute? Set to "True" to run, or "False" to update job')
  }
  stages {
    stage('Build-->') {
	parallel {
	   stage ('Build api') {
	    when { 
		    allOf {expression { return env.Execute == "true" }; expression { return env.API_BUILD == "true" } } 
	    } 
      steps {
          sh '''
	        echo "api"
          '''
      }
	      post {
		always {
	  sh '''
          echo "Wipe docker: logout and prune all data"
		    '''
		}
	      }
	    }
	stage ('Build front') {
	    when { 
		    allOf {expression { return env.Execute == "true" }; expression { return env.FRONT_BUILD == "true" } } 
	    } 
      steps {
          sh '''#!/bin/bash
	        echo "front"
          '''
      }
	  post {
	    always { 
		sh '''#!/bin/bash
               echo "Wipe docker: logout and prune all data"
	       '''
	    }
          }
	}
      }
	}
     stage('Post step-->') {
      when {
        allOf {
          expression { return env.Execute == "true" }
          anyOf {
            expression { return env.API_BUILD == "true" }
            expression { return env.FRONT_BUILD == "true" }
          }
        }
      }
      steps {
        {
        sh '''#!/bin/bash
          echo "123"
        '''
      }
    }
    }
   }
}
