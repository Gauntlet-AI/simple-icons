import OpenAI from 'openai';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs/promises';
import sharp from 'sharp';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize environment variables
dotenv.config({ path: path.join(__dirname, '../.env') });

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPEN_AI_KEY,
});

async function testVisionAPI() {
  try {
    // Read the SVG file and icon data
    const svgPath = path.join(__dirname, '../icons/afdian.svg');
    const iconDataPath = path.join(__dirname, '../_data/simple-icons.json');
    
    const [svgBuffer, iconDataText] = await Promise.all([
      fs.readFile(svgPath),
      fs.readFile(iconDataPath, 'utf-8')
    ]);
    
    // Parse icon data and find the afdian icon
    const icons = JSON.parse(iconDataText);
    const icon = icons.find(i => i.title.toLowerCase() === 'afdian');
    const brandColor = icon ? `#${icon.hex}` : '#000000';
    
    console.log('Icon found:', icon ? 'Yes' : 'No');
    
    // Convert SVG to PNG using Sharp with brand color
    const pngBuffer = await sharp(svgBuffer)
      .resize(512, 512)  // Resize to a reasonable size
      .png()
      .flatten({ background: '#ffffff' })  // Use white background
      .tint(brandColor)  // Apply brand color
      .toBuffer();
    
    // Convert to base64
    const base64Image = pngBuffer.toString('base64');
    const dataUrl = `data:image/png;base64,${base64Image}`;
    
    console.log('Making Vision API request...');
    console.log('Using API Key:', process.env.OPEN_AI_KEY ? 'Present' : 'Missing');
    console.log('Brand Color:', brandColor);
    
    const response = await openai.chat.completions.create({
      model: "gpt-4-turbo",
      messages: [{
        role: "user",
        content: [
          { type: "text", text: "What do you see in this icon? Please describe its visual elements and style." },
          { 
            type: "image_url",
            image_url: {
              url: dataUrl,
              detail: "high"
            }
          }
        ]
      }],
      max_tokens: 150,
    });

    console.log('\nAPI Response:');
    console.log('Status: Success');
    console.log('Description:', response.choices[0].message.content);
    
  } catch (error) {
    console.error('\nAPI Error:');
    console.error('Status:', error.status);
    console.error('Message:', error.message);
    console.error('Type:', error.type);
    if (error.response) {
      console.error('Response:', error.response.data);
    }
  }
}

// Run the test
console.log('Starting Vision API test...');
testVisionAPI(); 