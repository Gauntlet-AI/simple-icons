/**
 * Analyze an icon using the API
 * @param {string} title The title of the icon
 * @param {string} svgPath The path to the SVG file
 */
export async function analyzeIcon(title, svgPath) {
  const response = await fetch('/api/analyze-icon', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title, svgPath }),
  });

  if (!response.ok) {
    throw new Error('Failed to analyze icon');
  }

  return response.json();
}

/**
 * Get a design score for an icon
 * @param {string} productDescription The product description
 * @param {string} iconAnalysis The icon analysis
 */
export async function getDesignScore(productDescription, iconAnalysis) {
  const response = await fetch('/api/analyze-score', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ productDescription, iconAnalysis }),
  });

  if (!response.ok) {
    throw new Error('Failed to get design score');
  }

  return response.json();
}

/**
 * Analyze an uploaded logo
 * @param {File} file The uploaded file
 * @param {string} businessName The business name
 * @param {string} description The product description
 * @param {string} brandColor The brand color in hex format
 */
export async function analyzeUploadedLogo(file, businessName, description, brandColor) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('businessName', businessName);
  formData.append('description', description);
  formData.append('brandColor', brandColor);

  const response = await fetch('/api/analyze-uploaded-logo', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Failed to analyze uploaded logo');
  }

  return response.json();
} 