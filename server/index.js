import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import cors from 'cors';
import dotenv from 'dotenv';
import express from 'express';
import OpenAI from 'openai';
import sharp from 'sharp';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize environment variables with explicit path to root .env
dotenv.config({path: path.join(__dirname, '../.env')});

// Initialize API clients
const openai = new OpenAI({
	apiKey: process.env.OPENAI_API_KEY,
});

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from the dist directory after building
app.use(express.static(path.join(__dirname, '../dist')));
// Serve static files from the public directory
app.use(express.static(path.join(__dirname, '../public')));

// API endpoint for icon analysis
app.post('/api/analyze-icon', async (request, res) => {
	try {
		const {title, svgPath} = request.body;

		if (!title || !svgPath) {
			return res.status(400).json({
				error: 'Missing required fields: title and svgPath are required',
			});
		}

		// Read both the SVG file and icon data
		const [svgBuffer, iconDataText] = await Promise.all([
			fs.readFile(path.join(__dirname, '..', svgPath)),
			fs.readFile(path.join(__dirname, '../_data/simple-icons.json'), 'utf8'),
		]);

		// Parse icon data and find the matching icon
		const icons = JSON.parse(iconDataText);
		const icon = icons.find(
			(i) => i.title.toLowerCase() === title.toLowerCase(),
		);
		const brandColor = icon ? `#${icon.hex}` : '#000000';

		// Convert SVG to PNG using Sharp with brand color
		const pngBuffer = await sharp(svgBuffer)
			.resize(512, 512)
			.png()
			.flatten({background: '#ffffff'})
			.tint(brandColor)
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
						'You are a helpful assistant that writes clear, concise product descriptions.',
				},
				{
					role: 'user',
					content: `Write a one sentence description for a product/company called "${title}".`,
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
						'You are a concise design critic. Analyze icons focusing on key visual elements and effectiveness. Keep each point brief but insightful. Use markdown formatting.',
				},
				{
					role: 'user',
					content: [
						{
							type: 'text',
							text: "Analyze this icon's design elements and effectiveness as a brand symbol. Focus on the most important aspects.",
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

		res.json({
			productDescription,
			iconAnalysis,
		});
	} catch (error) {
		console.error('Error in icon analysis:', error);
		res.status(500).json({
			error: 'API Error',
			details: error.message,
		});
	}
});

// New endpoint for generating design score
app.post('/api/analyze-score', async (request, res) => {
	try {
		const {productDescription, iconAnalysis} = request.body;

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

		res.json({
			designScore: scoreData.score,
			scoreExplanation: scoreData.explanation,
		});
	} catch (error) {
		console.error('Error in score analysis:', error);
		res.status(500).json({
			error: 'API Error',
			details: error.message,
		});
	}
});

// Handle all other routes by serving the main index.html
app.get('*', (request, res) => {
	res.sendFile(path.join(__dirname, '../dist/index.html'));
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
	console.log(`Server running on port ${PORT}`);
});
