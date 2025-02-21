/// <reference types="vite/client" />

type ImportMetaEnv = {
	readonly VITE_REPLICATE_API_TOKEN: string;
	readonly VITE_API_URL: string;
};

type ImportMeta = {
	readonly env: ImportMetaEnv;
};
