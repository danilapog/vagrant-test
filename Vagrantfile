
Vagrant.configure("2") do |config|
    config.vm.box = "%BOX_IMAGE%"
    
    config.vm.provider "virtualbox" do |v|
             v.memory = 7800
             v.customize ["modifyvm", :id, "--ioapic", "on"]
             v.cpus = 4
    end

    config.vm.define 'ubuntu'

    config.vm.hostname = "host4test"
    
    config.ssh.keep_alive = "true"

    config.vm.provision "shell", path: './install.sh'
    
    # Prevent SharedFoldersEnableSymlinksCreate errors
    config.vm.synced_folder ".", "/vagrant", disabled: true
end
