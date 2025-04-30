pipeline {
    agent any
    environment {
        VENV_DIR = "myenv"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Clone Repository') {
            steps {
                git credentialsId: 'my_secret_token', url: 'https://github.com/WalaaHijazi1/WorldGame-Project.git', branch: 'WorldGame-Project-Bonus'
            }
        }

        stage('Update Repository') {
            steps {
                sh '''
                    git fetch --all
                    git reset --hard origin/WorldGame-Project-Bonus
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh """
                        rm -rf ${VENV_DIR}
                        python3 -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Build Docker Image For Server') {
            steps {
                sh 'docker build -t live-games-server .'
            }
        }

        stage('Push Docker Image & Set Image Version For Server') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-username', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                            echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USER} --password-stdin
                            docker tag live-games-server:latest walaahij/live-games-server:${BUILD_ID}
                            docker push walaahij/live-games-server:${BUILD_ID}
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image For GuessGame') {
            steps {
                sh 'docker build -f Dockerfile.guess -t walaahij/guessgame .'
            }
        }

        stage('Push Docker Image & Set Image Version For GuessGame') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-username', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                            echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USER} --password-stdin
                            docker tag walaahij/guessgame:latest walaahij/guessgame-image:${BUILD_ID}
                            docker push walaahij/guessgame-image:${BUILD_ID}
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image For MemoryGame') {
            steps {
                sh 'docker build -f Dockerfile.memory -t walaahij/memorygame .'
            }
        }

        stage('Push Docker Image & Set Image Version For MemoryGame') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-username', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                            echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USER} --password-stdin
                            docker tag walaahij/memorygame:latest walaahij/memorygame-image:${BUILD_ID}
                            docker push walaahij/memorygame-image:${BUILD_ID}
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image For CurrencyRouletteGame') {
            steps {
                sh 'docker build -f Dockerfile.currency -t walaahij/currencyroulettegame .'
            }
        }

        stage('Push Docker Image & Set Image Version For CurrencyRouletteGame') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-username', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                            echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USER} --password-stdin
                            docker tag walaahij/currencyroulettegame:latest walaahij/currencyroulettegame-image:${BUILD_ID}
                            docker push walaahij/currencyroulettegame-image:${BUILD_ID}
                        '''
                    }
                }
            }
        }

        stage('Check & Install Docker-Compose') {
            steps {
                sh '''
                    if command -v docker-compose &> /dev/null; then
                        echo "Docker Compose found. Removing existing version..."
                        sudo rm -f /usr/local/bin/docker-compose
                        sudo rm -f /usr/bin/docker-compose
                    fi

                    echo "Installing Docker Compose..."
                    ARCH=$(uname -m)
                    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$ARCH" -o /usr/local/bin/docker-compose
                    sudo chmod +x /usr/local/bin/docker-compose
                    sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose || true
                '''
            }
        }

        stage('Docker Compose stage') {
            steps {
                script {
                    sh '''
                        sudo fuser -k 8777/tcp || true
                        sed -i "s|BUILD_ID_PLACEHOLDER|${BUILD_ID}|g" docker-compose.yml
                        docker-compose up -d --build
                    '''
                }
            }
        }

        stage('Wait for Docker-Compose') {
            steps {
                script {
                    sh '''
                        echo "Waiting for Docker Compose services to be up..."
                        counter=0
                        until curl -s http://localhost:8777 > /dev/null || [ $counter -ge 15 ]; do
                            echo "Waiting for service to be available on port 8777..."
                            sleep 2
                            counter=$((counter + 1))
                        done
                        if [ $counter -ge 15 ]; then
                            echo "Service did not become available in time. Failing build."
                            exit 1
                        fi
                        echo "Service is up and running."
                    '''
                }
            }
        }

        stage('Wait for Manual Game Play') {
            steps {
                script {
                    echo 'Waiting for user to finish playing...'
                    timeout(time: 10, unit: 'MINUTES') {
                        waitUntil {
                            return fileExists('continue.flag')
                        }
                    }
                }
            }
        }

        stage('Docker Compose Test') {
            steps {
                sh '''
                    echo "Running backend tests on the host against the running Docker Compose services..."
                    bash -c "
                        source ${VENV_DIR}/bin/activate
                        python3 e2e.py
                    "
                '''
            }
        }

        stage('Docker Compose Down & Remove Image') {
            steps {
                sh '''
                    echo "Stopping and removing Docker Compose services..."
                    docker-compose down --volumes --remove-orphans

                    echo "Removing containers..."
                    docker rm -f live-games-server-${BUILD_ID} mysql-games-container guessgame-image-${BUILD_ID} memorygame-image-${BUILD_ID} currencyroulettegameimage-${BUILD_ID} || true

                    echo "Removing Docker images..."
                    docker rmi -f walaahij/live-games-server:${BUILD_ID} walaahij/guessgame-image:${BUILD_ID} walaahij/memorygame-image:${BUILD_ID} walaahij/currencyroulettegame-image:${BUILD_ID} || true
                '''
            }
        }
    }
}
