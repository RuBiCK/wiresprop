pipeline {
  agent any
  stages {
    stage('error') {
      steps {
        sh '''#!/bin/bash
date
echo "Jenkins build"'''
      }
    }
  }
  environment {
    environment = 'DEV'
  }
}