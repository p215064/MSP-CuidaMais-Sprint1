import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const vite = path.join(root, 'node_modules', 'vite', 'bin', 'vite.js');
const api = path.join(root, 'server', 'index.js');
const children = [
  spawn(process.execPath, [api], { cwd: root, stdio: 'inherit' }),
  spawn(process.execPath, [vite, ...process.argv.slice(2)], { cwd: root, stdio: 'inherit' })
];
let closing = false;
function close(code = 0) {
  if (closing) return;
  closing = true;
  children.forEach((child) => child.kill());
  setTimeout(() => process.exit(code), 150);
}
children.forEach((child) => child.on('exit', (code) => { if (!closing && code) close(code); }));
process.on('SIGINT', () => close());
process.on('SIGTERM', () => close());
