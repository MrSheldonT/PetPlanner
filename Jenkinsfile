pipeline {
    agent any

    stages {
        stage('Checkout repository') {
            steps {
                checkout scm
            }
        }

        stage('Load .env file') {
            steps {
                sh 'rm -f .env'
                withCredentials([file(credentialsId: 'env-file', variable: 'ENV_FILE')]) {
                    sh 'cat $ENV_FILE > .env'
                }
            }
        }

        stage('Build and Run Containers') {
            steps {
                script {
                    sh 'docker compose down -v'
                    sh 'docker compose up -d --build'
                }
            }
        }

        stage('Wait for services') {
            steps {
                sh 'sleep 15'
            }
        }

        stage('Test API REST') {
            steps {
                sh 'docker exec petplanner-web-1 pytest'
            }
        }

        stage('Push web image to dockerhub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'dockerhubPassword', usernameVariable: 'dockerhubUser')]) {
                    sh 'docker login -u $dockerhubUser -p $dockerhubPassword'
                    sh 'docker tag petplanner-web:latest $dockerhubUser/petplanner-web:1.0'
                    sh 'docker push $dockerhubUser/petplanner-web:1.0'
                }
            }
        }
    }

    post {
        always {
            sh 'docker compose down -v'
            sh 'docker container prune -f'
        }
    }
}
