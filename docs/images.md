# キーバインド画像を作り直す

`images/*.svg` は、`layout/keymap.yaml` から `tools/gen_images.py` で生成する。
ファイル名には画像の内容のハッシュが入る（例: `images/base.3d9667a7.svg`）。
`ahk/` のキーバインドを変えたら、`layout/keymap.yaml` も同じように直し、リポジトリのルートで次を実行する。

```sh
uv run tools/gen_images.py
```

生成すると、`README.md` と `docs/思想.md` の画像リンクも新しいファイル名に書き換わり、同じ画像の古いハッシュ付きファイルは消える。
生成後は、消えたファイルも含めて `git add -A images` でコミットする。

ファイル名にハッシュを入れているのは、GitHub の README で画像のキャッシュを避けるため。
README の相対リンクの画像は `github.com/<リポジトリ>/raw/<ブランチ>/<パス>` から `raw.githubusercontent.com` へリダイレクトされ、このときクエリ文字列（`?v=` など）は落ちる。
リダイレクト先は `cache-control: max-age=300` で返るため、push 直後は古い画像を表示することがある（2026-11-08 に `curl -I` で確認）。
ファイル名を変えればリダイレクト先の URL も変わるので、キャッシュに当たらない。

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
