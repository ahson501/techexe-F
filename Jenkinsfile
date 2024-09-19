pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "techexeapp"  // Replace with your Docker image name
        DOCKER_COMPOSE_FILE = "docker-compose.yaml"  // Docker Compose file path

    }

    stages {
        stage('Checkout') {
            steps {
                // Correctly specify the branch (techexe-F) and repository URL
                git branch: 'techexe-F', url: 'https://github.com/ahson501/techexe-F.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image using docker-compose
                    sh 'docker-compose -f ${DOCKER_COMPOSE_FILE} build'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run Django tests within the Docker container
                    sh 'docker-compose -f ${DOCKER_COMPOSE_FILE} run web python manage.py test'
                }
            }
        }

        stage('Collect Static Files') {
            steps {
                script {
                    // Collect static files within the Docker container
                    sh 'docker-compose -f ${DOCKER_COMPOSE_FILE} run web python manage.py collectstatic --noinput'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Deploy the application
                    sh 'docker-compose -f ${DOCKER_COMPOSE_FILE} up -d'
                }
            }
        }
    }

    post {
        always {
            script {
                // Clean up containers and volumes after build
                sh 'docker-compose -f ${DOCKER_COMPOSE_FILE} down --volumes'
            }
        }

        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}
