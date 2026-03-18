import path from "node:path";

export function getProfilePath(env = process.env) {
  const base = env.LOCALAPPDATA || env.APPDATA;
  return path.join(base ?? "%LOCALAPPDATA%", "AcmeBench", "profile.json");
}
