pipeline {
    agent any

    environment {
        DOCKERHUB_REPO = 'walaahij/scores-flask-server' // this is an environment variable that i will use along the stages
    }

    stages {
        stage('Clone Repository') {
            steps {
	// This stage clones the repository from GitHub into the Jenkins workspace.
	// It uses Git credentials (my_secret_token) for authentication.
	// It checks out the main branch.
	// Cloning the repository every time we run Jenkins file ensures Jenkins has the latest code before running the pipeline.

                git credentialsId: 'my_secret_token',
                    url: 'https://github.com/WalaaHijazi1/WorldGame-Project.git',
                    branch: 'main'
            }
        }

        stage('Update Repository') {
            steps {
	 // If a previous build modified the repository, this ensures a fresh and clean state.
                sh '''
                    git fetch --all                                             # Fetches all branches and updates remote-tracking branches.
                    git reset --hard origin/main                       #  Ensures the local repository is in sync with the remote repository.
                '''
            }
        }
        stage('Clean Port 8777 Containers') {
             steps {
	// This stage was made to check if port 8777 is availabe and if not to delete the containers that are running in the port.
        	sh '''
            		CONTAINERS=$(docker ps --filter "publish=8777" --format "{{.ID}}")      
		# Lists running Docker containers that expose port 8777,
		# it extracts only the container IDs when running: --format "{{.ID}}", and saving all the ids in CONTAINERS variable.

            		if [ -n "$CONTAINERS" ]; then                                                      # Checks if CONTAINERS varibale is not empty, if not ...
                		echo "Stopping containers using port 8777..."       
                		docker stop $CONTAINERS                                            # STOPS all the containers that is running in the port
                		docker rm $CONTAINERS                                               # REMOVE all the containers that is running in the port
            		else
                		echo "No containers using port 8777"                            # If there was not any container running on the port it prints a message.
            		fi
        	     '''
   	}
           }
        stage('Build Docker image') {
            steps {
                sh 'docker build -t scores-flask-server .'                   // BUILDS a docker image that containes scores.py,MainScore.py and the text scores file, in order to run it as a server.
            }
        }
        stage('Run Docker image') {
           steps {
	        sh """
            docker rm -f scores-flask-server-${env.BUILD_ID} || true                                                                       # This line is a cleanup step: it ensures no old container with the same name interferes with the new one.
            docker run -d --name scores-flask-server-${env.BUILD_ID} -p 8777:8777 scores-flask-server                 # This line runs the Docker image as a background service, accessible on port 8777.
       	 """
          }
       }
        stage('Install Dependencies') {
            steps {
                sh 'rm -rf venv'                                               // removing any old virtual environment.
                sh 'python3 -m venv venv'                             // creating a new virtual environment with a file name of 'venv'.
                sh '''
                    . venv/bin/activate                                    # activating the new created virtual environment.
                    pip install -r requirements.txt                    # installing all the libraries that is defined in the requirements.txt file.
                '''
            }
        }
    stage('Test') {
            steps {
                script {
                    docker.image('python:3.8-slim').inside {
                        sh 'pip install selenium'
                        sh 'python e2e.py http://app:8777'
                    }
                }
            }
        }


        stage('Finalize') {                              // this is the final stage in this ci pipeline, it pushes the image into my private Docker Hub.
            steps {
                script {
	     	withCredentials([usernamePassword(                         //This securely injects credentials (from Jenkins' credentials store) into the pipeline.
                	credentialsId: 'docker-username',                              //Here 'docker-username' refers to a saved Jenkins credential (username/password pair).
                	usernameVariable: 'DOCKERHUB_USER', 
                	passwordVariable: 'DOCKERHUB_PASS'                     // Both DOCKERHUB_USER and DOCKERHUB_PASS will hold the username and password values from docker-username.
            		)]) {
 
                	echo "Logging in as ${DOCKERHUB_USER}"

               	 // Log in securely
                	sh """
		echo ${DOCKERHUB_PASS} | docker login -u ${DOCKERHUB_USER} --password-stdin                    # Logs in to Docker securely using --password-stdin, which avoids exposing the password in the process list.
                    	docker tag scores-flask-server:latest ${DOCKERHUB_REPO}:${env.BUILD_ID}                                  # Tags the image with a versioned tag, using the current Jenkins build number as the tag.
                    	docker push ${DOCKERHUB_REPO}:${env.BUILD_ID}                                                                     # Pushes the tagged image to Docker Hub.
                	"""
		dockerCompose.down()
                    }
                }
            }
        }
    }

    post {
        always {
            // deleteDir() within a post { always { ... } } block serves to clean up the workspace by deleting its contents after each build. 
            // This practice helps prevent potential issues caused by residual files from previous build
            deleteDir()
        }
    }
}
