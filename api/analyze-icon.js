import fs from 'node:fs/promises';
import path from 'node:path';
import OpenAI from 'openai';
import sharp from 'sharp';

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export default async function handler(request, response) {
  // Enable CORS
  response.setHeader('Access-Control-Allow-Credentials', true);
  response.setHeader('Access-Control-Allow-Origin', '*');
  response.setHeader('Access-Control-Allow-Methods', 'POST,OPTIONS');
  response.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  // Handle OPTIONS request for CORS
  if (request.method === 'OPTIONS') {
    response.status(200).end();
    return;
  }

  if (request.method !== 'POST') {
    return response.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { title, svgPath } = request.body;

    if (!title || !svgPath) {
      return response.status(400).json({
        error: 'Missing required fields: title and svgPath are required',
      });
    }

    // Read both the SVG file and icon data
    const [svgBuffer, iconDataText] = await Promise.all([
      fs.readFile(path.join(process.cwd(), svgPath)),
      fs.readFile(path.join(process.cwd(), '_data/simple-icons.json'), 'utf8'),
    ]);

    // Parse icon data and find the matching icon
    const icons = JSON.parse(iconDataText);
    const icon = icons.find(
      (i) => i.title.toLowerCase() === title.toLowerCase(),
    );
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
      model: 'gpt-4-turbo',
      messages: [
        {
          role: 'system',
          content:
            'You are a helpful assistant that writes clear, concise product descriptions.',
        },
        {
          role: 'user',
          content: `Write a one sentence description for a product/company called "${title}".`,
        },
      ],
      temperature: 0.7,
      max_tokens: 100,
    });

    // Then, analyze the icon
    const iconResponse = await openai.chat.completions.create({
      model: 'gpt-4-turbo',
      messages: [
        {
          role: 'system',
          content:
            'You are a concise design critic. Analyze icons focusing on key visual elements and effectiveness. Keep each point brief but insightful. Use markdown formatting.',
        },
        {
          role: 'user',
          content: [
            {
              type: 'text',
              text: "Analyze this icon's design elements and effectiveness as a brand symbol. Focus on the most important aspects.",
            },
            {
              type: 'image_url',
              image_url: {
                url: dataUrl,
                detail: 'high',
              },
            },
          ],
        },
      ],
      max_tokens: 500,
      temperature: 0.7,
    });

    const productDescription = descriptionResponse.choices[0].message.content;
    const iconAnalysis = iconResponse.choices[0].message.content;

    response.json({
      productDescription,
      iconAnalysis,
    });
  } catch (error) {
    console.error('Error in icon analysis:', error);
    response.status(500).json({
      error: 'API Error',
      details: error.message,
    });
  }
} 