Vagrant.configure("2") do |config|
    config.vm.box = "%BOX_IMAGE"

    config.ssh.insert_key = false
    
    config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.playbook = "playbook.yml"
  end
end
