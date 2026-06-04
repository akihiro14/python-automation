# python-automation

侍エンジニアの「Claude Codeでゼロから開発を学ぼう」コース用のPython自動化プロジェクト。

## プロジェクト概要

Pythonを使った自動化スクリプトの開発・学習プロジェクト。

## 技術スタック

- Python 3.x

## ディレクトリ構成

```
python-automation/
├── CLAUDE.md              # このファイル
├── README.md              # プロジェクト説明（セットアップ・実行方法）
├── .gitignore             # Git除外設定
├── .venv/                 # Python仮想環境（Gitに含めない）
├── scrape_books.py        # BeautifulSoupスクレイピングスクリプト
├── scrape_quotes.py       # Playwrightスクレイピングスクリプト
├── books_YYYYMMDD.md      # 書籍スクレイピング結果
├── quotes_YYYYMMDD.md     # 名言スクレイピング結果
└── quotes_YYYYMMDD.png    # 名言ページのスクリーンショット
```

## スクリプト一覧

### scrape_quotes.py

[quotes.toscrape.com/js](https://quotes.toscrape.com/js) から名言をPlaywrightでスクレイピングするスクリプト。

**機能:**
- robots.txt を読み込み、禁止パスへのアクセスを回避
- JavaScriptで描画される名言（テキスト・著者名）を全ページ（10ページ / 100件）取得
- 1ページ目のスクリーンショットを `quotes_YYYYMMDD.png` として保存
- リクエスト間に 1〜3 秒のランダム待機
- 接続エラー・タイムアウト発生時はログ出力して終了
- 結果を `quotes_YYYYMMDD.md` として保存

**実行方法:**
```bash
.venv\Scripts\activate
python scrape_quotes.py
```

**依存ライブラリ:**
- `playwright`
- `requests`

---

### scrape_books.py

[books.toscrape.com](https://books.toscrape.com/) から書籍情報をスクレイピングするスクリプト。

**機能:**
- robots.txt を読み込み、禁止パスへのアクセスを回避
- 書籍タイトル・価格・在庫状況を全ページ（50ページ / 1000件）取得
- リクエスト間に 1〜3 秒のランダム待機
- 接続エラー発生時はログ出力して終了
- 結果を `books_YYYYMMDD.md` として保存

**実行方法:**
```bash
.venv\Scripts\activate
python scrape_books.py
```

**依存ライブラリ:**
- `requests`
- `beautifulsoup4`

## 仮想環境

```bash
# 仮想環境の有効化（Windows）
.venv\Scripts\activate

# 仮想環境の無効化
deactivate
```

## Git運用ルール

- コードを変更するたびに、必ずGitHubリポジトリにプッシュする
- リモートリポジトリ: `git@github.com:akihiro14/python-automation.git`
- コミットメッセージは変更内容を簡潔に日本語または英語で記述する

### 基本的なGitフロー

```bash
git add .
git commit -m "変更内容の説明"
git push origin main
```

## 開発ルール

- 回答するたびにこのCLAUDE.mdを最新状態に更新する
- .envファイルには機密情報を記載し、Gitには含めない
- node_modulesはGitに含めない
