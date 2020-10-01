pipeline {
    environment {
        NAME = 'my-app'
        VERSION = '0.1'
        REGISTRY = 'yonahdissen/prom-app'
        REGISTRY_CREDENTIAL = 'dockerhub-yonahdissen'
    }
    stages {
        stage('Docker Build') {
            steps {
                container('docker') {
                    sh "docker build -t ${REGISTRY}:${VERSION} ."
                }
            }
        }
        stage('Run Tests') {
          steps {
            script {
                sh "docker run ${REGISTRY}:${VERSION} python3 /app/test_main.py"
            }
          }
        }
        stage('Docker Publish') {
            steps {
                container('docker') {
                    withDockerRegistry([credentialsId: "${REGISTRY_CREDENTIAL}", url: ""]) {
                        sh "docker push ${REGISTRY}:${VERSION}"
                    }
                }
            }
        }
        stage('Kubernetes Deploy') {
            steps {
                container('helm') {
                    sh "helm upgrade --install --force  --set image.tag=${VERSION}  ${NAME} ./prom-app --set service.type=LoadBalancer"
                }
            }
        }
    }
}
