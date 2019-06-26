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
              image 'python:3.6.5-alpine'
              args '-u root:root'
              }
            }
         steps {
            sh "pip install -r requirements_tests.txt"
            sh '''
                wget -q "https://chromedriver.storage.googleapis.com/75.0.3770.90/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
                && unzip /tmp/chromedriver.zip -d /usr/bin/ \
                && rm /tmp/chromedriver.zip \
                && chmod 777 /usr/bin/chromedriver
                export QA_HOST=http://51.75.63.168:5010/
                echo $PATH
                export PATH=/usr/bin:$PATH
                echo $PATH
            '''
            sh "pytest -v tests/test_ui.py"
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


