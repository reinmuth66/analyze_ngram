import json
from itertools import combinations

import pandas as pd


def analyze_ngrams_custom(
    file_path: str,
    chars: list,
    groups_list: list = None,
    exclude_chars: list = None,
    auto_exclude_chars: bool = False,
    calc_unigram: bool = True,
    calc_bigram: bool = True,
) -> None:
    if groups_list is None:
        groups_list = []
    if exclude_chars is None:
        exclude_chars = []

    # 全て小文字に統一
    chars = [c.lower() for c in chars]
    groups_list = [[c.lower() for c in g] for g in groups_list]
    if auto_exclude_chars:
        if len(chars) > 1:
            exclude_chars = chars[:-1]
        else:
            exclude_chars = []
    else:
        # Falseの場合は、config.jsonで指定された exclude_chars を使用する
        exclude_chars = [c.lower() for c in exclude_chars]

    print(f"{file_path} を読み込み中")
    df = pd.read_csv(file_path, sep="\t", usecols=["1-gram", "*/*"], low_memory=False)
    df = df.dropna(subset=["1-gram", "*/*"])
    df["1-gram"] = df["1-gram"].astype(str).str.lower()

    df["*/*"] = pd.to_numeric(df["*/*"], errors="coerce")
    df["*/*"] = df["*/*"].fillna(0).astype(int)

    freq_series = df.groupby("1-gram")["*/*"].sum()
    keys = freq_series.index.tolist()
    values = freq_series.tolist()
    freq_dict = {str(k): int(v) for k, v in zip(keys, values)}

    # 全体の基準となる合計頻度を算出
    total_unigram_base = sum(
        v for k, v in freq_dict.items() if len(k) == 1 and k.isalpha()
    )
    total_bigram_base = sum(
        v for k, v in freq_dict.items() if len(k) == 2 and k.isalpha()
    )

    # unigram の処理
    if calc_unigram:
        print("\nunigram")
        unigram_freqs = {c: int(freq_dict.get(c, 0)) for c in chars}

        for k, v in sorted(unigram_freqs.items(), key=lambda x: x[1], reverse=True):
            pct = (v / total_unigram_base * 100) if total_unigram_base > 0 else 0
            print(f"  {k}: {pct:.2f}%")

    # bigram の処理
    if calc_bigram:
        print("\nbigram")
        pair_freqs = []

        # グループに属している文字を平坦化
        flattened_groups = [c for g in groups_list for c in g]
        # グループに属していない単独の文字
        other_chars = [c for c in chars if c not in flattened_groups]

        # カテゴリとそれに属する文字リストの対応辞書を作成
        cat_to_chars = {c: [c] for c in other_chars}
        for g in groups_list:
            name = f"({'/'.join(g)})"
            cat_to_chars[name] = g

        categories = list(cat_to_chars.keys())

        # 異なるカテゴリ間の組み合わせ
        for pair in combinations(categories, 2):
            c1, c2 = pair
            list1 = cat_to_chars[c1]
            list2 = cat_to_chars[c2]

            total = 0
            details = {}
            for x in list1:
                for y in list2:
                    if x in exclude_chars and y in exclude_chars:
                        continue
                    b1 = x + y
                    b2 = y + x
                    f1 = int(freq_dict.get(b1, 0))
                    f2 = int(freq_dict.get(b2, 0))

                    if f1 > 0 or f2 > 0:
                        total += f1 + f2
                        details[b1] = f1
                        details[b2] = f2

            if details:
                total = sum(details.values())

                pair_freqs.append(
                    {"pair_name": f"{c1} {c2}", "total": total, "details": details}
                )

        # 足した合計頻度の降順で全体のペアをソート
        pair_freqs.sort(key=lambda x: x["total"], reverse=True)

        for p in pair_freqs:
            # ペアの合計頻度とそのパーセンテージ
            pct_pair = (
                (p["total"] / total_bigram_base * 100) if total_bigram_base > 0 else 0
            )
            print(f"{p['pair_name']}: {pct_pair:.3f}%")

            # 内訳の頻度とそのパーセンテージ
            for k, v in sorted(p["details"].items(), key=lambda x: x[1], reverse=True):
                pct_detail = (
                    (v / total_bigram_base * 100) if total_bigram_base > 0 else 0
                )
                print(f"  {k}: {pct_detail:.3f}%")
            print()


def main():
    with open("scripts/config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    file = config["file"]
    chars = list(config["chars"])
    groups_list = [list(g) for g in config["groups_list"]]
    exclude_chars = list(config["exclude_chars"])
    auto_exclude_chars = config["auto_exclude_chars"]
    calc_unigram = config["calc_unigram"]
    calc_bigram = config["calc_bigram"]

    analyze_ngrams_custom(
        file_path=file,
        chars=chars,
        groups_list=groups_list,
        exclude_chars=exclude_chars,
        auto_exclude_chars=auto_exclude_chars,
        calc_unigram=calc_unigram,
        calc_bigram=calc_bigram,
    )


if __name__ == "__main__":
    main()
