import { chromium } from 'playwright';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const output = path.resolve(projectRoot, '../deliverables/images/prototype');
await mkdir(output, { recursive: true });
const executablePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const browser = await chromium.launch({ executablePath, headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
const errors = [];
page.on('pageerror', (error) => errors.push(error.message));
await page.goto('http://127.0.0.1:3000', { waitUntil: 'networkidle' });
await page.evaluate(() => fetch('/api/reset', { method: 'POST' }));
await page.reload({ waitUntil: 'networkidle' });
await page.getByRole('heading', { name: 'Bom dia. Como está a Maria?' }).waitFor();
await page.screenshot({ path: path.join(output, '01-visao-geral.png'), fullPage: true });

await page.getByRole('button', { name: 'Perfil do idoso' }).click();
await page.getByLabel('Condições de saúde relevantes').fill('Hipertensão e mobilidade reduzida');
await page.getByRole('button', { name: 'Guardar perfil' }).click();
await page.getByText('Perfil do idoso guardado com sucesso.').waitFor();
await page.screenshot({ path: path.join(output, '02-perfil-idoso.png'), fullPage: true });

await page.getByRole('button', { name: 'Contactos familiares' }).click();
await page.getByLabel('Nome completo').fill('Rita Silva');
await page.getByLabel('Parentesco').fill('Neta');
await page.getByLabel('Telefone').fill('915 111 222');
await page.getByLabel('Email (opcional)').fill('rita.silva@example.com');
await page.getByRole('button', { name: 'Adicionar contacto' }).click();
await page.getByText('Contacto familiar adicionado.').waitFor();
await page.screenshot({ path: path.join(output, '03-contactos-familiares.png'), fullPage: true });

await page.getByRole('button', { name: 'Tensão arterial' }).click();
await page.getByLabel('Sistólica').fill('138');
await page.getByLabel('Diastólica').fill('84');
await page.getByLabel('Pulso').fill('73');
await page.getByRole('button', { name: 'Registar medição' }).click();
await page.getByText('Medição registada e classificada.').waitFor();
await page.screenshot({ path: path.join(output, '04-tensao-arterial.png'), fullPage: true });

await page.getByRole('button', { name: 'Deteção de quedas' }).click();
await page.getByRole('button', { name: 'Simular queda' }).click();
await page.getByRole('heading', { name: 'Está tudo bem?' }).waitFor();
await page.screenshot({ path: path.join(output, '05-deteccao-queda.png'), fullPage: true });
await page.getByRole('button', { name: 'Foi falso alarme' }).click();
await page.getByText('Alerta encerrado como falso alarme.').waitFor();

await page.setViewportSize({ width: 390, height: 844 });
await page.getByRole('button', { name: 'Cuida+ — início' }).click();
await page.screenshot({ path: path.join(output, '06-mobile.png'), fullPage: true });
if (errors.length) throw new Error(errors.join('\n'));
console.log('6 capturas criadas; fluxos das 4 funcionalidades executados sem erros de browser.');
await browser.close();
