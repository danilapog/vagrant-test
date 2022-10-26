Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/trusty64"

    config.vm.define 'ubuntu'

    config.ssh.insert_key = false
    
    config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.playbook = "playbook.yml"
  end

    # Prevent SharedFoldersEnableSymlinksCreate errors
    config.vm.synced_folder ".", "/vagrant", disabled: true
end
