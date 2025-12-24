export const API_MAX_RETRIES : number = 5;

export const BASE_API_URL : string = process.env.EXPO_PUBLIC_BASE_URL ?? 'http://192.168.68.166:8011/api/v1';

export const DEVICE_FRONT_DOOR : string = process.env.EXPO_PUBLIC_DEVICE_FRONT_DOOR ?? '1cdbd4e10fc4';
export const DEVICE_MAILBOX    : string = process.env.EXPO_PUBLIC_DEVICE_MAILBOX ?? '';

export const API_POLLING_INTERVAL_FAST : number = 10000;
export const API_POLLING_INTERVAL_SLOW : number = 60000;

export const HEATING_TEMPERATURE_MIN : number = 5;
export const HEATING_TEMPERATURE_MAX : number = 30;
