#!/bin/bash

prepare_debian () {

}

healthcheck_services () {

}

install_workspace () {

   apt-get remove postfix -y 
   wget https://download.onlyoffice.com/install/workspace-install.sh 
   echo "N" | sudo bash workspace-install.sh --skiphardwarecheck true --makeswap false
   if [ $? != 0 ] ; then exit 1; else healthcheck_services; fi

}

