pipeline {
    agent { label "Jenkins-Agent" }

    environment {
        DOCKER_USERNAME = 'addition1905'
        DOCKER_IMAGE = 'addition1905/audit-vision:latest'
    }

    stages {

        stage("Checkout Code") {
            steps {
                checkout scm
            }
        }

        stage("Build") {
            steps {
                echo "Building the application..."
            }
        }

        stage("SonarQube Analysis") {
            steps {
                withSonarQubeEnv('sonar-server') {
                    sh '''
                    docker run --rm \
                      -v $(pwd):/usr/src \
                      -w /usr/src \
                      sonarsource/sonar-scanner-cli:latest \
                      -Dsonar.projectKey=audit_key \
                      -Dsonar.projectName=Audit_Vision \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=$SONAR_HOST_URL \
                      -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }

        stage("Quality Gate") {
            steps {
                timeout(time: 15, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage("Docker Build and Push") {
            steps {
                script {
                    def img = docker.build(DOCKER_IMAGE)
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        img.push()
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
        success {
            echo "Pipeline executed successfully."
        }
        failure {
            echo "Pipeline failed."
        }
    }
}
