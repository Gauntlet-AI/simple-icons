import OpenAI from 'openai';
import sharp from 'sharp';
import fs from 'fs/promises';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

async function testVisionColor() {
  try {
    // Read the Orange SVG and JSON data
    const svgContent = await fs.readFile('icons/orange.svg', 'utf-8');
    const jsonContent = await fs.readFile('_data/simple-icons.json', 'utf-8');
    const iconData = JSON.parse(jsonContent);

    // Find the Orange icon data
    const icon = iconData.find(i => i.title === 'Orange');
    const brandColor = `#${icon.hex}`; // Should be #FF7900
    console.log(`Testing with Orange icon, expected color: ${brandColor}`);

    // Color the SVG (using the method we confirmed works)
    let svgString = svgContent;
    svgString = svgString.replace(/fill="[^"]*"/g, `fill="${brandColor}"`);
    if (!svgString.includes('fill="')) {
      svgString = svgString.replace(/<path/g, `<path fill="${brandColor}"`);
    }

    // Convert to PNG
    const pngBuffer = await sharp(Buffer.from(svgString))
      .resize(512, 512)
      .png()
      .toBuffer();

    // Convert to base64
    const base64Image = pngBuffer.toString('base64');
    const dataUrl = `data:image/png;base64,${base64Image}`;

    // Ask GPT-4V about the color
    const response = await openai.chat.completions.create({
      model: 'gpt-4-turbo',
      messages: [
        {
          role: 'user',
          content: [
            {
              type: 'text',
              text: 'What color is this icon? Please be specific and mention if you see the color as orange (#FF7900) or if you see it as black or some other color.',
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
      max_tokens: 100,
    });

    console.log('\nGPT-4V Response:');
    console.log(response.choices[0].message.content);

  } catch (error) {
    console.error('Error running test:', error);
  }
}

testVisionColor(); 