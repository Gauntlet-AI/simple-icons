import path from 'node:path';
import react from '@vitejs/plugin-react-swc';
import {defineConfig} from 'vite';
import fs from 'node:fs';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		react(),
		{
			name: 'copy-assets',
			async buildStart() {
				// Ensure directories exist
				if (!fs.existsSync('public/icons')) {
					fs.mkdirSync('public/icons', {recursive: true});
				}
				if (!fs.existsSync('public/_data')) {
					fs.mkdirSync('public/_data', {recursive: true});
				}

				// Copy SVG files
				const svgFiles = fs
					.readdirSync('icons')
					.filter((file) => file.endsWith('.svg'));
				for (const file of svgFiles) {
					fs.copyFileSync(`icons/${file}`, `public/icons/${file}`);
				}

				// Copy JSON data
				if (fs.existsSync('_data/simple-icons.json')) {
					fs.copyFileSync(
						'_data/simple-icons.json',
						'public/_data/simple-icons.json',
					);
				}
			},
		},
	],
	server: {
		port: 3000,
		open: true,
	},
	build: {
		outDir: 'dist',
		sourcemap: true,
		assetsDir: 'assets',
		emptyOutDir: true,
		rollupOptions: {
			input: {
				main: path.resolve(__dirname, 'index.html'),
			},
		},
		copyPublicDir: true,
	},
	base: './',
	publicDir: 'public',
	define: {
		// Add any needed environment variables here
		__DEFINES__: JSON.stringify({}),
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, './src'),
			'@icons': path.resolve(__dirname, './icons'),
			'@data': path.resolve(__dirname, './_data'),
		},
		extensions: ['.mjs', '.js', '.jsx', '.ts', '.tsx', '.json'],
	},
});
