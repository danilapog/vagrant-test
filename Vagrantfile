
Vagrant.configure("2") do |config|
    config.vm.box = "%BOX_IMAGE%"
    
    config.vm.provider "virtualbox" do |v|
             v.customize ["modifyvm", :id, "--memory", 5120] #<= 5120 equals 5GB total memory.
             v.customize ["modifyvm", :id, "--cpus", 4] #<= 4 equals 4cpu.
             v.customize ["modifyvm", :id, "--ioapic", "on"]
    end

    config.vm.define 'ubuntu'

    config.vm.hostname = "host4test"
    
    config.vm.provision "shell", path: './install.sh'
    
    # Prevent SharedFoldersEnableSymlinksCreate errors
    config.vm.synced_folder ".", "/vagrant", disabled: true
end
