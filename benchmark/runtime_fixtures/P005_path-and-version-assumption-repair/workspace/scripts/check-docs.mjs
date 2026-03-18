import { readFileSync } from "node:fs";

const readme = readFileSync(new URL("../README.md", import.meta.url), "utf8");

const checks = [
  {
    name: "mentions current path",
    pass: readme.includes("%LOCALAPPDATA%\\AcmeBench\\profile.json"),
    failure: "README must mention %LOCALAPPDATA%\\AcmeBench\\profile.json"
  },
  {
    name: "mentions current version family",
    pass: readme.includes("AcmeBench 2.4.x") || readme.includes("AcmeBench 2.4.1"),
    failure: "README must mention the current 2.4.x version family"
  },
  {
    name: "removes stale path",
    pass: !readme.includes("%APPDATA%\\AcmeBench\\config.json"),
    failure: "README still contains the stale %APPDATA%\\AcmeBench\\config.json path"
  },
  {
    name: "removes stale version claim",
    pass: !readme.includes("AcmeBench 1.x"),
    failure: "README still contains the stale 1.x version claim"
  }
];

const failures = checks.filter((check) => !check.pass);
if (failures.length > 0) {
  for (const failure of failures) {
    console.error(`FAIL: ${failure.failure}`);
  }
  process.exit(1);
}

for (const check of checks) {
  console.log(`PASS: ${check.name}`);
}
