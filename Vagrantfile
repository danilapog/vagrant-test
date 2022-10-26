Vagrant.configure("2") do |config|
    config.vm.box = "generic/centos7"

    config.ssh.insert_key = false
    
    config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.playbook = "playbook.yml"
  end
end
