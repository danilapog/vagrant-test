
Vagrant.configure("2") do |config|
    config.vm.box = "%BOX_IMAGE%"
    
    #config.vm.provider "virtualbox" do |v|
    #         v.memory = 8192
    #         v.cpus = 2
    #end

    config.vm.define 'ubuntu'

    config.vm.hostname = "host4test"

    config.vm.provision "shell", path: './install.sh'
    
    # Prevent SharedFoldersEnableSymlinksCreate errors
    config.vm.synced_folder ".", "/vagrant", disabled: true
end
