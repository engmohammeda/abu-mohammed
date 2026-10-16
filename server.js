import express from 'express';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;
const HOST = '0.0.0.0';

const DATA_DIR = path.join(__dirname, 'data');
const LEADS_FILE = path.join(DATA_DIR, 'leads.json');

app.use(express.json({ limit: '16kb' }));
app.use(express.urlencoded({ extended: true }));

// Ensure data directory exists
try { fs.mkdirSync(DATA_DIR, { recursive: true }); } catch {}

function readLeads() {
  try {
    if (!fs.existsSync(LEADS_FILE)) return [];
    const raw = fs.readFileSync(LEADS_FILE, 'utf8');
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function writeLeads(leads) {
  fs.writeFileSync(LEADS_FILE, JSON.stringify(leads, null, 2), 'utf8');
}

// Simple in-memory rate limiter for lead submissions
const rateBucket = new Map();
function rateLimit(req, res, next) {
  const ip = req.ip || req.connection?.remoteAddress || 'unknown';
  const now = Date.now();
  const windowMs = 60 * 1000;
  const max = 5;
  const entry = rateBucket.get(ip) || { count: 0, reset: now + windowMs };
  if (now > entry.reset) { entry.count = 0; entry.reset = now + windowMs; }
  entry.count += 1;
  rateBucket.set(ip, entry);
  if (entry.count > max) {
    return res.status(429).json({ ok: false, error: 'too_many_requests' });
  }
  next();
}

app.get('/api/health', (_req, res) => {
  res.json({ ok: true, service: 'haraj-riyadh-mashabat', time: new Date().toISOString() });
});

// Lead capture endpoint used by the landing page and WhatsApp funnel.
app.post('/api/leads', rateLimit, (req, res) => {
  const { name, phone, service, message, source } = req.body || {};
  const clean = (v) => (typeof v === 'string' ? v.trim().slice(0, 500) : '');
  const lead = {
    id: `lead_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
    name: clean(name),
    phone: clean(phone),
    service: clean(service),
    message: clean(message),
    source: clean(source) || 'website',
    createdAt: new Date().toISOString(),
    status: 'new',
  };
  if (!lead.phone && !lead.message) {
    return res.status(400).json({ ok: false, error: 'phone_or_message_required' });
  }
  const leads = readLeads();
  leads.push(lead);
  try { writeLeads(leads); } catch (e) {
    return res.status(500).json({ ok: false, error: 'storage_failed' });
  }
  res.status(201).json({ ok: true, id: lead.id });
});

// Admin read endpoint (token via env or query for demo).
app.get('/api/leads', (req, res) => {
  const token = process.env.ADMIN_TOKEN || 'dev-token';
  const provided = req.query.token || req.headers['x-admin-token'];
  if (provided !== token) {
    return res.status(401).json({ ok: false, error: 'unauthorized' });
  }
  const leads = readLeads();
  res.json({ ok: true, count: leads.length, leads });
});

// Serve static assets
app.use(express.static(path.join(__dirname, 'docs')));
app.use('/haraj-riyadh-2026', express.static(path.join(__dirname, 'haraj-riyadh-2026')));

// Catch-all: serve index.html
app.get('*', (req, res) => {
  if (req.path.startsWith('/api/')) return res.status(404).json({ ok: false, error: 'not_found' });
  res.sendFile(path.join(__dirname, 'docs', 'index.html'));
});

app.listen(PORT, HOST, () => {
  console.log(`Server listening on http://${HOST}:${PORT}`);
});
