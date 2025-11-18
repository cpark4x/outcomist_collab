import express from 'express';
import cors from 'cors';
import Anthropic from '@anthropic-ai/sdk';
import Database from 'better-sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize database
const dbPath = path.join(__dirname, '../canvas-collab.db');
const db = new Database(dbPath);

// Initialize database schema
db.exec(`
  CREATE TABLE IF NOT EXISTS workspaces (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS widgets (
    id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    type TEXT NOT NULL,
    position_x REAL NOT NULL,
    position_y REAL NOT NULL,
    width REAL NOT NULL,
    height REAL NOT NULL,
    data TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
  );
`);

// Initialize Anthropic client
const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) {
  console.warn('Warning: ANTHROPIC_API_KEY not set');
}
const anthropic = apiKey ? new Anthropic({ apiKey }) : null;

// Active agent streams
const activeStreams = new Map();

// Workspace routes
app.post('/api/workspaces', (req, res) => {
  const { name } = req.body;
  const id = crypto.randomUUID();

  const stmt = db.prepare('INSERT INTO workspaces (id, name) VALUES (?, ?)');
  stmt.run(id, name);

  res.json({ id, name, createdAt: new Date().toISOString() });
});

app.get('/api/workspaces', (req, res) => {
  const workspaces = db.prepare('SELECT * FROM workspaces ORDER BY updated_at DESC').all();
  res.json(workspaces);
});

app.get('/api/workspaces/:id', (req, res) => {
  const workspace = db.prepare('SELECT * FROM workspaces WHERE id = ?').get(req.params.id);
  if (!workspace) {
    return res.status(404).json({ error: 'Workspace not found' });
  }

  const widgets = db.prepare('SELECT * FROM widgets WHERE workspace_id = ?').all(req.params.id);
  res.json({ ...workspace, widgets });
});

app.put('/api/workspaces/:id', (req, res) => {
  const { name } = req.body;
  const stmt = db.prepare('UPDATE workspaces SET name = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?');
  const result = stmt.run(name, req.params.id);

  if (result.changes === 0) {
    return res.status(404).json({ error: 'Workspace not found' });
  }

  res.json({ success: true });
});

// Widget routes
app.post('/api/widgets', (req, res) => {
  const { workspaceId, type, positionX, positionY, width, height, data } = req.body;
  const id = crypto.randomUUID();

  const stmt = db.prepare(`
    INSERT INTO widgets (id, workspace_id, type, position_x, position_y, width, height, data)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `);
  stmt.run(id, workspaceId, type, positionX, positionY, width, height, JSON.stringify(data || {}));

  res.json({ id, workspaceId, type, positionX, positionY, width, height, data });
});

app.put('/api/widgets/:id', (req, res) => {
  const { positionX, positionY, width, height, data } = req.body;
  const stmt = db.prepare(`
    UPDATE widgets
    SET position_x = ?, position_y = ?, width = ?, height = ?, data = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
  `);
  const result = stmt.run(positionX, positionY, width, height, JSON.stringify(data || {}), req.params.id);

  if (result.changes === 0) {
    return res.status(404).json({ error: 'Widget not found' });
  }

  res.json({ success: true });
});

app.delete('/api/widgets/:id', (req, res) => {
  const stmt = db.prepare('DELETE FROM widgets WHERE id = ?');
  const result = stmt.run(req.params.id);

  if (result.changes === 0) {
    return res.status(404).json({ error: 'Widget not found' });
  }

  res.json({ success: true });
});

// Claude AI routes
app.post('/api/agent/send', async (req, res) => {
  if (!anthropic) {
    return res.status(500).json({ error: 'Anthropic API key not configured' });
  }

  const { widgetId, message } = req.body;

  // Set up SSE
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  try {
    const stream = await anthropic.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 8192,
      messages: [{ role: 'user', content: message }],
      stream: true,
    });

    // Store stream for potential cancellation
    activeStreams.set(widgetId, stream);

    for await (const event of stream) {
      if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
        res.write(`data: ${JSON.stringify({ type: 'output', text: event.delta.text })}\n\n`);
      }
    }

    res.write(`data: ${JSON.stringify({ type: 'complete' })}\n\n`);
    res.end();
  } catch (error) {
    res.write(`data: ${JSON.stringify({ type: 'error', message: error.message })}\n\n`);
    res.end();
  } finally {
    activeStreams.delete(widgetId);
  }
});

app.post('/api/agent/stop', (req, res) => {
  const { widgetId } = req.body;
  const stream = activeStreams.get(widgetId);

  if (stream && stream.controller) {
    stream.controller.abort();
    activeStreams.delete(widgetId);
  }

  res.json({ success: true });
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', anthropicConfigured: !!anthropic });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
  console.log(`Anthropic API: ${anthropic ? 'Configured' : 'Not configured'}`);
});
