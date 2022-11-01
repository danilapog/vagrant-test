Vagrant.configure("2") do |config|
    config.vm.box = "%BOX_IMAGE%"
    
    config.vm.define 'ubuntu'

    config.vm.hostname = "host4test"
    
    config.vm.provision "shell", path: './install.sh'
    
    # Prevent SharedFoldersEnableSymlinksCreate errors
    config.vm.synced_folder ".", "/vagrant", disabled: true
end
