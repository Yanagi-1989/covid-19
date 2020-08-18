#!/bin/bash
# cronを設定するスクリプト
# TODO: そのうちAnsibleで実装

USER="vagrant"
USER_HOME="/home/${USER}"


sudo apt update -y
sudo apt upgrade -y

sudo timedatectl set-timezone Asia/Tokyo

# ===========
# pyenvインストール

# pyenv及びpyenvにてインストールするPythonに必要なパッケージをインストール
# [参照]
# https://github.com/pyenv/pyenv/wiki/Common-build-problems
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
                    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
                    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

# pyenvをインストールし、パスを設定
git clone git://github.com/yyuu/pyenv.git ${USER_HOME}/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ${USER_HOME}/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ${USER_HOME}/.bash_profile
echo 'eval "$(pyenv init -)"' >> ${USER_HOME}/.bash_profile
source ${USER_HOME}/.bash_profile

# Pythonバージョンを固定
pyenv install 3.8.5
pyenv global 3.8.5

pip install pipenv
pipenv install --system

# ===========
# sqlite3ファイルを前もって生成
GEN_DB_SCRIPT="/home/${USER}/.pyenv/shims/python /home/${USER}/covid-19/cron/run.py"
${GEN_DB_SCRIPT}


# ===========
# cron設定


# Cronにて実行する内容
# 1時間間毎にsqlite3ファイルを生成
CRON_SCRIPT="0 */1 * * * ${USER} ${GEN_DB_SCRIPT}"
CRON_FILE="/etc/cron.d/sqlite3_csv"
# cronを設定
echo "# sqlite3のDBファイルを1分間毎に生成" | sudo tee -a  ${CRON_FILE}
echo "${CRON_SCRIPT}" | sudo tee -a  ${CRON_FILE}

# cron再起動
sudo service cron restart
sudo service cron status
