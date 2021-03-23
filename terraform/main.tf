terraform {
  required_version = ">= 0.14.0"
  required_providers {
    openstack = {
      source = "terraform-provider-openstack/openstack"
      version = "~> 1.35.0"
    }
  }
}

/* 認証情報 */
provider "openstack" {
  user_name = var.conoha_api_user_name
  password = var.conoha_api_password
  tenant_name = var.conoha_api_tenant_name
  auth_url = var.conoha_api_auth_url
}

/* 作成するVPSの情報 */
resource "openstack_compute_instance_v2" "vps" {
  name = "vps"
  # OS、メモリ等の設定
  image_name = var.vps_image_name
  flavor_name = var.vps_memory_size

  # VPSのセキュリティ周りの設定
  security_groups = var.vps_security_groups
  key_pair = var.conoha_ssh_key_name

  metadata = {
    # ダッシュボードで表示される名前
    instance_name_tag = "covid19_${var.timestamp}"
  }
}
