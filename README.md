# covid-19
新型コロナウイルス感染症（COVID-19）の感染者数をカレンダー風に表示

## 環境等
- サーバ: ConoHa VPS (個人開発のため金銭上の都合)
- サーバOS: Ubuntu20.04
- 言語: Python3.8.5
- WEBフレームワーク: Flask

## インスタンス作成
### 必要な情報を変数に設定
1. ConoHaAPIの認証情報を設定  
   ConoHaのログインユーザとは別に、前もってAPIユーザを作成しておく必要がある。  
   作成方法等の詳細は[このファイル](./terraform/variable.tf)のコメントを参照。
   ```bash
   # ConoHaコントロールパネル > API > APIユーザー > ユーザ名
   export CONOHA_API_USER_NAME="XXXXXXXXX"
   # ConoHaコントロールパネル > API > APIユーザー > パスワード
   export CONOHA_API_PASSWORD="XXXXXXXXX"
   # ConoHaコントロールパネル > API > API情報 > テナント名
   export CONOHA_API_TENANT_NAME="XXXXXXXXX"
   ```
1. 作成するVPSのSSH接続に使う鍵情報を設定  
   これも前もって作成しておく必要がある。  
   作成方法等の詳細は[このファイル](./terraform/variable.tf)のコメントを参照。
   ```bash
   # Conohaコントロールパネル > セキュリティ > SSH Key に存在するもの(存在しない場合は作成)
   export CONOHA_SSH_KEY_NAME="XXXXXXXXX"
   ```

### Terraformを実行
1. Terraform環境を構築
   ```bash
   cd terraform
   terraform init
   ```
1. 作成されるVPSの内容をチェック
   ```bash
   terraform plan \
     -out=tfplan \
     -var-file="terraform.tfvars" \
     -var timestamp=$(date '+%Y-%m-%d') \
     -var conoha_api_user_name=${CONOHA_API_USER_NAME} \
     -var conoha_api_password=${CONOHA_API_PASSWORD} \
     -var conoha_api_tenant_name=${CONOHA_API_TENANT_NAME} \
     -var conoha_ssh_key_name=${CONOHA_SSH_KEY_NAME}
   ```
1. 問題無いようであれば、VPS作成を実行
   ```bash
   terraform apply -auto-approve "tfplan"
   ```
1. 作成したVPSのグローバルIPアドレスを取得。  
   ```bash
   terraform show | grep access_ip_v4
   ```

## deploy
1. `~/.ssh/config`の、このプロジェクト用VPSの`Host`、  
   `conoha_covid19`の`HostName`を作成もしくは編集
   ```
   # 例
   Host conoha_covid19
       HostName		[Terraformにて作成したVPSのグローバルIP]
       User			root
       IdentityFile	~/.ssh/XXXXXX.pem
   ```
1. 当プロジェクトのトップディレクトリに移動
1. 以下のコマンドを実行
   ```bash
   cd ansible
   # conohaはコンソールに入らずにroot以外のユーザを追加する方法が無い
   ansible -m ping -u root -i hosts vps
   ansible-playbook -u root -i hosts site.yml
   ```
1. WEBブラウザにて新規に作成したサーバにのIPにアクセスし、画面が表示されることを確認
1. ConoHaにて、新しいサーバの接続許可ポートをWEBのみに設定
1. ConoHaにて、ネットワーク > ロードバランサー > バランシング元ポート80 > バランシング先IPアドレスに、  
   新規作成したサーバを追加し、以前のIPを削除
1. ConoHaにて、古いサーバを削除


## ローカル開発環境作成
以下のコマンドを実行
```bash
vagrant up
# うまくいかなかった場合は以下を実行
vagrant provision
```
