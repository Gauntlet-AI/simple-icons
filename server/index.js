import express from 'express';
import cors from 'cors';
import OpenAI from 'openai';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs/promises';
import sharp from 'sharp';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize environment variables with explicit path to root .env
dotenv.config({ path: path.join(__dirname, '../.env') });

// Initialize API clients
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from the dist directory after building
app.use(express.static(path.join(__dirname, '../dist')));

// API endpoint for icon analysis
app.post('/api/analyze-icon', async (req, res) => {
  try {
    const { title, svgPath } = req.body;

    if (!title || !svgPath) {
      return res.status(400).json({ 
        error: 'Missing required fields: title and svgPath are required' 
      });
    }

    // Read both the SVG file and icon data
    const [svgBuffer, iconDataText] = await Promise.all([
      fs.readFile(path.join(__dirname, '..', svgPath)),
      fs.readFile(path.join(__dirname, '../_data/simple-icons.json'), 'utf-8')
    ]);

    // Parse icon data and find the matching icon
    const icons = JSON.parse(iconDataText);
    const icon = icons.find(i => i.title.toLowerCase() === title.toLowerCase());
    const brandColor = icon ? `#${icon.hex}` : '#000000';

    // Convert SVG to PNG using Sharp with brand color
    const pngBuffer = await sharp(svgBuffer)
      .resize(512, 512)
      .png()
      .flatten({ background: '#ffffff' })
      .tint(brandColor)
      .toBuffer();

    // Convert to base64
    const base64Image = pngBuffer.toString('base64');
    const dataUrl = `data:image/png;base64,${base64Image}`;

    // First, get a product description
    const descriptionResponse = await openai.chat.completions.create({
      model: "gpt-4-turbo",
      messages: [{
        role: "system",
        content: "You are a helpful assistant that writes clear, concise product descriptions."
      }, {
        role: "user",
        content: `Write a one sentence description for a product/company called "${title}".`
      }],
      temperature: 0.7,
      max_tokens: 100,
    });

    // Then, analyze the icon
    const iconResponse = await openai.chat.completions.create({
      model: "gpt-4-turbo",
      messages: [{
        role: "system",
        content: "You are an expert design critic. Analyze icons in terms of their visual elements, symbolism, and effectiveness. Format your response in markdown with appropriate headings, bullet points, and emphasis where relevant."
      }, {
        role: "user",
        content: [
          { type: "text", text: "Analyze this icon in terms of its design elements, visual style, and effectiveness as a brand symbol. Structure your response with sections for Visual Elements, Style, and Brand Effectiveness." },
          { 
            type: "image_url",
            image_url: {
              url: dataUrl,
              detail: "high"
            }
          }
        ]
      }],
      max_tokens: 250,
    });

    // Calculate a design score based on certain keywords in the analysis
    const analysis = iconResponse.choices[0].message.content;
    const positiveKeywords = ['clean', 'simple', 'minimal', 'modern', 'effective', 'balanced', 'professional', 'distinctive', 'memorable', 'elegant'];
    const negativeKeywords = ['busy', 'complex', 'cluttered', 'confusing', 'unclear', 'amateur', 'unbalanced', 'generic'];
    
    let score = 70; // Base score
    const foundPositive = [];
    const foundNegative = [];
    
    positiveKeywords.forEach(keyword => {
      if (analysis.toLowerCase().includes(keyword)) {
        score += 3;
        foundPositive.push(keyword);
      }
    });
    negativeKeywords.forEach(keyword => {
      if (analysis.toLowerCase().includes(keyword)) {
        score -= 5;
        foundNegative.push(keyword);
      }
    });
    
    // Ensure score stays within 0-100 range
    score = Math.max(0, Math.min(100, score));

    // Generate score explanation
    let scoreExplanation = '';
    if (foundPositive.length > 0) {
      scoreExplanation += `Positive aspects include being ${foundPositive.slice(0, -1).join(', ')}${foundPositive.length > 1 ? ' and ' : ''}${foundPositive.slice(-1)[0]}. `;
    }
    if (foundNegative.length > 0) {
      scoreExplanation += `Areas for improvement: the design appears ${foundNegative.slice(0, -1).join(', ')}${foundNegative.length > 1 ? ' and ' : ''}${foundNegative.slice(-1)[0]}. `;
    }
    if (foundPositive.length === 0 && foundNegative.length === 0) {
      scoreExplanation = 'This icon has a balanced design with no strongly positive or negative characteristics.';
    }

    res.json({
      productDescription: descriptionResponse.choices[0].message.content,
      iconAnalysis: analysis,
      designScore: score,
      scoreExplanation
    });

  } catch (error) {
    console.error('Error in icon analysis:', error);
    res.status(500).json({ 
      error: 'API Error',
      details: error.message 
    });
  }
});

// Handle all other routes by serving the main index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../dist/index.html'));
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
}); 