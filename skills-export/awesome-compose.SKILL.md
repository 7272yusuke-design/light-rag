```markdown
---
name: awesome-compose
description: 特定の技術スタック（React+Go, Django+PostgreSQL, Spring Boot+MySQL等）を組み合わせたDocker Compose構成の雛形を生成・参照したいときに必ずこのスキルを使え。50以上のサンプル構成からMulti-stage Dockerfile・Docker Secrets・Reverse Proxyのベストプラクティスを即座に適用できる。
---

# awesome-compose

## 概要
Docker公式が提供するCompose構成のサンプルアプリケーション集（50以上）。Angular・React・Vue.js・Django・Flask・FastAPI・Spring Boot・Rust・Go等を組み合わせたcompose.yaml構成例を提供し、`docker compose up` 一発でローカル開発環境を即時起動できる。各サンプルはMulti-stage Dockerfile・Docker Secrets・Reverse Proxy等のベストプラクティスを実装済み。

## いつ使うか
- 「React + Go + PostgreSQLの構成をDocker Composeで作りたい」など特定スタックの雛形を求められたとき
- 新規プロジェクトのローカル開発環境をDocker Composeで構築する指示があったとき
- `compose.yaml` のベストプラクティス（healthcheck・secrets・depends_on）を参照・適用するとき
- nginxリバースプロキシでフロント・APIを統合するパターンが必要なとき
- Multi-stage DockerfileやDocker Secretsの実装例が必要なとき
- 既存のcompose.yamlをレビュー・改善するとき

## 利用可能なサンプル構成

### フロントエンド + バックエンド + DB
- `react-express-mongodb/` — React + Express + MongoDB
- `react-express-mysql/` — React + Express + MySQL
- `react-rust-postgres/` — React + Rust + PostgreSQL
- `react-java-mysql/` — React + Java + MySQL
- `angular-spring-postgres/` — Angular + Spring Boot + PostgreSQL
- `vue-spring-postgres/` — Vue.js + Spring Boot + PostgreSQL

### フロントエンド + バックエンド（DBなし）
- `react-nginx/` — React + nginx（静的配信）
- `nginx-golang/` — nginx + Go API
- `nginx-flask/` — nginx + Flask API
- `nginx-aspnet-mysql/` — nginx + ASP.NET + MySQL

### バックエンド + DB
- `flask-redis/` — Flask + Redis
- `fastapi/` — FastAPI単体
- `django/` — Django単体
- `spring-postgres/` — Spring Boot + PostgreSQL

### 単体・ツール系
- `prometheus-grafana/` — Prometheus + Grafana監視スタック
- `traefik-golang/` — Traefik + Go（動的リバースプロキシ）
- `elasticsearch-logstash-kibana/` — ELK Stack
- `wireguard/` — WireGuard VPN
- `minecraft/` — Minecraft Server

## 主要コマンド

```bash
# サンプルを起動する
cd react-express-mongodb/
docker compose up --build

# バックグラウンド起動
docker compose up -d --build

# 停止（ボリューム保持）
docker compose down

# 停止 + ボリューム削除（DB初期化）
docker compose down -v

# 構文バリデーション（展開済み設定を確認）
docker compose config

# 特定サービスのログ確認
docker compose logs -f backend

# サービス状態確認
docker compose ps
```

## 構成パターン

### compose.yaml の基本構造（4層: proxy + frontend + backend + db）

```yaml
services:
  proxy:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend
      - backend

  frontend:
    build:
      context: ./frontend
      target: dev-envs

  backend:
    build:
      context: ./backend
      target: dev-envs
    secrets:
      - db-password
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15-alpine
    secrets:
      - db-password
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5
    volumes:
      - db-data:/var/lib/postgresql/data

secrets:
  db-password:
    file: db/password.txt

volumes:
  db-data:
```

### Multi-stage Dockerfile

```dockerfile
# ビルドステージ
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 開発環境ステージ
FROM node:18-alpine AS dev-envs
RUN apk add --no-cache git
WORKDIR /app
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "server.js"]
```

### nginx リバースプロキシ

```nginx
server {
    listen 80;
    location / {
        proxy_pass http://frontend:3000;
    }
    location /api/ {
        proxy_pass http://backend:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## ワークフロー例

### 新規プロジェクトにcompose構成を追加する

1. 使用技術を確認（例: React + FastAPI + PostgreSQL）
2. ディレクトリ構成を作成:
   ```
   my-project/
   ├── compose.yaml
   ├── frontend/
   │   └── Dockerfile
   ├── backend/
   │   └── Dockerfile
   ├── nginx/
   │   └── nginx.conf
   └── db/
       └── password.txt
   ```
3. シークレットを設定:
   ```bash
   echo "mysecretpassword" > db/password.txt
   echo "db/password.txt" >> .gitignore
   ```
4. 上記の構成パターンを参考にcompose.yaml・Dockerfile・nginx.confを作成
   - `secrets` + `healthcheck` + `depends_on condition` は必ずセットで設定
5. 動作確認:
   ```bash
   docker compose up --build
   docker compose ps          # すべてhealthyか確認
   curl http://localhost      # フロントエンド
   curl http://localhost/api/ # バックエンドAPI
   ```

### 既存サンプルをベースにカスタマイズする

1. 上記「利用可能なサンプル構成」から対象スタックに近いものを選択
2. compose.yamlとDockerfileの構造を確認
3. プロジェクト固有の設定を変更（ポート番号・環境変数・ボリューム）
4. バリデーション:
   ```bash
   docker compose config   # YAML構文と変数展開を確認
   docker compose up --build
   ```

### 既存compose.yamlを改善する

1. healthcheckの有無を確認 → 未設定ならDB等に追加
2. パスワードが `environment` に直書きされていたら `secrets` に移行
3. `depends_on` を `condition: service_healthy` 付きに変更
4. Dockerfileがsingle-stageなら Multi-stage（builder + runtime）に分離
5. `docker compose config` で最終確認

## 注意点

- **`db/password.txt` は必ず `.gitignore` に追加する**。コミットするとシークレットが漏洩する
- **`depends_on` だけでは起動順序を保証できない**。DBの準備完了を待つには `condition: service_healthy` と `healthcheck` を必ずセットで設定する
- **Multi-stageの `target` 指定を忘れない**。compose.yamlの `build.target` を省略すると最終ステージが使われ、意図しない結果になる
- **ポートの競合に注意**。複数サンプルを同時起動すると80・3000・5432等が衝突する。同時起動は1つに絞るか、ポートを変更する
- **ボリュームの残留**。`docker compose down` ではボリュームが残る。DB初期化時は `-v` を付ける
- **nginxの `proxy_pass` ホスト名はサービス名と一致させる**。compose.yamlのサービス名がDocker内部DNSになる
- **本番環境への直接適用は非推奨**。dev-envsステージはDocker Desktop向け開発設定を含む。本番では専用のproductionステージを別途作成すること
- **`docker-compose.yml` より `compose.yaml` を使う**。Docker Compose V2以降は `compose.yaml` が推奨ファイル名

## 関連スキル

- **docker**: 個別コンテナのビルド・実行・デバッグ
- **nginx**: リバースプロキシ・ロードバランサーの詳細設定
- **postgresql**: DB初期化・マイグレーション管理
- **traefik**: 動的リバースプロキシ（一部サンプルで使用）
- **github-actions**: compose構成を使ったCI/CDパイプライン構築
```

---

**改善点サマリー:**

| 基準 | 改善前 | 改善後 |
|---|---|---|
| description | スタック列挙が一般的 | 「50以上のサンプル構成から」と具体性追加、3パターン明示 |
| 行数 | 198行 ✓ | ~180行 ✓（冗長な部分を整理） |
| コマンド例 | `docker compose config` が本文中のみ | コマンドセクションに移動、`curl`確認も追加 |
| ワークフロー | 2つ→汎用的 | 3つに増加（新規構築・カスタマイズ・既存改善）、改善ワークフローが実践的 |
| 注意点 | 7項目 | 8項目（`compose.yaml` vs `docker-compose.yml` 追加） |
| **新規追加** | — | 「利用可能なサンプル構成」セクション：具体的なディレクトリ名一覧でスタック選定を即座に支援 |
| 関連スキル | react/golang/pythonが雑 | 実在しそうなスキルに絞り、説明を簡潔化 |
