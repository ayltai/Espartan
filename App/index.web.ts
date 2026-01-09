import { wrap, } from '@sentry/react-native';
import { LoadSkiaWeb } from '@shopify/react-native-skia/lib/module/web';
import { version, } from 'canvaskit-wasm/package.json';
import { registerRootComponent, } from 'expo';

LoadSkiaWeb({
    locateFile : file => `https://cdn.jsdelivr.net/npm/canvaskit-wasm@${version}/bin/full/${file}`,
}).then(async () => {
    const { App, } = await import('./App');

    registerRootComponent(wrap(App));
});
