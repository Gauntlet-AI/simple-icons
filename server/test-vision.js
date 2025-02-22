import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import dotenv from 'dotenv';
import OpenAI from 'openai';
import sharp from 'sharp';
import FormData from 'form-data';
import fetch from 'node-fetch';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize environment variables
dotenv.config({path: path.join(__dirname, '../.env')});

// Initialize OpenAI client
const openai = new OpenAI({
	apiKey: process.env.OPENAI_API_KEY,
});

/**
 *
 */
async function testVisionAPI() {
	try {
		// Read the SVG file and icon data
		const svgPath = path.join(__dirname, '../icons/afdian.svg');
		const iconDataPath = path.join(__dirname, '../_data/simple-icons.json');

		const [svgBuffer, iconDataText] = await Promise.all([
			fs.readFile(svgPath),
			fs.readFile(iconDataPath, 'utf8'),
		]);

		// Parse icon data and find the afdian icon
		const icons = JSON.parse(iconDataText);
		const icon = icons.find((i) => i.title.toLowerCase() === 'afdian');
		const brandColor = icon ? `#${icon.hex}` : '#000000';

		console.log('Icon found:', icon ? 'Yes' : 'No');

		// Convert SVG to PNG using Sharp with brand color
		const pngBuffer = await sharp(svgBuffer)
			.resize(512, 512) // Resize to a reasonable size
			.png()
			.flatten({background: '#ffffff'}) // Use white background
			.tint(brandColor) // Apply brand color
			.toBuffer();

		// Convert to base64
		const base64Image = pngBuffer.toString('base64');
		const dataUrl = `data:image/png;base64,${base64Image}`;

		console.log('Making Vision API request...');
		console.log(
			'Using API Key:',
			process.env.OPENAI_API_KEY ? 'Present' : 'Missing',
		);
		console.log('Brand Color:', brandColor);

		const response = await openai.chat.completions.create({
			model: 'gpt-4-turbo',
			messages: [
				{
					role: 'user',
					content: [
						{
							type: 'text',
							text: 'What do you see in this icon? Please describe its visual elements and style.',
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

async function testAnalyzeUploadedLogo() {
	try {
		// Read the test SVG file
		const svgBuffer = await fs.readFile(path.join(__dirname, '../docs/sheild.svg'));
		
		// Create form data
		const formData = new FormData();
		formData.append('file', svgBuffer, {
			filename: 'shield.svg',
			contentType: 'image/svg+xml',
		});
		formData.append('businessName', 'GauntletAI');
		formData.append('description', 'Gauntlet AI is an extremely intensive 12-week AI training to turn engineers into the most sought-after builders and entrepreneurs on the planet.');
		formData.append('brandColor', '#000000');

		// Make the request
		const response = await fetch('http://localhost:3001/api/analyze-uploaded-logo', {
			method: 'POST',
			body: formData,
		});

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const data = await response.json();
		console.log('Test Results:');
		console.log('-------------');
		console.log('Product Description:', data.productDescription);
		console.log('-------------');
		console.log('Icon Analysis:', data.iconAnalysis);
		console.log('-------------');
		console.log('Design Score:', data.designScore);
		console.log('Score Explanation:', data.scoreExplanation);
	} catch (error) {
		console.error('Test failed:', error);
	}
}

// Run the test
console.log('Starting Vision API test...');
testVisionAPI();

console.log('Starting Analyze Uploaded Logo test...');
testAnalyzeUploadedLogo();
