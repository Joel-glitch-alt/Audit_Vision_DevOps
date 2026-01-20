pipeline {
    agent { label "Jenkins-Agent" }

    environment {
        SCANNER_HOME = tool 'sonarqube-scanner'
        SONARQUBE = 'Sonar-Server'
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
                withSonarQubeEnv("${SONARQUBE}") {
                    sh """
                        ${SCANNER_HOME}/bin/sonarqube-scanner \
                          -Dsonar.projectKey=audit_key \
                          -Dsonar.projectName=Audit_Vision \
                          -Dsonar.sources=. \
                          -Dsonar.sourceEncoding=UTF-8 \
                          -Dsonar.python.coverage.reportPaths=coverage.xml
                    """
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
    }

    post {
        always {
            echo "======== always ========"
        }
        success {
            echo "======== pipeline executed successfully ========"
        }
        failure {
            echo "======== pipeline execution failed ========"
        }
    }
}
