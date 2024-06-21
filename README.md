# Meal Shield

## アプリケーションの操作
### ソースコードへのアクセス
1. ダウンロード：`git clone https://github.com/al22-1B-01/meal_shield.git`
2. ソースコードへの移動：`cd meal_shield`
### APIキーの設定
1. APIキーの取得：`https://platform.openai.com/settings/profile?tab=api-keys`へアクセスしAPIキーを取得
    - 参考：https://nicecamera.kidsplates.jp/help/6648/
2. APIキーの設定：`cp backend/env.sample backend/.env`
3. `backend/.env`へのAPIキーの記載
### dockerコンテナの起動
1. `docker compose up -d --build`
### コンテナの起動、停止
1. Starting : `docker compose start`
2. Stopping : `docker compose stop`
### アプリケーションへの作成
`http://localhost:8080/`へブラウザでアクセス
