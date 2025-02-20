import OpenAI from 'openai';
import Replicate from 'replicate';

// Initialize the OpenAI client
const openai = new OpenAI({
  apiKey: import.meta.env.OPEN_AI_KEY,
  dangerouslyAllowBrowser: true  // Note: For production, use a backend server instead
});

// Initialize the Replicate client for CLIP
const replicate = new Replicate({
  auth: import.meta.env.VITE_REPLICATE_API_TOKEN,
});

interface IconAnalysis {
  productDescription: string;
  iconAnalysis: string;
  designScore: number;
}

export async function analyzeIcon(title: string, svgPath: string): Promise<IconAnalysis> {
  try {
    const response = await fetch('http://localhost:3001/api/analyze-icon', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title, svgPath }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Failed to parse error response' }));
      throw new Error(errorData.error || `Failed to analyze icon: ${response.status}`);
    }

    return response.json();
  } catch (error) {
    console.error('Error analyzing icon:', error);
    throw error;
  }
} 