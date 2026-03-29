@Library('shared-library') _

pipeline {
    agent any
    environment {
        IMAGE_NAME = "abdelrahmannayf/flaskmonitoring"
        NAMESPACE  = "monitoring"
        RELEASE    = "flaskapp"
        CHART_PATH = "flaskapp"
    }
    stages {
        stage('Build Image') {
            steps {
                buildImage(IMAGE_NAME)
            }
        }
        stage('Scan Image (Trivy)') {
            steps {
                sh 'trivy image $IMAGE_NAME:latest || true'
            }
        }
        stage('Push Image') {
            steps {
                pushImage(IMAGE_NAME)
            }
        }
        stage('Deploy with Helm') {
            steps {
                sh '''
                    helm upgrade --install $RELEASE ./$CHART_PATH \
                        --namespace $NAMESPACE \
                        --set image.repository=$IMAGE_NAME \
                        --set image.tag=latest
                '''
            }
        }
    }
}
