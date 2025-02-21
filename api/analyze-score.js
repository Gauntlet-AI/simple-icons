import OpenAI from 'openai';

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
    const { productDescription, iconAnalysis } = request.body;

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

    const scoreData = JSON.parse(scoreResponse.choices[0].message.content);

    response.json({
      designScore: scoreData.score,
      scoreExplanation: scoreData.explanation,
    });
  } catch (error) {
    console.error('Error in score analysis:', error);
    response.status(500).json({
      error: 'API Error',
      details: error.message,
    });
  }
} 