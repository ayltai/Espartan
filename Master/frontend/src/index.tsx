import { browserTracingIntegration, ErrorBoundary, init, replayIntegration, } from '@sentry/react';
import { Alert, theme, Typography, } from 'antd';
import { EsparkApp, } from 'espark-react';
import { StrictMode, Suspense, } from 'react';
import { createRoot, } from 'react-dom/client';

if (import.meta.env.VITE_APP_SENTRY_API_KEY) init({
    dsn          : import.meta.env.VITE_APP_SENTRY_API_KEY,
    integrations : [
        browserTracingIntegration(),
        replayIntegration(),
    ],
});

const Root = () => (
    <StrictMode>
        <Suspense fallback='Loading'>
            <ErrorBoundary fallback={<Alert.ErrorBoundary />}>
                <EsparkApp
                    themeConfig={{
                        algorithm : theme.darkAlgorithm,
                        token     : {
                            colorPrimary : '#f57c00',
                        },
                    }}
                    title={{
                        icon : (
                            <div style={{
                                marginTop : 8,
                            }}>
                                <img
                                    width={24}
                                    height={24}
                                    alt='Espartan Logo'
                                    src='images/favicon-96x96.png' />
                            </div>
                        ),
                        text : (
                            <Typography.Title
                                style={{
                                    marginLeft   : 8,
                                    marginRight  : 8,
                                    marginTop    : 16,
                                    marginBottom : 8,
                                    color        : '#ddd',
                                }}
                                level={4}>
                                Espartan
                            </Typography.Title>
                        ),
                    }}
                    telemetryDataTransformer={(value : number, dataType : string) => {
                        if (dataType === 'door_open') return value === 100 ? 'Opened' : value === 200 ? 'Opened (Warning)' : value === 300 ? 'Opened (Critical)' : 'Closed';

                        if (dataType === 'motion') return value === 100 ? 'Motion Detected' : 'No Motion';

                        if (dataType === 'battery') return `${(value / 100.0).toFixed(0)} %`;

                        if (dataType === 'humidity') return `${(value / 100.0).toFixed(1)} %`;

                        if (dataType === 'temperature') return `${(value / 100.0).toFixed(1)} °C`;

                        return (value / 100.0).toFixed(1);
                    }}
                    apiEndpoint={import.meta.env.DEV ? `http://${window.location.hostname}:8000/api/v1` : '/api/v1'} />
            </ErrorBoundary>
        </Suspense>
    </StrictMode>
);

createRoot(document.getElementById('root')!).render(<Root />);
