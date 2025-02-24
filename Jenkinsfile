pipeline {
    agent any
    environment {
        IMAGE_TAG = "${env.BUILD_ID}"
        GIT_BRANCH = "main"
        DOCKER_IMAGE_NAME = "earscope-model"
    }
    stages {
        stage('Checkout Code') {
            steps {
                script {
                    sh """
                    echo "Cleaning workspace..."
                    rm -rf flask-server-earscope-TA || true
                    """
                    withCredentials([usernamePassword(credentialsId: 'github-auth-to-jenkins', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                        sh """
                        echo "Cloning repository with authentication..."
                        git clone https://${GIT_USER}:${GIT_TOKEN}@github.com/adrfstwn/flask-server-earscope-TA.git -b ${GIT_BRANCH}
                        """
                    }
                }
            }
        }
        stage('Prepare .env File') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'earscope-model-env', variable: 'ENV_FILE')]) {
                        sh """
                        echo "Creating .env file..."
                        cp \${ENV_FILE} flask-server-earscope-TA/.env
                        """
                    }
                }
            }
        }
        stage('Stop Running Containers') {
            steps {
                script {
                    sh """
                    echo "Stopping running container..."
                    
                    cd flask-server-earscope-TA
                    
                    if docker ps -a | grep earscope-model; then
                        docker compose down || true
                    fi

                    echo "Checking if old image exists..."
                    OLD_IMAGE_ID=\$(docker images -q ${DOCKER_IMAGE_NAME})

                    if [ ! -z "\$OLD_IMAGE_ID" ]; then
                        echo "Deleting old image..."
                        docker rmi -f \$OLD_IMAGE_ID
                    else
                        echo "No old image found, skipping delete step."
                    fi
                    """
                }
            }
        }
        stage('Build & Deploy Docker Image') {
            steps {
                script {
                    sh """
                    echo "Updating docker-compose.yml with new image tag..."
                    
                    cd flask-server-earscope-TA
                    
                    # Update image tag in docker-compose.yml
                    sed -i "s|image:.*|image: ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}|" docker-compose.yml
                    
                    echo "Final docker-compose.yml content:"
                    cat docker-compose.yml
                    
                    echo "Building Docker image locally..."
                    docker compose build --no-cache
                    
                    echo "Deploying container using docker compose..."
                    docker compose up -d --force-recreate
                    
                    echo "Checking working directory in the container..."
                    docker exec earscope-model pwd
                    docker exec earscope-model ls -al /app
                    """
                }
            }
        }
    }
    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}