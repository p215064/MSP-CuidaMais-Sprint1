import { promises as fs } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const dirname = path.dirname(fileURLToPath(import.meta.url));
const defaultFile = path.join(dirname, 'data', 'db.json');

export const initialState = () => ({
  elder: {
    id: 'elder-1', name: 'Maria Silva', birthDate: '1946-05-12',
    phone: '912 345 678', address: 'Rua das Flores, 12, Porto',
    conditions: 'Hipertensão', notes: 'Usa andarilho. Prefere contacto telefónico.'
  },
  contacts: [
    { id: 'contact-1', name: 'Ana Silva', relationship: 'Filha', phone: '913 456 789', email: 'ana.silva@example.com', priority: 1 },
    { id: 'contact-2', name: 'João Silva', relationship: 'Filho', phone: '914 567 890', email: 'joao.silva@example.com', priority: 2 }
  ],
  readings: [
    { id: 'reading-1', systolic: 128, diastolic: 78, pulse: 72, measuredAt: '2026-10-25T08:30:00.000Z' },
    { id: 'reading-2', systolic: 135, diastolic: 82, pulse: 75, measuredAt: '2026-10-24T18:15:00.000Z' },
    { id: 'reading-3', systolic: 131, diastolic: 80, pulse: 70, measuredAt: '2026-10-24T08:20:00.000Z' },
    { id: 'reading-4', systolic: 126, diastolic: 77, pulse: 69, measuredAt: '2026-10-23T08:10:00.000Z' }
  ],
  falls: []
});

export class Store {
  constructor(file = process.env.DB_FILE || defaultFile) {
    this.file = file;
    this.state = initialState();
  }

  async init() {
    try {
      this.state = JSON.parse(await fs.readFile(this.file, 'utf8'));
    } catch (error) {
      if (error.code !== 'ENOENT') throw error;
      await this.save();
    }
    return this;
  }

  async save() {
    await fs.mkdir(path.dirname(this.file), { recursive: true });
    const temporary = `${this.file}.tmp`;
    await fs.writeFile(temporary, JSON.stringify(this.state, null, 2));
    await fs.rename(temporary, this.file);
  }

  async reset() {
    this.state = initialState();
    await this.save();
    return this.state;
  }
}
