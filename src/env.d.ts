/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly OPEN_AI_KEY: string
  readonly VITE_REPLICATE_API_TOKEN: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
} 