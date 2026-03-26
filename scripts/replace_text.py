import re


def replace_text(input_file, output_file, allowed_symbols):
    """
    指定されたテキストファイルを処理し、別のファイルに出力する
    """
    # UTF-8でファイルを読み込む
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    # 大文字を全て小文字に置換
    text = text.lower()

    # 改行を削除
    text = text.replace("\n", "").replace("\r", "")

    # 指定した記号、英数字、半角スペース以外を削除
    pattern = f"[^a-z0-9 {re.escape(allowed_symbols)}]"
    text = re.sub(pattern, "", text)

    # 処理結果を書き出す
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

    print(output_file)


def main():
    input_file_path = "data/input.txt"
    output_file_path = "data/output.txt"
    symbols_to_keep = ".,-"
    replace_text(input_file_path, output_file_path, symbols_to_keep)


if __name__ == "__main__":
    main()
