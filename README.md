# python-automation

BeautifulSoup と Playwright を使って Web サイトから情報を自動収集し、Markdown レポートとして保存する Python スクレイピングツールです。
robots.txt の遵守・ランダム待機・エラーログ出力など、実務を意識した設計になっています。

---

## 必要な環境

| 項目 | バージョン |
| --- | --- |
| Python | 3.14 以上（3.10 以上で動作可能） |
| requests | 2.34 以上 |
| beautifulsoup4 | 4.14 以上 |
| playwright | 1.60 以上 |

---

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone git@github.com:akihiro14/python-automation.git
cd python-automation
```

### 2. 仮想環境の作成と有効化

```bash
# 仮想環境を作成
python -m venv .venv

# 有効化（Windows）
.venv\Scripts\activate

# 有効化（Mac / Linux）
source .venv/bin/activate
```

### 3. ライブラリのインストール

```bash
pip install requests beautifulsoup4 playwright
```

### 4. Playwright 用ブラウザのインストール

```bash
playwright install chromium
```

---

## 実行方法

### scrape_books.py — 書籍情報のスクレイピング

[books.toscrape.com](https://books.toscrape.com/) から書籍タイトル・価格・在庫状況を全ページ取得します。

```bash
python scrape_books.py
```

**出力ファイル:**

| ファイル名 | 内容 |
| --- | --- |
| `books_YYYYMMDD.md` | 書籍一覧（タイトル・価格・在庫状況）|

---

### scrape_quotes.py — 名言のスクレイピング

[quotes.toscrape.com/js](https://quotes.toscrape.com/js)（JavaScript 描画ページ）から名言テキストと著者名を全ページ取得します。
実行するとブラウザが画面に表示されます。

```bash
python scrape_quotes.py
```

**出力ファイル:**

| ファイル名 | 内容 |
| --- | --- |
| `quotes_YYYYMMDD.md` | 名言一覧（テキスト・著者名）|
| `quotes_YYYYMMDD.png` | 1 ページ目のスクリーンショット |

---

## 設定できる項目

現在、設定は各スクリプト冒頭の定数で管理しています。`.env` ファイルによる外部設定にも対応予定です。

| 定数名 | デフォルト値 | 説明 |
| --- | --- | --- |
| `BASE_URL` | 各スクリプト参照 | スクレイピング対象のベース URL |
| `USER_AGENT` | `Mozilla/5.0 (compatible; ...)` | リクエスト時の User-Agent 文字列 |
| 待機時間 | `random.uniform(1, 3)` | リクエスト間のランダム待機秒数（1〜3 秒）|

> `.env` ファイルは Git 管理対象外です（`.gitignore` で除外済み）。機密情報は `.env` に記載してください。

---

## よくあるエラーと対処法

### `ConnectionError` / `接続エラー`

```
[ERROR] 接続エラー: ...
```

**原因:** ネットワーク接続の問題、または対象サイトがダウンしている。  
**対処:** インターネット接続を確認してから再実行してください。

---

### `playwright install` を忘れた

```
playwright._impl._errors.Error: Executable doesn't exist at ...
```

**原因:** ブラウザのバイナリがインストールされていない。  
**対処:**
```bash
playwright install chromium
```

---

### `ModuleNotFoundError: No module named 'playwright'`

**原因:** 仮想環境が有効化されていない、またはライブラリが未インストール。  
**対処:**
```bash
# 仮想環境を有効化
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Mac / Linux

# ライブラリをインストール
pip install requests beautifulsoup4 playwright
```

---

### `TimeoutError` / タイムアウト

```
[ERROR] タイムアウト: https://...
```

**原因:** ページの読み込みに時間がかかりすぎている。  
**対処:** ネットワーク状況を確認のうえ再実行してください。スクリプト内の `timeout` 値（ミリ秒）を大きくすることでも対応できます。

---

### robots.txt によりアクセスが禁止される

```
[WARNING] robots.txt によりアクセス禁止: https://...
```

**原因:** 対象 URL が robots.txt の `Disallow` に該当している。  
**対処:** 対象 URL を変更するか、robots.txt の内容を確認してください。アクセス禁止のパスへは意図的にアクセスしない設計になっています。
