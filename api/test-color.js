import sharp from 'sharp';

export default async function handler(request, response) {
  // Enable CORS
  response.setHeader('Access-Control-Allow-Credentials', true);
  response.setHeader('Access-Control-Allow-Origin', '*');
  response.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS');
  response.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (request.method === 'OPTIONS') {
    response.status(200).end();
    return;
  }

  try {
    // Let's use a test icon - Orange's icon since it has a distinctive color
    const svgPath = '/icons/orange.svg';
    const jsonPath = '/_data/simple-icons.json';
    
    // Get the base URL from the request
    const protocol = request.headers['x-forwarded-proto'] || 'http';
    const baseUrl = `${protocol}://${request.headers.host}`;

    // Fetch SVG and JSON data
    const [svgResponse, iconDataResponse] = await Promise.all([
      fetch(`${baseUrl}${svgPath}`),
      fetch(`${baseUrl}${jsonPath}`)
    ]);

    if (!svgResponse.ok || !iconDataResponse.ok) {
      throw new Error('Failed to fetch required files');
    }

    const svgBuffer = await svgResponse.arrayBuffer();
    const iconData = await iconDataResponse.json();

    // Find the Orange icon data
    const icon = iconData.find(i => i.title === 'Orange');
    const brandColor = `#${icon.hex}`; // Should be #FF7900

    // Parse hex color into RGB
    const hex = brandColor.replace('#', '');
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);

    // Try multiple approaches to color the SVG:

    // Approach 1: Direct color in SVG
    let svgString1 = Buffer.from(svgBuffer).toString('utf-8');
    svgString1 = svgString1.replace(/fill="[^"]*"/g, `fill="${brandColor}"`);
    if (!svgString1.includes('fill="')) {
      svgString1 = svgString1.replace(/<path/g, `<path fill="${brandColor}"`);
    }

    // Approach 2: Using currentColor
    let svgString2 = Buffer.from(svgBuffer).toString('utf-8');
    svgString2 = svgString2.replace(/fill="[^"]*"/g, 'fill="currentColor"');
    if (!svgString2.includes('fill="')) {
      svgString2 = svgString2.replace(/<path/g, '<path fill="currentColor"');
    }

    // Generate multiple test versions
    const results = await Promise.all([
      // Test 1: Direct color in SVG
      sharp(Buffer.from(svgString1))
        .resize(512, 512)
        .png()
        .toBuffer(),

      // Test 2: Using tint
      sharp(Buffer.from(svgString2))
        .resize(512, 512)
        .tint({ r, g, b })
        .png()
        .toBuffer(),

      // Test 3: Using both fill and tint
      sharp(Buffer.from(svgString1))
        .resize(512, 512)
        .tint({ r, g, b })
        .png()
        .toBuffer(),

      // Test 4: Using composite
      sharp(Buffer.from(svgString2))
        .resize(512, 512)
        .composite([{
          input: Buffer.from(svgString2),
          blend: 'over'
        }])
        .tint({ r, g, b })
        .png()
        .toBuffer()
    ]);

    // Convert all results to base64
    const images = results.map(buffer => 
      `data:image/png;base64,${buffer.toString('base64')}`
    );

    // Return HTML page with all versions for comparison
    response.setHeader('Content-Type', 'text/html');
    response.send(`
      <html>
        <body style="background: #f0f0f0; padding: 20px;">
          <h1>Color Test Results for Orange Icon (${brandColor})</h1>
          <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
            ${images.map((img, i) => `
              <div style="background: white; padding: 20px; border-radius: 8px; text-align: center;">
                <h2>Test ${i + 1}</h2>
                <img src="${img}" style="width: 200px; height: 200px;" />
              </div>
            `).join('')}
          </div>
        </body>
      </html>
    `);

  } catch (error) {
    console.error('Error in test coloring:', error);
    response.status(500).json({
      error: 'API Error',
      details: error.message
    });
  }
} 