import path from 'node:path';
import react from '@vitejs/plugin-react';
import {defineConfig} from 'vite';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [react()],
	server: {
		port: 3000,
		open: true,
	},
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
	},
});
