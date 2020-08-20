# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/xenial64"
  config.vm.synced_folder "../covid-19", "/home/vagrant/covid-19"
  # Flaskをローカル起動させた場合のポート番号
  config.vm.network :forwarded_port, guest: 5000, host: 5000

  config.vm.provider "virtualbox" do |vb|
    vb.name = "vagrant_covid19"
    vb.memory = "2048"
  end

end
