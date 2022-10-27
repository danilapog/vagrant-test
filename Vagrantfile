Vagrant.configure("2") do |config|
    config.vm.box = "%BOX_IMAGE%"
    
    config.ssh.username = 'root'

    config.ssh.password = 'vagrant'

    config.ssh.insert_key = 'true'

    config.vm.define 'ubuntu'

    # Prevent SharedFoldersEnableSymlinksCreate errors
    config.vm.synced_folder ".", "/vagrant", disabled: true
end
