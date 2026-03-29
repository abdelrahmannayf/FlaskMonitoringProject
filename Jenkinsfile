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
                sh "docker build -t ${IMAGE_NAME}:latest ."
            }
        }
        stage('Scan Image (Trivy)') {
            steps {
                sh 'trivy image $IMAGE_NAME:latest || true'
            }
        }
        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-cred',
                    passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
                    sh 'docker push $IMAGE_NAME:latest'
                }
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
