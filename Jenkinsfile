#!groovy

node {
    def scmVars = checkout scm

    def dockerRepoName = 'zooniverse/aggregation-for-caesar'
    def stackName = 'aggregation-caesar'

    def dockerImageName = "${dockerRepoName}:${BRANCH_NAME}"
    def buildArgs = "--build-arg REVISION='${scmVars.GIT_COMMIT}' ."
    def newImage = null

    stage('Build Docker image') {
        newImage = docker.build(dockerImageName, buildArgs)
        newImage.push()
        newImage.push(scmVars.GIT_COMMIT)
    }

    if (BRANCH_NAME == 'master') {
        stage('Update latest tag') {
            newImage.push('latest')
        }

        stage('Deploy to Kubernetes') {
          sh "kubectl --context azure apply --record -f kubernetes/"
          sh "sed 's/__IMAGE_TAG__/${scmVars.GIT_COMMIT}/g' kubernetes/deployment.tmpl | kubectl --context azure apply --record -f -"
        }
    }
}
