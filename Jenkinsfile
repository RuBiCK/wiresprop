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
    stage('Test') {
      parallel {
        stage('Test') {
          agent any
          steps {
            sleep 5
          }
        }
        stage('test2') {
          steps {
            echo 'pasando por test2'
          }
        }
      }
    }
    stage('unit test') {
      agent any
      steps {
        sh 'date'
        dir(path: '.')
      }
    }
    stage('') {
      steps {
        mail(subject: 'Asunto', body: 'cuerpo', from: 'ru@ru.gmail', to: 'rubick@gmail.com')
      }
    }
  }
  environment {
    environment = 'DEV'
  }
}