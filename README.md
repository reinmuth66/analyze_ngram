# analyze_ngram

英字のn-gram頻度データを解析し、キーボード配列の検討に役立てるためのスクリプト集。

## スクリプト

### analyze_ngram.py

[English Letter Frequency Counts: Mayzner Revisited or ETAOIN SRHLDCU](https://norvig.com/mayzner.html) からダウンロードできる `ngrams1.tsv` を解析するスクリプト。指定した文字のunigram・bigram頻度をパーセンテージで出力する。

### replace_text.py

[Keyboard Layout Analyzer](https://patorjk.com/keyboard-layout-analyzer/#/main) で論理配列のスコアを計るために、[罪と罰](https://www.gutenberg.org/cache/epub/2554/pg2554.txt) のテキストを前処理するスクリプト。大文字を小文字に統一し、指定した記号・英数字・半角スペース以外の文字を除去する。

## セットアップ

### 必要環境

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)

### インストール

```bash
uv sync
```

## 使い方

### analyze_ngram.py

1. [English Letter Frequency Counts: Mayzner Revisited or ETAOIN SRHLDCU](https://norvig.com/mayzner.html) から `ngrams-all.tsv.zip` をダウンロード
```bash
curl -Lo data/ngrams-all.tsv.zip https://norvig.com/tsv/ngrams-all.tsv.zip
```
2. 展開する
```bash
gunzip -c data/ngrams-all.tsv.zip > data/ngrams1.tsv
```
3. `scripts/config.json` を編集して解析対象を設定
4. 実行

```bash
uv run scripts/analyze_ngram.py
```

#### `config.json` の設定項目

| キー | 型 | 説明 |
|------|----|------|
| `file` | string | 入力ファイルのパス |
| `chars` | string | 解析対象の文字を連結した文字列 |
| `groups_list` | string の配列 | 同一指などでグループ化する文字の組 |
| `exclude_chars` | string | bigramの集計から除外する文字。空欄で除外なし |
| `auto_exclude_chars` | bool | `true` にすると `chars` の末尾以外を自動で `exclude_chars` に設定 |
| `calc_unigram` | bool | unigram頻度を出力するか |
| `calc_bigram` | bool | bigram頻度を出力するか |

#### `config.json` の例

```json
{
  "file": "data/ngrams1.tsv",
  "chars": "zueiaol",
  "groups_list": ["ua", "zi"],
  "exclude_chars": "",
  "auto_exclude_chars": false,
  "calc_unigram": false,
  "calc_bigram": true
}
```

### replace_text.py

1. 処理したいテキストファイルを `data/input.txt` として配置
2. 必要に応じてスクリプト内の `symbols_to_keep` を編集する。デフォルト設定は`.,-`
3. 実行

```bash
uv run scripts/replace_text.py
```

処理結果は `data/output.txt` に出力される。
