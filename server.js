import express from 'express';
import cors from 'cors';
import { analyzeIcon } from './api/analyze-icon.js';

const app = express();
const port = 3001; // Different from your Vite dev server port

app.use(cors());
app.use(express.json());

// Serve static files
app.use('/icons', express.static('icons'));
app.use('/_data', express.static('_data'));

// API endpoint
app.post('/api/analyze-icon', analyzeIcon);

app.listen(port, () => {
  console.log(`API server running at http://localhost:${port}`);
}); 