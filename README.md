## API 一覧

[ドキュメント](https://documenter.getpostman.com/view/7714348/UzBgvpkc)

## 事前設定

Postgresql をインストールしてください。

DEBUG モードなら`__devinit__.sql`を実行してください。
RELEASE モードならユーザーとロールを作成し`qiita`データーベースを作成してください。

## ライブラリインストール

ターミナルに`pip install -r requirements.txt`を入力し必要なライブラリをインストールしてください。

## マイグレーション

ターミナルに`python3 ./manage.py migrate`を入力しマイグレーションを実行してください。

## DEBUG モード実行

ターミナルに`python3 ./manage.py runserver 0.0.0.0:8000`で`localhost:8000`からサーバーが起動されます。

## RELEASE モード実行

フォルダーの中に`qiita_backend.ini`ファイルを作成してください。

中身は以下のようになります。

```
[uwsgi]
chdir=プロジェクトフォルダー
module=qiita_backend.wsgi
master=True
pidfile=/tmp/qiita_backend.pid
vacuum=True
max-requests=5000
```

ターミナルに`uwsgi --ini qiita_backend.ini`を入力してください。
