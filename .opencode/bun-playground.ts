/**
 * NOTE: Butの挙動確認用のファイル
 *       主に`$`の実行結果の挙動について確認を行なっている
 */
import { $ } from "bun";

console.log("------------- task check:lint -------------");
const lintCliResult = await $`task check:lint`.nothrow().quiet();
console.log("exitCode:", lintCliResult.exitCode);
if (lintCliResult.exitCode !== 0) {
  // NOTE: task check:lintはoutputフォーマットをjson指定してるため、`.json()`でjsonを出力できる
  const lintResult = lintCliResult.json();
  console.log(lintResult);
}

console.log("------------- task check:types -------------");
const typeCheckCliResult = await $`task check:types`.nothrow().quiet();
console.log("exitCode:", typeCheckCliResult.exitCode);
if (typeCheckCliResult.exitCode !== 0) {
  // NOTE: task check:typesはoutputフォーマットをjson指定してるため、`.json()`でjsonを出力できる
  const typeCheckResult = typeCheckCliResult.json();
  console.log(typeCheckResult);
}

console.log("------------- task check:imports -------------");
const lintImportsCliResult = await $`task check:imports`.nothrow().quiet();
console.log("exitCode:", lintImportsCliResult.exitCode);
if (lintImportsCliResult.exitCode !== 0) {
  // NOTE: task check:importsはoutputフォーマットを指定できずテキストでの出力のみ
  const lintImportsResult = lintImportsCliResult.text();
  console.log(lintImportsResult);
}
