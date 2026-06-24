pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Build Started'
            }
        }

        stage('Test') {
            steps {
                echo 'Testing Application'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t flask-app .'
            }
        }

        stage('Deploy Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
            }
        }
    }
}