# retro-rpg-ai-harness
AIハーネスの例を提示するリポジトリ。そのままだとつまらないのでPythonで簡単なRPGアプリを作成

## 使用ツール

- mise
    - https://mise.jdx.dev/
    - 言語およびバージョン管理
    - 環境依存を減らすためmiseを使用
    - mise.tomlがある場合miseはそのファイルがあるディレクトリをルートとして、仮想環境のように扱う挙動をする
        - つまり環境変数や普段端末全体に入れるパッケージであるuvやlefthookをグローバルではなくプロジェクトに包含できる
    - **AIハーネスでのロール**
        - AIハーネス向けのロールはなし
        - しかしLLMはリポジトリをコンテキストにするため、現在のプロジェクトがどういう環境を想定しているのか、LLmも人間も想像しやすい
- uv
    - https://docs.astral.sh/uv/
    - pythonのパッケージ管理を担当
    - miseは環境の管理を行う、uvはpythonの管理を行う
    - **AIハーネスでのロール**
        - AIハーネス向けのロールはなし
        - uvは他のpythonパッケージ管理ツールよりも早い為、CLI実行などが早い。これがAIハーネスで有利になることあり
- ruff
    - Pythonのlinter兼formatter
    - AIハーネスの要の1つ
    - **AIハーネスでのロール**
        - AIハーネスでは「AIを制限する」ことが重要な考え方の1つ。ruffはlinterとformatterの機能を提供しているため、ハーネスの考え方では最重要の1つ。
- Task
    - https://taskfile.dev/
    - タスクランナー
    - makefileのような機能、ただしYAML記法が使えたりスピードが早かったり
    - miseのタスクランナーも使えるが一旦こちらで統一
    - CLIのインターフェースを統一することができる
    - **AIハーネスでのロール**
        - AIハーネス向けのロールはなし
        - ただし、AIハーネスではCLI実行も重要なポイントの1つ。その実行を簡単にしてくれるという意味では縁の下の力持ち的存在
- pydantic
    - https://pydantic.dev/docs/validation/latest/get-started/
    - pythonの型付け用
    - **AIハーネスでのロール**
- mypy
    - https://mypy.readthedocs.io/en/latest/index.html
    - pythonの型付け用
    - **AIハーネスでのロール**
        - pythonの型付けの正しさを監視するため、AIの生成するコードの正しさを補強することができる
- import-linter
    - https://import-linter.readthedocs.io/en/stable/
    - Pythonのimport方向を制限できる
        - これを行うことでimport地獄からの解放が可能
        - AI側でもimport方向の強制をする事ことでアーキテクチャを強制することができる
    - AIハーネスの要の1つ
    - **AIハーネスでのロール**
        - importの方向に制限をかけることで期待しないファイルやディレクトリからのimportを制限できる
        - 最終的にコードは人間が確認するもの、ディレクトリのアーキテクチャを綺麗にしておくことは常に優先順位の上に起きたい
        - このディレクトリアーキテクチャの守るために使用
- lefthook
    - https://github.com/evilmartians/lefthook
    - AIハーネスの要の1つ
    - **AIハーネスでのロール**
        - AIハーネスをしっかりと行っていればgitフックを使った確認は不要に感じる。しかし、実際にAIハーネスをセットアップするのは人間。そのため、最終的に全部を最後の最後で確認するためにgitフックを使ったチェックを実行するのは良い考えと言える

## AI Agent

OpenCode

## Plugins

- SuperPowers

## カスタムPlugins

- app-router.ts
- env-protection.ts
- ruff-after-edit.ts

## MCPs

- Context 7 MCP
- Tavily MCP

## 環境変数

環境変数の管理は`.env`ファイルで行う。

```env
# MCP
CONTEXT7_API_KEY=
TAVILY_API_KEY=
```

