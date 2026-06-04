# python-automation

侍エンジニアの「Claude Codeでゼロから開発を学ぼう」コース用のPython自動化プロジェクト。

## プロジェクト概要

Pythonを使った自動化スクリプトの開発・学習プロジェクト。

## 技術スタック

- Python 3.x

## ディレクトリ構成

```
python-automation/
├── CLAUDE.md         # このファイル
├── .gitignore        # Git除外設定
├── .venv/            # Python仮想環境（Gitに含めない）
└── (スクリプト追加予定)
```

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
