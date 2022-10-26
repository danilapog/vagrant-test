Vagrant.configure("2") do |config|
    config.vm.box = ""generic/ubuntu1804""

    config.vm.define 'ubuntu'

    config.ssh.insert_key = false
   
    config.vm.network "private_network", ip: "192.168.56.0"
    
    config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.playbook = "playbook.yml"
  end

    # Prevent SharedFoldersEnableSymlinksCreate errors
    config.vm.synced_folder ".", "/vagrant", disabled: true
end
