import { getLocales, } from 'expo-localization';
import en from './assets/en.json';

const translations : Record<string, Record<string, string>> = {
    en,
};

export const locale = getLocales()[0].languageCode === 'en' ? 'en' : 'en';

export const t = (key : string) : string => translations[locale][key] || key;
