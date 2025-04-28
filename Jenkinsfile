pipeline {
    agent any
    environment {
        VENV_DIR = "myenv"          // Define virtual environment directory
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir() // Clean workspace before pulling fresh repo
            }
        }

        stage('Clone Repository') {
            steps {

        // This stage clones the repository from GitHub into the Jenkins workspace.
        // It uses Git credentials (github-pat) for authentication.
        // It checks out the main branch.
        // Cloning the repository every time we run Jenkins file ensures Jenkins has the latest code before running the pipeline.

                git credentialsId: 'my_secret_token', url: 'https://github.com/WalaaHijazi1/WorldGame-Project.git', branch: 'WorldGame-Project-Bonus'
            }
        }

        stage('Update Repository') {
            steps {

         // If a previous build modified the repository, this ensures a fresh and clean state.
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
                 #Remove existing venv to avoid corruption or permission issues
                        rm -rf ${VENV_DIR}

                 # Create a fresh virtual environment
                        python3 -m venv ${VENV_DIR}

                 # Activate and install dependencies
                        . ${VENV_DIR}/bin/activate
                        pip install -r requirements.txt
                    """
                }
            }
        }
        stage('Build Docker Image For Server') {               // Build an image of the rest app server.
            steps {
                sh 'docker build -t live-games-server .'
            }
        }
        stage('Push Docker Image & Set Image Version For Server') {
        // This stage logs into Docker Hub securely, tags the Docker image with the current build ID, and pushes it to your Docker Hub account under the name walaahij/rest-app-server:<build_id>.
            steps {
                script {

             // withCredentials sets docker username and password to temporary environment variables, DOCKER_USER and DOCKER_PASSWORD.
             // These variables are only available inside this block — keeps them secure.

                    withCredentials([usernamePassword(credentialsId: 'docker-username', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                # Here the image is being tagged with build id, after I access docker personal hub, and then the image is pushed to docker.
                            echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USER} --password-stdin
                            docker tag live-games-server:latest walaahij/live-games-server:${BUILD_ID}
                            docker push walaahij/live-games-server:${BUILD_ID}
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image For GuessGame') {               // Build an image of the rest app server.
            steps {
                sh 'docker build -f Dockerfile.guess -t walaahij/guessgame .'
            }
        }
        stage('Push Docker Image & Set Image Version For GuessGame') {
        // This stage logs into Docker Hub securely, tags the Docker image with the current build ID, and pushes it to your Docker Hub account under the name walaahij/rest-app-server:<build_id>.
            steps {
                script {

             // withCredentials sets docker username and password to temporary environment variables, DOCKER_USER and DOCKER_PASSWORD.
             // These variables are only available inside this block — keeps them secure.

                    withCredentials([usernamePassword(credentialsId: 'docker-username', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                # Here the image is being tagged with build id, after I access docker personal hub, and then the image is pushed to docker.
                            echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USER} --password-stdin
		docker tag walaahij/guessgame:latest walaahij/guessgame-image:${BUILD_ID}
		docker push walaahij/guessgame-image:${BUILD_ID}
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image For MemoryGame') {               // Build an image of the rest app server.
            steps {
                sh 'docker build -f Dockerfile.memory -t walaahij/memorygame .'
            }
        }
        stage('Push Docker Image & Set Image Version For MemoryGame') {
        // This stage logs into Docker Hub securely, tags the Docker image with the current build ID, and pushes it to your Docker Hub account under the name walaahij/rest-app-server:<build_id>.
            steps {
                script {

             // withCredentials sets docker username and password to temporary environment variables, DOCKER_USER and DOCKER_PASSWORD.
             // These variables are only available inside this block — keeps them secure.

                    withCredentials([usernamePassword(credentialsId: 'docker-username', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                # Here the image is being tagged with build id, after I access docker personal hub, and then the image is pushed to docker.
                            echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USER} --password-stdin
		docker tag walaahij/memorygame:latest walaahij/memorygame-image:${BUILD_ID}
		docker push walaahij/memorygame-image:${BUILD_ID}
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image For CurrencyRouletteGame') {               // Build an image of the rest app server.
            steps {
                sh 'docker build -f Dockerfile.currency -t walaahij/currencyroulettegame .'
            }
        }
        stage('Push Docker Image & Set Image Version For CurrencyRouletteGame') {
        // This stage logs into Docker Hub securely, tags the Docker image with the current build ID, and pushes it to your Docker Hub account under the name walaahij/rest-app-server:<build_id>.
            steps {
                script {

             // withCredentials sets docker username and password to temporary environment variables, DOCKER_USER and DOCKER_PASSWORD.
             // These variables are only available inside this block — keeps them secure.

                    withCredentials([usernamePassword(credentialsId: 'docker-username', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                # Here the image is being tagged with build id, after I access docker personal hub, and then the image is pushed to docker.
                            echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USER} --password-stdin
		docker tag walaahij/currencyroulettegame:latest walaahij/currencyroulettegame-image:${BUILD_ID}
		docker push walaahij/currencyroulettegame-image:${BUILD_ID}
                        '''
                    }
                }
            }
        }

        stage('Check & Install Docker-Compose') {                         // This stage ensures Docker Compose is installed properly and uses the latest version.
            steps {
                sh '''

              # Checks if docker-compose is already installed.
              # If yes, it removes the old binary from both common paths.

                    if command -v docker-compose &> /dev/null; then
                        echo "Docker Compose found. Removing existing version..."
                        sudo rm -f /usr/local/bin/docker-compose
                        sudo rm -f /usr/bin/docker-compose
                    else
                        echo "Docker Compose not found."
                    fi

              # Now it installs Docker compose.
                    echo "Installing Docker Compose..."

              # uname -m returns the machine architecture, it stores it
              # in the variable ARCH, so docker-compose in the right binary can be downloaded.
                    ARCH=$(uname -m)

              # $(uname -s) gives the righ Operating System
                    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$ARCH" -o /usr/local/bin/docker-compose

                    #Making the downloaded file executable
              sudo chmod +x /usr/local/bin/docker-compose

             # In the next line I create a symbolic link (shortcut) in /usr/bin so I can run docker-compose from anywhere.
             #|| true ensures this command won’t break the script even if the link already exists or fails.
                    sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose || true
                '''
            }
        }

        stage('Docker Compose stage') {
            steps {
                script {
                    // Substitute the BUILD_ID into the docker-compose.yml file before running
                    sh '''
                        # Remove manually started MySQL container if exists
                        docker rm -f my-mysql-container || true

                  # Kill any process that is using port 8777 on the host
                        sudo fuser -k 8777/tcp || true

                        # Replace image tag in docker-compose.yml
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

                  # Here I try to curl the app to which the flask server should be running,
                  # If the service is not available yet, it waits 2 seconds, then tries again,
                  # till the server is up and running.
                        until curl -s http://localhost:8777 > /dev/null || [ $counter -ge 15 ]; do
                            echo "Waiting for service to be available on port 8777..."
                            sleep 2
                            counter=$((counter + 1))
                        done

                  # but if it did not run properly after 15 times of trying it will give a message.
                        if [ $counter -ge 15 ]; then
                            echo "Service did not become available in time. Failing build."
                            exit 1
                        fi

                        echo "Service is up and running."
                    '''
                }
            }
        }

        stage('Docker Compose Test') {
            steps {
          // Here I ran the backend testing to test the sql container that i ran and the docker image that I pulled from docker HUB.
                sh '''
                    echo "Running backend tests inside Docker Compose..."
                    docker-compose exec live-games-server python3 e2e.py
                '''
            }
        }

        stage('Docker Compose Down & Remove Image') {
            steps {
	         sh '''
	 # Now, all the services that is defined in docker compose stops.
              # it also removes all the vlumes that is defined in docker-compose.
            echo "Stopping and removing Docker Compose services..."
            docker-compose down --volumes --remove-orphans

            echo "Forcing removal of remaining containers..."

             # Remove all the containers with the BUILD_ID tag and the sql-games-container container
            # Remove containers by their name if they exist.
            docker rm -f live-games-server-${BUILD_ID} mysql-games-container guessgame-image-${BUILD_ID} memorygame-image-${BUILD_ID} currencyroulettegameimage-${BUILD_ID} || true

            echo "Removing Docker images..."
            docker rmi -f walaahij/live-games-server:${BUILD_ID} walaahij/guessgame-image:${BUILD_ID} walaahij/memorygame-image:${BUILD_ID} walaahij/currencyroulettegame-image:${BUILD_ID} || true
        '''
        	}
          }
    }
}

