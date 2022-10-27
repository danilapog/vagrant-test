Vagrant.configure("2") do |config|
    config.vm.box = "%BOX_IMAGE%"
    
    config.vm.define 'ubuntu'
    config.vm.provision "shell", inline: <<-SHELL
    echo -e "vagrant\nvagrant" | passwd root
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
    sed -in 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
    service ssh restart
    SHELL
    config.ssh.username = 'root'   
    config.ssh.password = 'vagrant'
    config.ssh.insert_key = 'true'

    # Prevent SharedFoldersEnableSymlinksCreate errors
    config.vm.synced_folder ".", "/vagrant", disabled: true
end
