#!/bin/bash

set -e 

export TERM=xterm-256color^M

SERVICES_SYSTEMD=(
	"onlyofficeAutoCleanUp.service" 
	"onlyofficeBackup.service" 
	"onlyofficeControlPanel.service" 
	"onlyofficeFeed.service" 
	"onlyofficeIndex.service"                          
        "onlyofficeJabber.service"                         
        "onlyofficeMailAggregator.service"                 
        "onlyofficeMailCleaner.service"                    
        "onlyofficeMailImap.service"                       
        "onlyofficeMailWatchdog.service"                  
        "onlyofficeNotify.service"                   
        "onlyofficeRadicale.service"                       
        "onlyofficeSocketIO.service"                       
        "onlyofficeSsoAuth.service"                        
        "onlyofficeStorageEncryption.service"              
        "onlyofficeStorageMigrate.service"                
        "onlyofficeTelegram.service"                       
        "onlyofficeThumb.service"                        
        "onlyofficeThumbnailBuilder.service"               
        "onlyofficeUrlShortener.service"                   
	"onlyofficeWebDav.service")      

SERVICES_SUPERVISOR=(
	"ds:converter"
	"ds:docservice"
	"ds:metrics")


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

function prepare_vm() {
  if [ ! -f /etc/centos-release ]; then 
    apt-get remove postfix -y 
    echo "${COLOR_GREEN}☑ PREPAVE_VM: Postfix was removed${COLOR_RESET}"
  fi

  echo '127.0.0.1 host4test' | sudo tee -a /etc/hosts   
  echo "${COLOR_GREEN}☑ PREPAVE_VM: Hostname was setting up${COLOR_RESET}"   

}

function install_workspace() {
  wget https://download.onlyoffice.com/install/workspace-install.sh 
  echo "N" | bash workspace-install.sh --skiphardwarecheck true --makeswap false 
}

function healthcheck_systemd_services() {
 
  sleep 60s 

  for service in ${SERVICES_SYSTEMD[@]} 
  do 
    if systemctl is-active --quiet ${service}; then
      echo "${COLOR_GREEN}☑ OK: Service ${service} is running${COLOR_RESET}"
    else 
      echo "${COLOR_RED}⚠ FAILED: Service ${service} is not running${COLOR_RESET}"
      SYSTEMD_SVC_FAILED="true"
    fi
  done
}

function healthcheck_supervisor_services() {
  for service in ${SERVICES_SUPERVISOR[@]}
    do
      if supervisorctl status ${service} > /dev/null 2>&1 ; then
        echo "${COLOR_GREEN}☑ OK: Service ${service} is running${COLOR_RESET}"
      else
        echo "${COLOR_RED}⚠ FAILED: Service ${service} is not running${COLOR_RESET}"
        SUPERVISOR_SVC_FAILED="true"
      fi
    done
}

function healthcheck_documentserver() {
echo "test"
}

function healthcheck_general_status() {
  if [ ! -z "${SYSTEMD_SVC_FAILED}" ] || [ ! -z ${SUPERVISOR_SVC_FAILED} ]; then
    echo "${COLOR_YELLOW}⚠ ⚠ ATTENTION: Some sevices is not running⚠ ⚠ ${COLOR_RESET}"
    exit 1
  fi
}


main() {
  common::get_colors
  prepare_vm
  install_workspace
  healthcheck_systemd_services
  healthcheck_supervisor_services
  healthcheck_general_status
}


main
