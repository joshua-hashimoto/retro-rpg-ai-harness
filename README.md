# retro-rpg-ai-harness
AIハーネスの例を提示するリポジトリ。そのままだとつまらないのでPythonで簡単なRPGアプリを作成

## 使用ツール

- mise
    - https://mise.jdx.dev/
    - 言語およびバージョン管理
    - 環境依存を減らすためmiseを使用
- uv
- ruff
    - Pythonのlinter兼formatter
    - AIハーネスの要の1つ
- Task
    - https://taskfile.dev/
    - タスクランナー
    - makefileのような機能、ただしYAML記法が使えたりスピードが早かったり
    - miseのタスクランナーも使えるが、一旦こちらで統一
- pydantic
- mypy
- import-linter
    - Pythonのimport方向を制限できる
        - これを行うことでimport地獄からの解放が可能
        - AI側でもimport方向の強制をする事ことでアーキテクチャを強制することができる
    - AIハーネスの要の1つ
- left

## AI Agent

OpenCode

## Plugins

- SuperPowers

## カスタムPlugins

- app-router.ts
- ruff-after-edit.ts

## MCPs

- Serena MCP

