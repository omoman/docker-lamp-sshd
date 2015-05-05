Vagrant.configure(2) do |config|
  config.vm.box = "chef/centos-7.0"
  config.vm.network "forwarded_port", guest: 8082, host: 8080
  config.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
  end
end
