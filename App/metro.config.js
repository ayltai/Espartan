const { mergeConfig } = require('@react-native/metro-config');
const { getSentryExpoConfig, } = require('@sentry/react-native/metro');
const { getDefaultConfig, } = require('expo/metro-config');

const baseConfig   = getDefaultConfig(__dirname);
const sentryConfig = getSentryExpoConfig(__dirname);

const config = mergeConfig(baseConfig, sentryConfig);

module.exports = config;
