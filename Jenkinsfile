pipeline {
    agent any

    environment {
        DOCKERHUB_REPO = 'walaahijazi/scores-flask-server'
        COMPOSE_PROJECT_NAME = 'scores-flask-server'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git credentialsId: 'my_secret_token',
                    url: 'https://github.com/WalaaHijazi1/WorldGame-Project.git',
                    branch: 'main'
            }
        }

        stage('Build and Start Services') {
            steps {
                script {
                    // Build using Docker's compose plugin
                    sh 'docker compose build'
                    
                    // Start services in detached mode
                    sh 'docker compose up -d --wait app selenium-hub chrome'
                }
            }
        }

        stage('Run E2E Tests') {
            steps {
                script {
                    docker.image('python:3.8-slim').inside("--network ${COMPOSE_PROJECT_NAME}_test-network") {
                        sh '''
                            pip install selenium
                            python e2e.py http://app:8777
                        '''
                    }
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-username',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_PASS'
                    )]) {
                        sh """
                            docker login -u ${DOCKERHUB_USER} -p ${DOCKERHUB_PASS}
                            docker tag ${COMPOSE_PROJECT_NAME}-app:latest ${DOCKERHUB_REPO}:${env.BUILD_ID}
                            docker push ${DOCKERHUB_REPO}:${env.BUILD_ID}
                            docker push ${DOCKERHUB_REPO}:latest
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                // Use Docker's compose plugin for cleanup
                sh 'docker compose down -v --remove-orphans || true'
            }
            deleteDir()
        }
    }
}