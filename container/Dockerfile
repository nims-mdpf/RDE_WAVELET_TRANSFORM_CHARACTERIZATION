# Python Verison: 3.13
# python 3.13.7-slim-bookworm for linux/amd64
FROM python@sha256:5fa2567616c8d0e9a9470c8b4c1cb8b6f4d9f2fd45a548df393bed3537a7a324

ARG PIP_TRUSTED_HOST

# appディレクトリを作成
RUN mkdir /app
WORKDIR /app

# 必要なPythonライブラリのインストール
RUN pip install --upgrade pip
COPY requirements.txt /app
RUN pip install -r requirements.txt

# プログラムや設定ファイルなどをコピーする
COPY main.py /app
COPY modules/ /app/modules/
