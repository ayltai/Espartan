import '@testing-library/jest-dom/vitest';
import createFetchMock from 'vitest-fetch-mock';

Object.defineProperty(window, 'matchMedia', {
    writable : true,
    value    : vi.fn().mockImplementation((query : string) => ({
        matches             : false,
        media               : query,
        onchange            : null,
        addListener         : vi.fn(),
        removeListener      : vi.fn(),
        addEventListener    : vi.fn(),
        removeEventListener : vi.fn(),
        dispatchEvent       : vi.fn(),
    })),
});

vi.mock('i18next', () => ({
    language       : 'en',
    changeLanguage : () => new Promise(() => {
    }),
}));

const t = (key : string, options? : any) => {
    if (options?.returnObjects) {
        if (key === 'labels.device.modes') return [
            'Actuator',
            'Sensor',
        ];
    }

    return key;
};

vi.mock('react-i18next', () => ({
    getI18n        : () => ({
        t,
    }),
    useTranslation : () => ({
        t,
    }),
}));


const fetchMocker = createFetchMock(vi);
fetchMocker.enableMocks();
