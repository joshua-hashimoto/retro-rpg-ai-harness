# AGENTS.md

## コード品質

このプロジェクトは ruff / mypy / import-linter / pydantic を使用しており、フックで自動チェックされる。
**最初から準拠したコードを書くこと。**詳細な設定は `ruff.toml` と `pyproject.toml` を参照。

### スタイル (ruff)

- すべての関数・メソッドの引数と戻り値に型注釈を付ける。
- すべての公開関数・クラス・モジュールに1行 docstring を書く。
- `tests/` 配下は型注釈・docstring 不要。

### 型 (mypy)

- `Any` を避け、具体的な型または `TypeVar` / ジェネリクスを使う。
- `Optional[X]` より `X | None` を使う。

### データモデル (pydantic)

- データ構造は `pydantic.BaseModel` サブクラスで定義する。辞書やデータクラスは使わない。

### モジュール境界 (import-linter)

- 依存方向: `app.models` → `app.game` の一方向のみ許可。逆方向のインポートは禁止。
