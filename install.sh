#!/bin/bash

prepare_debian () {

}

healthcheck_services () {

}

install_workspace () {
   if [ ! -f /etc/centos-release ]; then apt-get remove postfix -y ; fi
   echo '127.0.0.1 host4test' | sudo tee -a /etc/hosts
   wget https://download.onlyoffice.com/install/workspace-install.sh 
   echo "N" | sudo bash workspace-install.sh --skiphardwarecheck true --makeswap false
   if [ $? != 0 ] ; then echo "exit with 0" ; exit 0; fi

}

install_workspace
