#!/bin/bash

set -e 

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
    COLOR_RESET=$'\e[0m'
}

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


prepare_vm() {
  if [ ! -f /etc/centos-release ]; then 
    apt-get remove postfix -y 
  fi

  echo '127.0.0.1 host4test' | sudo tee -a /etc/hosts 
  echo "PREPAVE_VM: Postfix was removed <<=="  
  echo "PREPAVE_VM: Hostname was setting up <<=="   

}

install_workspace() {
  wget https://download.onlyoffice.com/install/workspace-install.sh 
  echo "N" | bash workspace-install.sh --skiphardwarecheck true --makeswap false 
}

healthcheck_systemd_services() {
  for service in ${SERVICES_SYSTEMD[@]} 
  do 
    if systemctl is-active --quiet ${service}; then
      echo "${COLOR_GREEN}☑ OK: Service ${service} is running${COLOR_RESET}"
    else 
      echo "${COLOR_RED}⚠ FAILED: Service ${service} is not running${COLOR_RESET}"
      SERVICES_FAILED="true"
    fi
  done

  if [ ! -z "${SERVICES_FAILED}" ]; then
    echo "${COLOR_YELLOW}Some sevices is not running${COLOR_RESET}"
    exit 1
  fi
}

#healthcheck_supervisor_services(){
#  for service in ${SERVICES_SUPERVISOR[@]}
#  do
#
#}


main() {
  prepare_vm
  install_workspace
  healthcheck_systemd_services
  healthcheck_supervisor_services

}


main
