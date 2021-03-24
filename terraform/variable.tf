# タイムスタンプ
variable "timestamp" { type=string }

/* ConoHaの認証情報

   ここで使用されるユーザ等の情報は、ConoHaコンソールにログインする際の情報とは異なる。
   API用のユーザ情報を使用する。
   APIユーザはConoHaのコントロールパネルのAPI > APIユーザー から新規に作成ができる。*/
# ConoHaコントロールパネル > API > APIユーザー > ユーザ名
variable "conoha_api_user_name" { type=string }
# ConoHaコントロールパネル > API > APIユーザー > パスワード
variable "conoha_api_password" { type=string }
# ConoHaコントロールパネル > API > API情報 > テナント名
variable "conoha_api_tenant_name" { type=string }
# ConoHaコントロールパネル > API > API情報 > エンドポイント > Identity Service
variable "conoha_api_auth_url" { type=string }

/* 作成するVPSの情報 */
# 使用するSSHキー
# Conohaコントロールパネル > セキュリティ > SSH Key に存在するもの(存在しない場合は作成)
variable "conoha_ssh_key_name" { type=string }
# VPSのOS等の種類
variable "vps_image_name" { type=string }
# メモリサイズ
variable "vps_memory_size" { type=string }
# 許可するポートの種類
variable "vps_security_groups" { type=list }
