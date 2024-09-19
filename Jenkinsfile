pipeline {
    agent any

    environment {
        BRANCH_NAME = 'techexe-F'
        REPO_URL = 'https://github.com/ahson501/techexe-F.git'
    }

    stages {
        stage('Checkout') {
            steps {
                // Clone the repository
                git branch: "${BRANCH_NAME}", url: "${REPO_URL}"
            }
        }
        stage('Build') {
            steps {
                // Build your project here
                echo 'Building the project...'
                // Add commands to build your project
            }
        }
        stage('Push to Remote') {
            steps {
                // Push the build artifacts or changes to the remote repository
                echo 'Pushing changes to remote repository...'
                // Add commands to push to remote repository
                sh 'git config user.email "you@example.com"'
                sh 'git config user.name "Your Name"'
                sh 'git add .'
                sh 'git commit -m "Automated commit by Jenkins"'
                sh 'git push origin ${BRANCH_NAME}'
            }
        }
    }
    
    post {
        success {
            echo 'Build and push succeeded!'
        }
        failure {
            echo 'Build or push failed.'
        }
    }
}
