$script = <<-SCRIPT
echo I am provisioning...
if [ ! -f /etc/centos-release ]; then apt-get remove postfix -y ; fi
echo '127.0.0.1 host4test' | sudo tee -a /etc/hosts
wget https://download.onlyoffice.com/install/workspace-install.sh 
echo "N" | bash workspace-install.sh --skiphardwarecheck true --makeswap false
SCRIPT

Vagrant.configure("2") do |config|
    config.vm.box = "%BOX_IMAGE%"
    
    config.vm.define 'ubuntu'

    config.vm.hostname = "host4test"

    config.vm.provision "shell", 
      inline: -c $script
    
    #config.vm.provision "shell", path: './install.sh'
    
    # Prevent SharedFoldersEnableSymlinksCreate errors
    config.vm.synced_folder ".", "/vagrant", disabled: true
end
