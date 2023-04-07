#!/usr/bin/env bash

# Scripts for deploys and check Kuberneted-Docs helm chart

set -euo pipefail 

export TERM=xterm-256color^M

function common::get_colors() {
    COLOR_BLUE=$'\e[34m'
    COLOR_GREEN=$'\e[32m'
    COLOR_RED=$'\e[31m'
    COLOR_RESET=$'\e[0m'
    COLOR_YELLOW=$'\e[33m'
    export COLOR_BLUE
    export COLOR_GREEN
    export COLOR_RED
    export COLOR_RESET
    export COLOR_YELLOW
}

function k8s_w8_workers() {
         for i in {1..20}; do
            echo "${COLOR_YELLOW}Get k8s workers status ${i}${COLOR_RESET}"
            STATUS=$(kubectl get nodes -o json | jq -r '.items[] | select ( .status.conditions[] | select( .type=="Ready" and .status=="False")) | .metadata.name')
            if [[ -z "${STATUS}"  ]]; then
              echo "${COLOR_GREEN}☑ OK: K8s workers is ready. Continue...${COLOR_RESET}"
              local k8s_ready
              k8s_ready='true'
              break
            else
              sleep 5
            fi
         done
         if [[ "${k8s_ready}" != 'true' ]]; then
           err "\e[0;31m Something goes wrong. K8s is not ready \e[0m"
           exit 1
         fi
}

function k8s_get_info() {
            kubectl get all
            kubectl get sc
            kubectl get nodes
}

function k8s_deploy_deps() {
            # Add dependency helm charts
            helm repo add bitnami https://charts.bitnami.com/bitnami
            helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
            helm repo add nfs-server-provisioner https://kubernetes-sigs.github.io/nfs-ganesha-server-and-external-provisioner
            helm repo add onlyoffice https://download.onlyoffice.com/charts/stable
            helm repo update
            echo "${COLOR_GREEN}☑ OK: Helm repository was added${COLOR_RESET}" 
            
            # Install nfs server
            helm install nfs-server nfs-server-provisioner/nfs-server-provisioner \
                 --set persistence.enabled=true \
                 --set persistence.storageClass=${K8S_STORAGE_CLASS} \
                 --set persistence.size=${NFS_PERSISTANCE_SIZE}
            echo "${COLOR_GREEN}☑ OK: NFS Server was deployed${COLOR_RESET}"
            
            # Install rabbitmq
            helm install rabbitmq bitnami/rabbitmq \
                 --set metrics.enabled=false
            echo "${COLOR_GREEN}☑ OK: Rabbitmq was deployed${COLOR_RESET}"
            
            # Install redis
            helm install redis bitnami/redis \
                 --set architecture=standalone \
                 --set metrics.enabled=false
            echo "${COLOR_GREEN}☑ OK: Redis was deployed${COLOR_RESET}
            
            # Install postgresql
            helm install postgresql bitnami/postgresql \
                 --set auth.database=postgres \
                 --set primary.persistence.size=2G \
                 --set metrics.enabled=false
            echo "${COLOR_GREEN}☑ OK: Postgresql was deployed${COLOR_RESET}
            
     }
      
function k8s_wait_deps() {

            echo "${COLOR_YELLOW}Wait that all dependency is ready${COLOR_RESET}" 
            sleep 120
     }
     
function k8s_ct_install() {
            echo "${COLOR_YELLOW}Attention❗: Start ct install test${COLOR_RESET}"
            ct install --charts .
     }
          
function k8s_deploy_docs(){
            helm install documentserver onlyoffice/docs
            sleep 180
     }

function main () {
   common::get_colors
   #k8s_w8_workers
   k8s_deploy_deps
   k8s_wait_deps
   k8s_ct_install
 }
 
 main
