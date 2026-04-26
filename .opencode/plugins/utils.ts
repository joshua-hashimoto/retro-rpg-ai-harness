import { appendFile, mkdir } from "node:fs/promises";
import { join } from "node:path";

import dayjs from "dayjs";

export const EDIT_TOOLS = new Set([
  "edit",
  "write",
  "patch",
  "apply_patch",
  "multiedit",
]);

export type WriteLogBody = {
  service: string;
  level: string;
  message: string;
  extra: Record<string, unknown>;
};

export type WriteLog = {
  directory: string;
  body: WriteLogBody;
};

export const writeLog = async ({ directory, body }: WriteLog) => {
  const logDir = join(directory, "logs/opencode");
  await mkdir(logDir, { recursive: true });
  const now = dayjs().format("YYYY-MM-DD");
  const logFile = join(logDir, `plugin-debug_${now}.log`);
  await appendFile(logFile, `${JSON.stringify(body)}\n`);
};
