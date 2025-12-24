import { captureException, } from '@sentry/react-native';

export const handleError = (error : any) => {
    if (process.env.EXPO_PUBLIC_ENVIRONMENT === 'dev') {
        console.error(error);
    } else {
        captureException(error);
    }
};
