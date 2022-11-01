$script = <<SCRIPT
wget https://download.onlyoffice.com/install/workspace-install.sh
echo "N" | sudo bash workspace-install.sh --skiphardwarecheck true --makeswap false
if [ $? != 0 ] ; then exit 1; else exit 0; fi
SCRIPT

Vagrant.configure("2") do |config|
    config.vm.box = "%BOX_IMAGE%"
    
    config.vm.define 'ubuntu'

    config.vm.hostname = "host4test"
    
    config.vm.provision "shell", inline: "$script"
    
    # Prevent SharedFoldersEnableSymlinksCreate errors
    config.vm.synced_folder ".", "/vagrant", disabled: true
end
