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
        stage('Checkout') {
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
                sh 'sleep 15'
            }
        }

        stage('Test API REST') {
            steps {
                sh 'pytest'
            }
        }
    }
}

