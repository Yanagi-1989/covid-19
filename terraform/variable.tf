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
/* VPSのOS等の種類

[1. トークンを取得]
参考: https://www.conoha.jp/docs/identity-post_tokens.php
CONOHA_API_USER_NAME="XXXXXXXXX"
CONOHA_API_PASSWORD="XXXXXXXXX"
CONOHA_TENANT_ID="XXXXXXXXX"
curl -X POST \
  -H "Accept: application/json" \
  -d "{\"auth\":{\"passwordCredentials\":{\"username\":\"${CONOHA_API_USER_NAME}\",
                                          \"password\":\"${CONOHA_API_PASSWORD}\"},
                 \"tenantId\":\"${CONOHA_TENANT_ID}\"}}" \
  https://identity.tyo1.conoha.io/v2.0/tokens \
  | jq ".access.token.id"

[2. 使用できるOSイメージ名一覧取得]
参考: https://www.conoha.jp/docs/compute-get_images_list.php
TOKEN="XXXXXXXXX"  # 先程取得したトークン
curl -X GET \
  -H "Accept: application/json" \
  -H "X-Auth-Token: ${TOKEN}" \
  https://compute.tyo1.conoha.io/v2/${CONOHA_TENANT_ID}/images \
  | jq ".images | sort_by(.name) | map(.name)" \
  | grep "vmi-ubuntu" | grep "20.04" */
variable "vps_image_name" { type=string }
# メモリサイズ
variable "vps_memory_size" { type=string }
# 許可するポートの種類
variable "vps_security_groups" { type=list }
