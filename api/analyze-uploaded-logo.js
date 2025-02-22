import OpenAI from 'openai';
import sharp from 'sharp';
import multer from 'multer';
import { promisify } from 'util';

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Configure multer for file upload
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB limit
  },
  fileFilter: (req, file, cb) => {
    if (file.mimetype === 'image/svg+xml' || file.mimetype === 'image/png') {
      cb(null, true);
    } else {
      cb(new Error('Only SVG and PNG files are allowed'));
    }
  },
});

// Promisify multer middleware
const runMiddleware = promisify(upload.single('file'));

/**
 * @param {import('express').Request} request
 * @param {import('express').Response} response
 */
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
    // Handle file upload
    await runMiddleware(request, response);

    const { businessName, description, brandColor } = request.body;
    const file = request.file;

    if (!file || !businessName || !description) {
      return response.status(400).json({
        error: 'Missing required fields',
      });
    }

    // Convert SVG/PNG to PNG buffer for OpenAI
    let pngBuffer;
    if (file.mimetype === 'image/svg+xml') {
      // If SVG, apply brand color if provided
      let svgString = file.buffer.toString('utf-8');
      if (brandColor) {
        // First, ensure the path has a fill attribute
        if (!svgString.includes('fill="')) {
          svgString = svgString.replace(/<path/g, `<path fill="${brandColor}"`);
        } else {
          svgString = svgString.replace(/fill="[^"]*"/g, `fill="${brandColor}"`);
        }
        
        // Add a white background to ensure visibility
        svgString = svgString.replace(/<svg([^>]*)>/, `<svg$1><rect width="100%" height="100%" fill="white"/>`);
      }
      
      // Convert to PNG with white background and proper dimensions
      pngBuffer = await sharp(Buffer.from(svgString))
        .resize(512, 512, {
          fit: 'contain',
          background: { r: 255, g: 255, b: 255, alpha: 1 }
        })
        .png()
        .toBuffer();
    } else {
      // If PNG, resize with white background
      pngBuffer = await sharp(file.buffer)
        .resize(512, 512, {
          fit: 'contain',
          background: { r: 255, g: 255, b: 255, alpha: 1 }
        })
        .png()
        .toBuffer();
    }

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
            'You are a helpful assistant that writes clear, specific product descriptions. Focus on what the company/product actually does, its main offering or service, and its target audience. Keep it to one concise but informative sentence.',
        },
        {
          role: 'user',
          content: `Write a specific one-sentence description for "${businessName}" based on this description: "${description}"`,
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
            `You are a concise design critic. Analyze icons focusing on key visual elements, effectiveness, and how well they align with the business description. ${brandColor ? `The icon's color is ${brandColor}, and you should see that the image that has been passed to you has ${brandColor}, so comment on that specifically, and how ${brandColor} contributes to the design.` : ''} Keep each point brief but insightful. Use markdown formatting. ${brandColor ? 'Always mention the brand color in your analysis.' : ''} Consider how well the design elements support and reflect the business's purpose.`,
        },
        {
          role: 'user',
          content: [
            {
              type: 'text',
              text: `Analyze this icon's design elements and effectiveness as a brand symbol for the following business: "${description}". Focus on how well the visual elements align with and support the business's purpose and target audience.`,
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

    const productDescription = descriptionResponse.choices[0].message.content || '';
    const iconAnalysis = iconResponse.choices[0].message.content || '';

    // Get the design score
    const scoreResponse = await openai.chat.completions.create({
      model: 'gpt-4-turbo',
      messages: [
        {
          role: 'system',
          content:
            'You are a design critic focused on evaluating logos based on two key criteria: Memorability (ease of recognition and clarity) and Relevance (connection to the product/audience). Provide a score out of 100 and a brief 1-2 sentence explanation.',
        },
        {
          role: 'user',
          content: `Based on this product description and icon analysis, score the logo's effectiveness:

Product Description: ${productDescription}

Icon Analysis: ${iconAnalysis}

Focus on:
1. Memorability: Is it easy to recognize and uncluttered?
2. Relevance: Is the logo relevant to the target audience/product?

Respond with only a JSON object containing:
{
  "score": number,
  "explanation": "1-2 sentence explanation"
}`,
        },
      ],
      temperature: 0.7,
      max_tokens: 150,
    });

    const scoreData = JSON.parse(scoreResponse.choices[0].message.content || '{}');

    response.json({
      productDescription,
      iconAnalysis,
      designScore: scoreData.score,
      scoreExplanation: scoreData.explanation,
    });
  } catch (error) {
    console.error('Error in logo analysis:', error);
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    response.status(500).json({
      error: 'API Error',
      details: errorMessage,
    });
  }
} 