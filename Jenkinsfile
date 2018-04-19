pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                dir('frontend') {
                    sh 'yarn install'
                }
            }
        }
        stage('Test') {
            steps {
                dir('frontend') {
                    sh 'yarn lint'
                    sh 'yarn test'
                }
            }
        }
        stage('Deploy') {
            steps {
                sh 'curl -D - -X "POST" -H "Accept: application/json" \
                    -H "Content-Type: application/json" \
                    -H "X-Rundeck-Auth-Token: $RD_AUTH_TOLEN" \
                    http://fox.linea.gov.br:4440/api/16/job/0430ff97-56fb-4bb4-b323-6f870bf3af94/executions'
            }
        }
    }
}
