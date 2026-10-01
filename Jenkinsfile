stage('Build') {
    steps {
        sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
    }
}

stage('Security Scan') {
    steps {
        sh """
            trivy image \
            --severity HIGH,CRITICAL \
            --exit-code 1 \
            ${IMAGE_NAME}:${IMAGE_TAG}
        """
    }
}

stage('Push Image') {
    steps {
        withCredentials([
            usernamePassword(
                credentialsId: 'dockerhub-creds',
                usernameVariable: 'DOCKER_USER',
                passwordVariable: 'DOCKER_PASS'
            )
        ]) {
            sh '''
                echo "$DOCKER_PASS" | docker login \
                    -u "$DOCKER_USER" --password-stdin

                docker push ${IMAGE_NAME}:${IMAGE_TAG}

                docker logout
            '''
        }
    }
}

stage('Deploy Kubernetes') {
    steps {
        withCredentials([
            file(
                credentialsId: 'kubernetes-config',
                variable: 'KUBECONFIG'
            )
        ]) {
            sh """
                kubectl -n food-ordering \
                  set image deployment/food-ordering \
                  food-ordering=${IMAGE_NAME}:${IMAGE_TAG}

                kubectl -n food-ordering \
                  rollout status deployment/food-ordering \
                  --timeout=180s
            """
        }
    }
}

stage('Smoke Test') {
    steps {
        withCredentials([
            file(
                credentialsId: 'kubernetes-config',
                variable: 'KUBECONFIG'
            )
        ]) {
            sh '''
                kubectl -n food-ordering \
                  run smoke-test \
                  --rm \
                  --restart=Never \
                  --image=curlimages/curl:8.10.1 \
                  -- \
                  curl -f http://food-ordering-service/health
            '''
        }
    }
}