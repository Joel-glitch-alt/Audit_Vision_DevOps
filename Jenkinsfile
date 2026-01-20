pipeline {
    agent { label "Jenkins-Agent" }

    stages {
        stage("Checkout Code") {
            steps { checkout scm }
        }

        stage("Build") {
            steps { echo "Building the application..." }
        }

        stage("SonarQube Analysis") {
            steps {
                script {
                    withSonarQubeEnv('sonar-server') {
                        sh """
                        docker run --rm \
                          -v \$(pwd):/usr/src \
                          -w /usr/src \
                          sonarsource/sonar-scanner-cli:latest \
                          -Dsonar.projectKey=audit_key \
                          -Dsonar.projectName=Audit_Vision \
                          -Dsonar.sources=. \
                          -Dsonar.host.url=\$SONAR_HOST_URL \
                          -Dsonar.login=\$SONAR_AUTH_TOKEN \
                          -Dsonar.working.directory=./.scannerwork
                        """
                        
                        // Copy the report-task.txt to workspace root
                        sh """
                        if [ -f .scannerwork/report-task.txt ]; then
                            mkdir -p target/sonar
                            cp .scannerwork/report-task.txt target/sonar/report-task.txt
                            cat target/sonar/report-task.txt
                        else
                            echo "Warning: report-task.txt not found"
                            ls -la .scannerwork/ || echo ".scannerwork directory not found"
                        fi
                        """
                    }
                }
            }
        }

        stage("Quality Gate") {
            steps {
                timeout(time: 15, unit: 'MINUTES') {
                    script {
                        def qg = waitForQualityGate()
                        if (qg.status != 'OK') {
                            error "Pipeline aborted due to quality gate failure: ${qg.status}"
                        }
                    }
                }
            }
        }
    }

    post {
        always { echo "Pipeline finished." }
        success { echo "Pipeline executed successfully." }
        failure { echo "Pipeline failed." }
    }
}