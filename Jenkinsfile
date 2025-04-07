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

        stage('Build Docker Images') {
            steps {
                script {
                    sh 'docker-compose build'
                }
            }
        }

        stage('Start Services') {
            steps {
                script {
                    sh """
                        docker-compose up -d app selenium-hub chrome
                        sleep 30  # Wait for services to initialize
                    """
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
                            docker tag ${COMPOSE_PROJECT_NAME}_app:latest ${DOCKERHUB_REPO}:${env.BUILD_ID}
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
                sh 'docker-compose down -v --remove-orphans'
            }
            deleteDir()
        }
    }
}