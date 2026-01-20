pipeline{
    agent{
        label "Jenkins-Agent"
    }
    stages{
        stage("Checkout Code"){
            steps{
                checkout scm
            }
            
        }
        stage("Build"){
            steps{
                echo "Building the application..."
            }
    }
    post{
        always{
            echo "========always========"
        }
        success{
            echo "========pipeline executed successfully ========"
        }
        failure{
            echo "========pipeline execution failed========"
        }
    }
  }
}