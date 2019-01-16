pipeline {
    environment {
        registry = "linea/qlf"
        registryCredential = 'Dockerhub'
        dockerImage = ''
    }
    agent any

    stages {
        stage('Build') {
            steps {
                sh './configure.sh ci'
                dir('frontend') {
                    sh 'yarn install'
                }
            }
        }
        stage('Test Frontend') {
            steps {
                dir('frontend') {
                    sh 'yarn lint'
                    sh 'yarn test'
                }
            }
        }
        stage('Build Images') {
            when {
                expression {
                   env.BRANCH_NAME.toString().equals('master')
                }
            }
            steps {
              parallel(
              frontend: {
                  dir('frontend') {
                      script {
                          dockerImage = docker.build registry + ":FRONT$GIT_COMMIT"
                          docker.withRegistry( '', registryCredential ) {
                          dockerImage.push()
                      }
                        sh "docker rmi $registry:FRONT$GIT_COMMIT --force"
                      }
                  }
              },
              backend: {
                  dir('backend') {
                      script {
                          dockerImage = docker.build registry + ":BACK$GIT_COMMIT"
                          docker.withRegistry( '', registryCredential ) {
                          dockerImage.push()
                      }
                        sh "docker rmi $registry:BACK$GIT_COMMIT --force"
                      }
                  }
              }
          )
        }
      }
    }
}
