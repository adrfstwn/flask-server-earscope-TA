pipeline {
    agent any
    environment {
        IMAGE_TAG = "${env.BUILD_ID}"
        GIT_BRANCH = "main"
        DOCKER_IMAGE_NAME = "earscope-model"
        REMOTE_WORKDIR = "/var/www/flask-server-TA"
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
        stage('Deploy to VPS Earscope') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'vps-earscope', keyFileVariable: 'SSH_KEY', usernameVariable: 'SSH_USER')]) {
                        sh """
                        echo "Copying project files to VPS..."
                        rsync -avz -e "ssh -i \${SSH_KEY} -o StrictHostKeyChecking=no -p 9802" flask-server-earscope-TA/ \${SSH_USER}@103.155.246.50:${REMOTE_WORKDIR}

                        echo "Running deployment commands on VPS..."
                        ssh -i \${SSH_KEY} -o StrictHostKeyChecking=no -p 9802 \${SSH_USER}@103.155.246.50 << EOF
                            cd ${REMOTE_WORKDIR}

                            echo "Stopping running containers..."
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

                            echo "Updating docker-compose.yml with new image tag..."
                            sed -i "s|image:.*|image: ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}|" docker-compose.yml

                            echo "Building Docker image..."
                            docker compose build --no-cache

                            echo "Deploying container..."
                            docker compose up -d --force-recreate

                            echo "Checking working directory in the container..."
                            docker exec earscope-model pwd
                            docker exec earscope-model ls -al /app
                        EOF
                        """
                    }
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
