import sharp from 'sharp';
import fs from 'fs/promises';
import path from 'path';

async function testColorIcon() {
  try {
    // Read the Orange SVG and JSON data directly from files
    const svgContent = await fs.readFile('icons/orange.svg', 'utf-8');
    const jsonContent = await fs.readFile('_data/simple-icons.json', 'utf-8');
    const iconData = JSON.parse(jsonContent);

    // Find the Orange icon data
    const icon = iconData.find(i => i.title === 'Orange');
    const brandColor = `#${icon.hex}`; // Should be #FF7900
    console.log(`Testing with Orange icon, brand color: ${brandColor}`);

    // Create output directory if it doesn't exist
    await fs.mkdir('test-output', { recursive: true });

    // Parse hex color into RGB
    const hex = brandColor.replace('#', '');
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);

    // Try multiple approaches:

    // Test 1: Direct color in SVG
    let svgString1 = svgContent.replace(/fill="[^"]*"/g, `fill="${brandColor}"`);
    if (!svgString1.includes('fill="')) {
      svgString1 = svgString1.replace(/<path/g, `<path fill="${brandColor}"`);
    }
    await fs.writeFile('test-output/test1.svg', svgString1);
    await sharp(Buffer.from(svgString1))
      .resize(512, 512)
      .png()
      .toFile('test-output/test1.png');

    // Test 2: Using tint
    let svgString2 = svgContent.replace(/fill="[^"]*"/g, 'fill="currentColor"');
    if (!svgString2.includes('fill="')) {
      svgString2 = svgString2.replace(/<path/g, '<path fill="currentColor"');
    }
    await fs.writeFile('test-output/test2.svg', svgString2);
    await sharp(Buffer.from(svgString2))
      .resize(512, 512)
      .tint({ r, g, b })
      .png()
      .toFile('test-output/test2.png');

    // Test 3: Using both fill and tint
    await sharp(Buffer.from(svgString1))
      .resize(512, 512)
      .tint({ r, g, b })
      .png()
      .toFile('test-output/test3.png');

    // Test 4: Using composite
    await sharp(Buffer.from(svgString2))
      .resize(512, 512)
      .composite([{
        input: Buffer.from(svgString2),
        blend: 'over'
      }])
      .tint({ r, g, b })
      .png()
      .toFile('test-output/test4.png');

    console.log('Test files generated in test-output directory:');
    console.log('- test1.png: Direct color in SVG');
    console.log('- test2.png: Using tint');
    console.log('- test3.png: Using both fill and tint');
    console.log('- test4.png: Using composite and tint');
    console.log('\nCheck these files to see which approach produces the best result.');

  } catch (error) {
    console.error('Error running test:', error);
  }
}

testColorIcon(); 