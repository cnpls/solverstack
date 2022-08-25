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

    config.vm.network :forwarded_port, guest: 3000, host: 3000
  
    config.vm.provision "shell", inline: <<-SHELL
      apt-get update -y
      apt-get upgrade -y
      apt-get dist-upgrade -y
      cd /vagrant
      curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
      echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
      sudo apt-get -y update && sudo apt-get -y install yarn
      yarn install
    SHELL

    end