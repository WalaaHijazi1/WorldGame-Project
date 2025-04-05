pipeline {
    agent any

    environment {
        DOCKERHUB_REPO = 'walaahijazi/scores-flask-server' // Example, adjust this
    }

    stages {
        stage('Clone Repository') {
            steps {
                git credentialsId: 'my_secret_token',
                    url: 'https://github.com/WalaaHijazi1/WorldGame-Project.git',
                    branch: 'main'
            }
        }

        stage('Update Repository') {
            steps {
                sh '''
                    git fetch --all
                    git reset --hard origin/main
                '''
            }
        }

        stage('Build Docker image & run it') {
            steps {
                sh 'docker build -t scores-flask-server .'
	  sh "docker run -d --name scores-flask-server-${env.BUILD_ID} -p 8777:8777 scores-flask-server"
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'rm -rf venv'
                sh 'python3 -m venv venv'
                sh '''
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test Flask Server') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 e2e.py
                '''
            }
        }

        stage('Finalize') {
            steps {
                script {
                    sh "docker-compose -p scores-flask-server down -v"

                    withCredentials([usernamePassword(
                        credentialsId: 'docker-username',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_PASS'
                    )]) {
                        sh """
                            docker login -u ${DOCKERHUB_USER} -p ${DOCKERHUB_PASS}
                            docker tag scores-flask-server:latest ${DOCKERHUB_REPO}:${env.BUILD_ID}
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
            deleteDir()
        }
    }
}
