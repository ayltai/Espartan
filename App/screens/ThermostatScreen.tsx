import { FontAwesome6, } from '@expo/vector-icons';
import { LinearGradient, } from 'expo-linear-gradient';
import React, { useEffect, useMemo, } from 'react';
import { ScrollView, View, } from 'react-native';
import { Divider, IconButton, SegmentedButtons, Surface, Text, } from 'react-native-paper';

import { useGetConfigurationsQuery, useGetCurrentStateQuery, useGetDevicesQuery, useGetRecentTelemetryQuery, useGetTelemetriesQuery, useSetConfigurationsMutation, } from '../apis';
import { DeviceChart, DeviceList, Gauge, } from '../components';
import { API_POLLING_INTERVAL_SLOW, HEATING_TEMPERATURE_MAX, HEATING_TEMPERATURE_MIN, } from '../constants';
import { t, } from '../i18n';
import { handleError, } from '../utils';

const COLOURS = [
    '#ba68c8',
    '#2196f3',
    '#ff5722',
    '#afb42b',
    '#455a64',
    '#4caf50',
];

export const ThermostatScreen = () => {
    const [ setConfiguration, { isLoading : isUpdatingConfigurations, error : setConfigurationsError, }, ] = useSetConfigurationsMutation();

    const { data : configurationsData, error : configurationsError, } = useGetConfigurationsQuery(undefined, {
        pollingInterval : API_POLLING_INTERVAL_SLOW,
    });

    const { data : devicesData, error : devicesError, } = useGetDevicesQuery(undefined, {
        pollingInterval : API_POLLING_INTERVAL_SLOW,
    });

    const { data : telemetryData, error : telemetryError, } = useGetRecentTelemetryQuery(24 * 60 * 60, {
        pollingInterval : API_POLLING_INTERVAL_SLOW,
    });

    const { data : telemetriesData, error : telemetriesError, } = useGetTelemetriesQuery(undefined, {
        pollingInterval : API_POLLING_INTERVAL_SLOW,
    });

    const actuatorId = useMemo(() => {
        if (!devicesData) return null;

        const actuator = devicesData.find(device => device.capabilities && device.capabilities.indexOf('action_relay') >= 0);
        if (actuator) return actuator.id;

        return null;
    }, [ devicesData, ]);

    const { data : currentStateData, error : currentStateError, } = useGetCurrentStateQuery(actuatorId!, {
        pollingInterval : API_POLLING_INTERVAL_SLOW,
        skip            : actuatorId === null,
    });

    const lowestTemperature = useMemo(() => {
        if (!telemetryData || telemetryData.length === 0) return 0;

        let lowest = Number.MAX_VALUE;
        telemetryData.filter(telemetry => telemetry.dataType === 'temperature').forEach(telemetry => {
            if (telemetry.value < lowest) lowest = telemetry.value;
        });

        return lowest;
    }, [ telemetryData, ]);

    const averageTemperature = useMemo(() => {
        if (!telemetryData || telemetryData.length === 0) return 0;

        let sum   = 0;
        let count = 0;

        telemetryData.filter(telemetry => telemetry.dataType === 'temperature').forEach(telemetry => {
            sum   += telemetry.value;
            count += 1;
        });

        return sum / count;
    }, [ telemetryData, ]);

    const currentTemperature = useMemo(() => configurationsData?.decisionStrategy === 'avg' ? averageTemperature : lowestTemperature, [ configurationsData, averageTemperature, lowestTemperature, ]);

    const handleIncrementThreshold = () => {
        setConfiguration({
            thresholdOn      : configurationsData!.thresholdOff,
            thresholdOff     : configurationsData!.thresholdOff + 0.5,
            decisionStrategy : configurationsData!.decisionStrategy,
        });
    };

    const handleDecrementThreshold = () => {
        setConfiguration({
            thresholdOn      : configurationsData!.thresholdOff - 1.0,
            thresholdOff     : configurationsData!.thresholdOff - 0.5,
            decisionStrategy : configurationsData!.decisionStrategy,
        });
    };

    const handleStrategyChange = (strategy : string) => {
        setConfiguration({
            thresholdOn      : configurationsData!.thresholdOn,
            thresholdOff     : configurationsData!.thresholdOff,
            decisionStrategy : strategy,
        });
    };

    useEffect(() => {
        if (setConfigurationsError) handleError(setConfigurationsError);
    }, [ setConfigurationsError, ]);

    useEffect(() => {
        if (configurationsError) handleError(configurationsError);
    }, [ configurationsError, ]);

    useEffect(() => {
        if (devicesError) handleError(devicesError);
    }, [ devicesError, ]);

    useEffect(() => {
        if (telemetryError) handleError(telemetryError);
    }, [ telemetryError, ]);

    useEffect(() => {
        if (telemetriesError) handleError(telemetriesError);
    }, [ telemetriesError, ]);

    useEffect(() => {
        if (currentStateError) handleError(currentStateError);
    }, [ currentStateError, ]);

    return (
        <ScrollView contentContainerStyle={{
            flexGrow : 1,
        }}>
            <View style={{
                width          : '100%',
                display        : 'flex',
                flexDirection  : 'column',
                alignItems     : 'center',
                justifyContent : 'center',
            }}>
                <View style={{
                    width : '100%',
                }}>
                    <View style={{
                        margin : 32,
                    }}>
                        <Surface
                            style={{
                                width        : '100%',
                                borderRadius : 24,
                            }}
                            elevation={2}>
                            <LinearGradient
                                style={{
                                    width          : '100%',
                                    minHeight      : 200,
                                    paddingTop     : 32,
                                    borderRadius   : 16,
                                    display        : 'flex',
                                    alignItems     : 'center',
                                    justifyContent : 'center',
                                }}
                                colors={currentTemperature < (configurationsData ? configurationsData.thresholdOn * 100 : 1600) ? [
                                    '#bbdefb',
                                    '#64b5f6',
                                ] : currentTemperature > (configurationsData ? configurationsData?.thresholdOff * 100 : 2000) ? [
                                    '#ffccbc',
                                    '#ff8a65',
                                ] : [
                                    '#c8e6c9',
                                    '#81c784',
                                ]}>
                                {configurationsData && (
                                    <Gauge
                                        currentTemperature={currentTemperature}
                                        thresholdOn={configurationsData.thresholdOn * 100}
                                        thresholdOff={configurationsData.thresholdOff * 100}
                                        positionOffset={-32} />
                                )}
                            </LinearGradient>
                        </Surface>
                    </View>
                </View>
                <Surface style={{
                    width                : '100%',
                    padding              : 24,
                    borderTopLeftRadius  : 24,
                    borderTopRightRadius : 24,
                    display              : 'flex',
                    flexDirection        : 'column',
                    flexGrow             : 1,
                    alignItems           : 'center',
                }}>
                    <View style={{
                        marginBottom   : 16,
                        display        : 'flex',
                        flexDirection  : 'row',
                        alignItems     : 'center',
                        justifyContent : 'center',
                    }}>
                        <FontAwesome6
                            name='fire-flame-curved'
                            size={32}
                            color={currentStateData === 1 ? '#d32f2f' : '#546e7a'} />
                        <View style={{
                            width : 8,
                        }} />
                        <Text
                            style={{
                                color : currentStateData === 1 ? '#d32f2f' : '#546e7a',
                            }}
                            variant='headlineSmall'>
                            {currentStateData === 1 ? t('label_thermo_status_on') : t('label_thermo_status_off')}
                        </Text>
                    </View>
                    <Divider style={{
                        width        : '100%',
                        marginBottom : 16,
                    }} />
                    {devicesData && telemetryData && (
                        <DeviceList
                            devices={devicesData.filter(device => device.capabilities && (device.capabilities.indexOf('temperature') >= 0 || device.capabilities.indexOf('humidity') >= 0))}
                            telemetries={telemetryData}
                            colours={COLOURS} />
                    )}
                    <Divider style={{
                        width        : '100%',
                        marginTop    : 16,
                        marginBottom : 16,
                    }} />
                    {configurationsData && (
                        <>
                            <View style={{
                                width          : '50%',
                                display        : 'flex',
                                flexDirection  : 'row',
                                alignItems     : 'center',
                                justifyContent : 'center',
                            }}>
                                <IconButton
                                    disabled={isUpdatingConfigurations || configurationsData.thresholdOn <= HEATING_TEMPERATURE_MIN}
                                    size={32}
                                    icon='arrow-down-drop-circle-outline'
                                    onPress={handleDecrementThreshold} />
                                <View
                                    style={{
                                        display        : 'flex',
                                        flexDirection  : 'column',
                                        alignItems     : 'center',
                                        justifyContent : 'center',
                                    }}>
                                    <Text variant='bodySmall'>
                                        {t('label_thermo_target')}
                                    </Text>
                                    <Text
                                        style={{
                                            fontWeight : 'bold',
                                        }}
                                        variant='titleMedium'>
                                        {(configurationsData.thresholdOn + 0.5).toFixed(1)} °C
                                    </Text>
                                </View>
                                <IconButton
                                    disabled={isUpdatingConfigurations || configurationsData.thresholdOn >= HEATING_TEMPERATURE_MAX}
                                    size={32}
                                    icon='arrow-up-drop-circle-outline'
                                    onPress={handleIncrementThreshold} />
                            </View>
                            <View style={{
                                width          : '50%',
                                marginTop      : 16,
                                marginBottom   : 16,
                                display        : 'flex',
                                flexDirection  : 'row',
                                alignItems     : 'center',
                                justifyContent : 'center',
                            }}>
                                <Text variant='bodySmall'>
                                    {t('label_thermo_decision_strategy')}
                                </Text>
                                <View style={{
                                    width : 8,
                                }} />
                                <SegmentedButtons
                                    density='small'
                                    buttons={[
                                        {
                                            disabled : isUpdatingConfigurations,
                                            label    : t('label_thermo_decision_strategies_min'),
                                            value    : 'min',
                                        }, {
                                            disabled : isUpdatingConfigurations,
                                            label    : t('label_thermo_decision_strategies_avg'),
                                            value    : 'avg',
                                        },
                                    ]}
                                    value={configurationsData.decisionStrategy}
                                    onValueChange={handleStrategyChange} />
                            </View>
                        </>
                    )}
                    <View style={{
                        width        : '100%',
                        marginTop    : 16,
                        marginBottom : 16,
                    }} />
                    {devicesData && telemetriesData && (
                        <DeviceChart
                            devices={devicesData.filter(device => device.capabilities && device.capabilities.indexOf('temperature') >= 0)}
                            telemetries={telemetriesData}
                            colours={COLOURS} />
                    )}
                </Surface>
            </View>
        </ScrollView>
    );
};
