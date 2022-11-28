
Vagrant.configure("2") do |config|
    config.vm.box = "#{ENV['DISTR']}/#{ENV['OS']}"
    
    config.vm.provider "virtualbox" do |v|
             v.customize ["modifyvm", :id, "--memory", 6144] #<= 6144 equals 6GB total memory.
             v.customize ["modifyvm", :id, "--cpus", 4] #<= 4 equals 4cpu.
             v.customize ["modifyvm", :id, "--ioapic", "on"]
    end

    config.vm.define 'ubuntu'

    config.vm.hostname = "host4test"
    
    if ENV['TEST_CASE'] == 'install-prod'
    config.vm.provision "shell", path: './install.sh', :args => "--production-install true"
    end

    if ENV['TEST_CASE'] == 'install-local'
    config.vm.provision "file", source: "../../../OneClickInstall-Workspace/.", destination: "/home/vagrant"
    config.vm.provision "shell", path: './install.sh', :args => "--local-install true"
    end

    if ENV['TEST_CASE'] == 'update-local'
    config.vm.provision "file", source: "../../../OneClickInstall-Workspace/.", destination: "/home/vagrant"
    config.vm.provision "shell", path: './install.sh', :args => "--local-update true"
    end

    # Prevent SharedFoldersEnableSymlinksCreate errors
    config.vm.synced_folder ".", "/vagrant", disabled: true
end
