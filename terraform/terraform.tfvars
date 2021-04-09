# 認証用のエンドポイント
conoha_api_auth_url = "https://identity.tyo1.conoha.io/v2.0"
# 使用するOS(Ubuntu20.04)
vps_image_name = "vmi-ubuntu-20.04-amd64"
# メモリサイズ(Terraform上では1gb以上でないとメモリ不足となりうまく作成できない模様)
vps_memory_size = "g-1gb"

vps_security_groups = [
  # 許可: SSH接続用ポート(22)
  "gncs-ipv4-ssh",
  # 許可: WEB用ポート(20/21/80/443)
  "gncs-ipv4-web"
]
