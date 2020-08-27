# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/xenial64"
  config.vm.synced_folder "../covid-19", "/home/vagrant/covid-19"
  config.vm.network "private_network", ip: "192.168.33.10"
  # Flaskをローカル起動させた場合のポート番号
  config.vm.network :forwarded_port, guest: 5000, host: 5000
  # Nginx + uWSGIにてFlaskプロジェクトをローカル起動させた場合のポート番号
  config.vm.network :forwarded_port, guest: 80, host: 80

  config.vm.provider "virtualbox" do |vb|
    vb.name = "vagrant_covid19"
    vb.memory = "2048"
  end

  config.vm.provision "ansible" do |ansible|
    ansible.ask_become_pass = false
    ansible.playbook = "ansible/site.yml"
    ansible.groups = {
      "local" => ["default"]
    }
  end
end
