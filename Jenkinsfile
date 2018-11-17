pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        sh '''#!/bin/bash
date
echo "Jenkins build"'''
        echo 'Mensaje'
      }
    }
  }
  environment {
    environment = 'DEV'
  }
}