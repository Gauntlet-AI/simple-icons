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

    // Get the base URL from the request
    const protocol = request.headers['x-forwarded-proto'] || 'http';
    const baseUrl = `${protocol}://${request.headers.host}`;

    // Fetch SVG and JSON data from public URLs
    const [svgResponse, iconDataResponse] = await Promise.all([
      fetch(`${baseUrl}${svgPath}`),
      fetch(`${baseUrl}/_data/simple-icons.json`)
    ]);

    if (!svgResponse.ok || !iconDataResponse.ok) {
      throw new Error('Failed to fetch required files');
    }

    const svgBuffer = await svgResponse.arrayBuffer();
    const iconData = await iconDataResponse.json();

    // Find the matching icon
    const icon = iconData.find(
      (i) => i.title.toLowerCase() === title.toLowerCase(),
    );
    const brandColor = icon ? `#${icon.hex}` : '#000000';

    // Read the SVG as string and directly set the brand color
    let svgString = Buffer.from(svgBuffer).toString('utf-8');
    svgString = svgString.replace(/fill="[^"]*"/g, `fill="${brandColor}"`);
    if (!svgString.includes('fill="')) {
      svgString = svgString.replace(/<path/g, `<path fill="${brandColor}"`);
    }

    // Convert to PNG using Sharp
    const pngBuffer = await sharp(Buffer.from(svgString))
      .resize(512, 512)
      .png()
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
            'You are a helpful assistant that writes clear, specific product descriptions. Focus on what the company/product actually does, its main offering or service, and its target audience. Keep it to one concise but informative sentence.',
        },
        {
          role: 'user',
          content: `Write a specific one-sentence description for "${title}" that explains what they do or offer.`,
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
            `You are a concise design critic. Analyze icons focusing on key visual elements and effectiveness. The icon's color is ${brandColor}, and you should see that the image that has been passed to you has ${brandColor}, so comment on that specifically, and how ${brandColor} contributes to the design. Keep each point brief but insightful. Use markdown formatting. Always mention the brand color in your analysis.`,
        },
        {
          role: 'user',
          content: [
            {
              type: 'text',
              text: "Analyze this icon's design elements and effectiveness as a brand symbol. Focus on the most important aspects including its use of the brand color.",
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
    console.error('Error in icon analysis(!):', error);
    response.status(500).json({
      error: 'API Error',
      details: error.message,
    });
  }
} 