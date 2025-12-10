/// <reference types="vitest/config" />
import react from '@vitejs/plugin-react-swc';
import { defineConfig, } from 'vite';

export default defineConfig({
    base    : './',
    plugins : [
        react(),
    ],
    test    : {
        globals     : true,
        environment : 'jsdom',
        coverage    : {
            enabled    : true,
            provider   : 'v8',
            reporter   : [
                'json',
                'text',
            ],
            include    : [
                'src/**/*.{ts,tsx}',
            ],
            exclude    : [
                'html/**',
                'public/**',
                'src/**/vite-env.d.ts',
                'src/**/*.types.ts',
                'src/components/**/index.tsx',
                'src/routes/**/index.tsx',
                'src/models/**/*.ts',
                'src/setupTests.ts',
                'src/utils/test.tsx',
                'vite.config.ts',
                '.eslint.config.js',
            ],
            thresholds : {
                statements : 65,
            },
        },
        include     : [
            'src/**/*.test.{ts,tsx}',
        ],
        reporters   : [
            'default',
            'html',
        ],
        setupFiles  : [
            'src/setupTests.ts',
        ],
    },
    build   : {
        sourcemap : true,
    },
});
