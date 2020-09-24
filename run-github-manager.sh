#!/bin/bash

set -euo pipefail 

check_docker () {
    
    docker -v 

    if [[ $? != 0 ]]
    then
        echo "docker command not found."
    fi

}

buid_docker_image () {
    
    echo "Building Docker Image..."

    docker build -t github-manager . 

}


run_docker_image () {

    echo "Running Docker Image..."

    docker run --rm github-manager ${ARGS}

}

ARGS="$@"

check_docker

buid_docker_image

run_docker_image