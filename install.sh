#!/bin/bash

set -e 

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

healthcheck_services() {
  for service in ${SERVICES_SYSTEMD[@]} 
    do 
      if systemctl is-active --quiet ${service}; then
        echo "OK: Service ${service} is running"
      else 
        echo "FAILED: Service ${service} is not running"
        SERVICES_FAILED="true"
      fi
  done

  if [ ! -z "${SERVICES_FAILED}" ]; then
    echo "Some sevices is not running"
    exit 1
  fi
}


main() {
  prepare_vm
  install_workspace
  healthcheck_services

}


main
