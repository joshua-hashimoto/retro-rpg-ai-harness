import type { Plugin } from "@opencode-ai/plugin";

import { writeLog, type WriteLogBody } from "./utils";

export const EnvProtectionPlugin: Plugin = async ({ directory, client }) => {
  // NOTE: tool内部で共通的な情報があるので、メソッドでまとめる
  const createToolLog = () => {
    return (message: WriteLogBody["message"], extra: WriteLogBody["extra"]) => {
      writeLog({
        directory,
        body: {
          service: "EnvProtectionPlugin",
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
    "tool.execute.before": async (input, output) => {
      const traceLog = createToolLog();
      const tool = input.tool;
      // NOTE: 実行確認のためのログも出力
      traceLog("Calling tool.execute.before", {
        tool,
      });

      const isReadTool = tool === "read";
      const filePath: string | null = output?.args?.filePath;
      traceLog("Evaluating read file", { filePath });
      const hasEnvInFilePath = filePath?.includes(".env");
      if (isReadTool && hasEnvInFilePath) {
        const errorMessage = "Cannot read .env file";
        // NOTE: 実行確認のためのログも出力
        traceLog(errorMessage, {});
        throw new Error(errorMessage);
      }
    },
  };
};
