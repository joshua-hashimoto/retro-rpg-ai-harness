import type { Plugin } from "@opencode-ai/plugin";

import { EDIT_TOOLS, writeLog, type WriteLogBody } from "./utils";

export const RuffAfterEditPlugin: Plugin = async ({ $, directory, client }) => {
  // NOTE: tool内部で共通的な情報があるので、メソッドでまとめる
  const createToolLog = () => {
    return (message: WriteLogBody["message"], extra: WriteLogBody["extra"]) => {
      writeLog({
        directory,
        body: {
          service: "RuffAfterEditPlugin",
          level: "Info",
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
      traceLog(`Calling 'tool.execute.after' hook`, {});

      const tool = input.tool;

      if (!EDIT_TOOLS.has(tool)) {
        traceLog("input.tool is not edit related. Stop plugin execution.", {
          tool,
        });
        return;
      }

      traceLog("Run ruff check...", {});
      // NOTE: Ruff CLIを実行。uvで仮想環境を管理してるため、uvを経由して実行する
      const response =
        await $`uv run ruff check ${directory} --select ALL --fix --output-format json`.nothrow();

      traceLog("ruff check complete.", { tool, ...response });

      // NOTE: エラーがない(exitCodeが0)であれば完了ログだけを出して処理を抜ける
      if (response.exitCode === 0) {
        // NOTE: 実行確認のためのログも出力
        traceLog("No error in ruff execution.", {});
        await client.app.log({
          body: {
            service: "RuffAfterEditPlugin",
            level: "info",
            message: "ruff execution successful",
            extra: {
              tool,
            },
          },
        });
        traceLog("Exeting plugin.", {});
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
          tool,
        });
        return;
      }
      // NOTE: AIにレスポンスを返却する必要がある。返却するレスポンスには
      //       1. sessionId
      //       2. 返却内容
      //       が必要になる。
      const issues = response.json();
      traceLog("Issues found in ruff check. Suggesting fixes.", {
        issues,
      });
      const message = `Fix the following ruff check errors. \n ${JSON.stringify(issues)}`;
      await client.session.prompt({
        path: {
          id: sessionId,
        },
        body: {
          parts: [
            {
              type: "text",
              text: message,
            },
          ],
        },
      });
    },
  };
};
