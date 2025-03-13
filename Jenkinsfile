pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile' // Nama file Dockerfile (default: Dockerfile)
            additionalBuildArgs '--no-cache' // Opsional: argumen tambahan untuk build
        }
    }
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
        stage('Build Docker Image') {
            steps {
                script {
                    dir('flask-server-earscope-TA') {
                        sh """
                        echo "Building Docker image with tag ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}..."
                        docker build -t ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} .

                        echo "Checking size of the built Docker image..."
                        IMAGE_SIZE=\$(docker images --format "{{.Size}}" ${DOCKER_IMAGE_NAME}:${IMAGE_TAG})
                        echo "Size of Docker image '${DOCKER_IMAGE_NAME}:${IMAGE_TAG}': \$IMAGE_SIZE
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
        always {
            cleanWs()
    }
}