# キーバインド画像を作り直す

`images/*.svg` は、`layout/keymap.yaml` から `tools/gen_images.py` で生成する。
`ahk/` のキーバインドを変えたら、`layout/keymap.yaml` も同じように直し、リポジトリのルートで次を実行する。

```sh
uv run tools/gen_images.py
```

生成すると、`README.md` と `docs/思想.md` の画像リンクの末尾の `?v=` も画像の内容のハッシュに書き換わる。
GitHub の README は画像のキャッシュが残り、push しても古い画像を表示することがあるため、URL を変えてキャッシュを避けている。

## `layout/keymap.yaml` の書き方

`keyboard.rows` がキーの配置、`layers` がレイヤごとの割り当てを持つ。
`layers` の 1 つが画像 1 枚になる。

`layers[].keys` の各キーには、表示する文字（`to`）、補足（`sub`、省略可）、色を決める `kind` を書く。

| `kind` | 意味 |
|---|---|
| `remap` | 別のキーへの置き換え |
| `combo` | Ctrl や Shift と一緒に押したときだけ変わるもの |
| `modifier` | 修飾キー（押している間だけ別の割り当てに切り替えるキー） |
| `output` | 修飾キーを押している間に出力されるもの |
| `ahk` | AutoHotkey 自体の操作 |

キーの配置は概形で、実機を採寸したものではない。
