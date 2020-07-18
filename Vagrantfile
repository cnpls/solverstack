# -*- mode: ruby -*-
# vi: set ft=ruby :


# if on windows host without admin rights, warn & exit
if Vagrant::Util::Platform.windows? then
  def running_in_admin_mode?
    (`reg query HKU\\S-1-5-19 2>&1` =~ /ERROR/).nil?
  end

  unless running_in_admin_mode?
    puts "This vagrant makes use of SymLinks to the host. On Windows, Administrative privileges are required to create symlinks (mklink.exe). Try again from an Administrative command prompt."
    exit 1
  end
end

Vagrant.configure(2) do |config|

    config.vm.provider "virtualbox" do |vb|
      vb.memory = "512"
      vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
    end

    config.vm.box = "bento/ubuntu-20.04"

    # Install Docker
    config.vm.provision :docker

    # Install Docker Compose
    # First, install required plugin https://github.com/leighmcculloch/vagrant-docker-compose:
    # vagrant plugin install vagrant-docker-compose
    config.vm.provision :docker_compose

    config.vm.network :forwarded_port, guest: 80, host: 80

    # web-client
    config.vm.network :forwarded_port, guest: 3000, host: 3000

    # user-auth
    config.vm.network :forwarded_port, guest: 8080, host: 8080

    # user-crud
    config.vm.network :forwarded_port, guest: 8081, host: 8081

    # vrp-rpc
    config.vm.network :forwarded_port, guest: 5000, host: 5000

    # mogno
    config.vm.network :forwarded_port, guest: 27017, host: 27017
  end