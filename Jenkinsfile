pipeline {
environment {
    registry = "lozog95/pass_gen_web"
    registryCredential = 'dockerhub'
  }
    agent none
    stages {
        stage("Init and test") {
        environment {
                PATH = "$PATH:/usr/local/bin"
            }
            agent {
              docker {
              image 'python:3.6.5-alpine'
              args '-u root:root'
              }
            }
            stages {
               stage('Prepare environment') {
                 steps {
                   sh 'pip install -r requirements.txt'
                 }
               }
               stage('Run unit tests') {
                 steps {
                   sh 'python -m pytest --junitxml=tests.xml -v tests/test_generator.py'
                 }
               }
            }
            post {
              always {
                junit '*.xml'
              }
            }
        }
        stage("QA: Build and deploy"){
            agent any
                    steps{
                script {
          dockerImage = docker.build registry + ":$BUILD_NUMBER"
          docker.withRegistry( '', registryCredential ) {
            dockerImage.push()
          }
        }
        sh "docker service update --image lozog95/pass_gen_web:${BUILD_NUMBER} password-web-qa"
      }
    }
    stage("QA: Testing"){
        agent {
              docker {
              image 'selenium/standalone-chrome'
              args '-u root:root'
              }
            }
         steps {
            sh '''
                apt-get update && apt-get install python3-distutils -y && apt-get install python3-pip -y
                python3 -m pip install -r requirements_tests.txt'''
            sh "python3 -m pytest -v tests/test_ui.py"
         }
    }
    stage("PRD: Deploy"){
            agent any
            input{
    message "Wykonac wdrozenie na produkcje?"
  }
                    steps{
        sh "docker service update --image lozog95/pass_gen_web:${BUILD_NUMBER} password-web"
      }
    }

    }
}


