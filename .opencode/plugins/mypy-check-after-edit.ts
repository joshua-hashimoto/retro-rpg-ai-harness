import type { Plugin } from "@opencode-ai/plugin";

import { EDIT_TOOLS, writeLog, type WriteLogBody } from "./utils";

export const MypyCheckAfterEditPlugin: Plugin = async ({
  $,
  directory,
  client,
}) => {
  // NOTE: tool内部で共通的な情報があるので、メソッドでまとめる
  const createToolLog = () => {
    return (
      message: WriteLogBody["message"],
      options: {
        level?: WriteLogBody["level"];
        extra?: WriteLogBody["extra"];
      } = {},
    ) => {
      const { level = "info", extra = {} } = options;

      writeLog({
        directory,
        body: {
          service: "MypyCheckAfterEditPlugin",
          level,
          message,
          extra: {
            ...extra,
          },
        },
      });
    };
  };

  return {
    "tool.execute.after": async (input, output) => {
      const traceLog = createToolLog();
      traceLog(`Calling 'tool.execute.after' hook`);

      const tool = input.tool;

      if (!EDIT_TOOLS.has(tool)) {
        traceLog("input.tool is not edit related. Stop plugin execution.", {
          extra: {
            tool,
          },
        });
        return;
      }

      traceLog("Run task check:types...");
      // NOTE: Ruff CLIを実行。uvで仮想環境を管理してるため、uvを経由して実行する
      const result = await $`task check:types`.nothrow().quiet(); // ⚠️CAUTION: .quiet()がないとOpenCodeのTUIがおかしくなります

      traceLog("task check:types complete.", {
        extra: { tool, result },
      });

      // NOTE: エラーがない(exitCodeが0)であれば完了ログだけを出して処理を抜ける
      if (result.exitCode === 0) {
        // NOTE: 実行確認のためのログも出力
        traceLog("No error in ruff execution.");
        // IDEA: ここでclient.session.promptやclient.tui.showToastでpluginの実行の問題がなかったことを通知することもできる
        await client.tui.showToast({
          body: {
            message: "type checking has finished successfully",
            variant: "success",
          },
        });
        traceLog("Exeting plugin.");
        return;
      }

      // NOTE: エラーがある場合は内容をAIに返す
      //       この時、AIに修正するように指示を出すことで修正まで対応してくれる
      //       注意点として、このHookは上に修正指示の時にも実行される(ループする)
      //       そのため、問題が続くとループに入る可能性もある
      //       ループで修正する、がハーネスの基本だがトークン消費の問題もあるため、
      //       あまりに処理が長い場合は途中で止めるなどをした方が良い
      const sessionId = input.sessionID;
      if (!sessionId) {
        traceLog("No valid session id found.", {
          extra: { tool },
        });
        return;
      }
      // NOTE: Toastでユーザーに通知
      await client.tui.showToast({
        body: {
          message: "Type check failed; sending errors back to the agent",
          variant: "error",
        },
      });
      // NOTE: AIにレスポンスを返却する必要がある。返却するレスポンスには
      //       1. sessionId
      //       2. 返却内容
      //       が必要になる。
      const errorsJson = result.json();
      const errors = JSON.stringify(errorsJson);
      traceLog("Error found in linting.", {
        extra: { tool, errors },
      });
      await client.session.prompt({
        path: {
          id: sessionId,
        },
        body: {
          noReply: true,
          parts: [
            {
              type: "text",
              text: `Fix these mypy errors:\n${errors}`,
            },
          ],
        },
      });
    },
  };
};
