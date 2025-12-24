import { wrap, } from '@sentry/react-native';
import { registerRootComponent, } from 'expo';

import { App, } from './App';

registerRootComponent(wrap(App));
