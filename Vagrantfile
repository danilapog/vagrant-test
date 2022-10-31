Vagrant.configure("2") do |config|
    config.vm.box = "%BOX_IMAGE%"
    
    config.vm.define 'ubuntu'

    config.vm.hostname = "host4test"
    
    config.vm.provider "virtualbox" do |vb|
     vb.gui = false
     vb.memory = "14000"
    end
    
    # Prevent SharedFoldersEnableSymlinksCreate errors
    config.vm.synced_folder ".", "/vagrant", disabled: true
end
