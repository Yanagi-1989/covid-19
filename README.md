# covid-19
新型コロナウイルス感染症（COVID-19）


## deploy
1. ConoHaにてサーバを追加
1. `~/.ssh/config`の`conoha_covid19`の`HostName`を編集
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
