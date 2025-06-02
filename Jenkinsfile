pipeline {
    agent any

    environment {
        DB_PASSWORD    = credentials('DB_PASSWORD')
        DB_USER        = credentials('DB_USER')
        DB_HOST        = credentials('DB_HOST')
        DB_NAME        = credentials('DB_NAME')
        SECRET_KEY     = credentials('SECRET_KEY')
        EMAIL_USER     = credentials('EMAIL_USER')
        EMAIL_PASSWORD = credentials('EMAIL_PASSWORD')
        PYTHONPATH     = credentials('PYTHONPATH')
    }

    stages {
        stage('Checkout repository') {
            steps {
                checkout scm
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

        stage('Wait for Services') {
            steps {
                sh 'sleep 10'
            }
        }

        stage('Test API REST') {
            steps {
                sh 'docker ps -a'
                sh 'docker container rm petplanner-web-1'
                sh """
                    docker run -d -p 5000:5000 --name petplanner-web-1 --network petplanner_default \\
                    --env DB_PASSWORD=${DB_PASSWORD} \\
                    --env DB_USER=${DB_USER} \\
                    --env DB_HOST=${DB_HOST} \\
                    --env DB_NAME=${DB_NAME} \\
                    --env SECRET_KEY=${SECRET_KEY} \\
                    --env EMAIL_USER=${EMAIL_USER} \\
                    --env EMAIL_PASSWORD=${EMAIL_PASSWORD} \\
                    --env PYTHONPATH=${PYTHONPATH} \\
                    petplanner-web
                """
                sh 'sleep 10'
                sh 'docker logs petplanner-web-1'
                sh 'docker exec petplanner-web-1 pytest'
            }
        }
    }

    post {
        always {
            sh 'docker stop petplanner-web-1'
            sh 'docker compose down -v'
            sh 'docker container prune -f'
        }
    }
}

