import Replicate from 'replicate';

// Initialize the Replicate client for CLIP
const replicate = new Replicate({
	auth: import.meta.env.VITE_REPLICATE_API_TOKEN,
});

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001';

type IconAnalysis = {
	productDescription: string;
	iconAnalysis: string;
	designScore: number;
};

/**
 * @param title
 * @param svgPath
 */
export async function analyzeIcon(
	title: string,
	svgPath: string,
): Promise<IconAnalysis> {
	try {
		const response = await fetch(`${API_URL}/api/analyze-icon`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({title, svgPath}),
		});

		if (!response.ok) {
			const errorData = await response
				.json()
				.catch(() => ({error: 'Failed to parse error response'}));
			throw new Error(
				errorData.error || `Failed to analyze icon: ${response.status}`,
			);
		}

		return response.json();
	} catch (error) {
		console.error('Error analyzing icon:', error);
		throw error;
	}
}

/**
 * @param productDescription
 * @param iconAnalysis
 */
export async function getDesignScore(
	productDescription: string,
	iconAnalysis: string,
): Promise<{designScore: number; scoreExplanation: string}> {
	try {
		const response = await fetch(`${API_URL}/api/analyze-score`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({productDescription, iconAnalysis}),
		});

		if (!response.ok) {
			const errorData = await response
				.json()
				.catch(() => ({error: 'Failed to parse error response'}));
			throw new Error(
				errorData.error || `Failed to get design score: ${response.status}`,
			);
		}

		return response.json();
	} catch (error) {
		console.error('Error getting design score:', error);
		throw error;
	}
}
