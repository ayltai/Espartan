import { FontAwesome6, } from '@expo/vector-icons';
import React, { useEffect, useMemo, } from 'react';
import { View, } from 'react-native';
import { AnimatedCircularProgress, } from 'react-native-circular-progress';
import { Divider, IconButton, SegmentedButtons, Text, } from 'react-native-paper';

import { useGetConfigurationsQuery, useGetCurrentStateQuery, useGetDevicesQuery, useGetRecentTelemetryQuery, useSetConfigurationsMutation, } from '../apis';
import { API_POLLING_INTERVAL_SLOW, HEATING_TEMPERATURE_MAX, HEATING_TEMPERATURE_MIN, } from '../constants';
import { t, } from '../i18n';
import { handleError, } from '../utils';

const ORDER = [
    'Entrance',
    'Living Room',
    'Kitchen',
    'Harold',
    'Loft',
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
        if (currentStateError) handleError(currentStateError);
    }, [ currentStateError, ]);

    return (
        <View style={{
            width          : '100%',
            display        : 'flex',
            flexDirection  : 'column',
            alignItems     : 'center',
            justifyContent : 'center',
        }}>
            <View style={{
                width          : '100%',
                height         : 200,
                display        : 'flex',
                alignItems     : 'center',
                justifyContent : 'center',
            }}>
                {configurationsData && (
                    <>
                        <AnimatedCircularProgress
                            size={180}
                            width={16}
                            tintColor={currentTemperature < configurationsData.thresholdOn - 0.5 ? '#fbc02d' : currentTemperature > configurationsData.thresholdOff + 0.5 ? '#d32f2f' : '#388e3c'}
                            backgroundWidth={2}
                            backgroundColor='#607d8b'
                            arcSweepAngle={240}
                            rotation={240}
                            lineCap='round'
                            fill={(currentTemperature / 100.0 - HEATING_TEMPERATURE_MIN) / (HEATING_TEMPERATURE_MAX - HEATING_TEMPERATURE_MIN) * 100} />
                        <Text
                            style={{
                                top       : '50%',
                                left      : '50%',
                                position  : 'absolute',
                                transform : [
                                    {
                                        translateX : '-50%',
                                    }, {
                                        translateY : '-50%',
                                    },
                                ],
                                textAlign : 'center',
                                width     : '100%',
                            }}
                            variant='headlineMedium'>
                            {currentTemperature ? (currentTemperature / 100.0).toFixed(1) : '-'}°C
                        </Text>
                        <Text
                            style={{
                                width          : '100%',
                                left           : -32,
                                top            : 40,
                                display        : 'flex',
                                flexDirection  : 'row',
                                justifyContent : 'center',
                                position       : 'absolute',
                            }}
                            variant='bodySmall'>
                            15°C
                        </Text>
                        <Text
                            style={{
                                width          : '100%',
                                left           : 32,
                                top            : 40,
                                display        : 'flex',
                                flexDirection  : 'row',
                                justifyContent : 'center',
                                position       : 'absolute',
                            }}
                            variant='bodySmall'>
                            20°C
                        </Text>
                        <Text
                            style={{
                                width          : '100%',
                                left           : -48,
                                top            : 140,
                                display        : 'flex',
                                flexDirection  : 'row',
                                justifyContent : 'center',
                                position       : 'absolute',
                            }}
                            variant='bodySmall'>
                            5°C
                        </Text>
                        <Text
                            style={{
                                width          : '100%',
                                left           : 48,
                                top            : 140,
                                display        : 'flex',
                                flexDirection  : 'row',
                                justifyContent : 'center',
                                position       : 'absolute',
                            }}
                            variant='bodySmall'>
                            30°C
                        </Text>
                    </>
                )}
            </View>
            <View style={{
                display       : 'flex',
                flexDirection : 'column',
                flexGrow      : 1,
                alignItems    : 'center',
            }}>
                <View style={{
                    marginBottom   : 8,
                    display        : 'flex',
                    flexDirection  : 'row',
                    alignItems     : 'center',
                    justifyContent : 'center',
                }}>
                    <FontAwesome6
                        name='fire-flame-curved'
                        size={32}
                        color={currentStateData === 1 ? '#d32f2f' : '#546e7a'} />
                    &nbsp;
                    <Text
                        style={{
                            color : currentStateData === 1 ? '#d32f2f' : '#546e7a',
                        }}
                        variant='headlineSmall'>
                        {currentStateData === 1 ? t('label_thermo_status_on') : t('label_thermo_status_off')}
                    </Text>
                </View>
                <Divider />
                {devicesData && devicesData.filter(device => device.capabilities && device.capabilities.indexOf('temperature') >= 0).slice().sort((a, b) => {
                        const indexA = a.displayName ? ORDER.indexOf(a.displayName) : -1;
                        const indexB = b.displayName ? ORDER.indexOf(b.displayName) : -1;

                        if (indexA === -1 && indexB === -1) return devicesData.indexOf(a) - devicesData.indexOf(b);

                        if (indexA === -1) return 1;
                        if (indexB === -1) return -1;

                        return indexA - indexB;
                    }).map(device => (
                        <View
                            key={device.id}
                            style={{
                                width          : '100%',
                                display        : 'flex',
                                flexDirection  : 'row',
                                justifyContent : 'space-between',
                            }}>
                            <Text
                                style={{
                                    marginRight : 8,
                                    flexGrow    : 1,
                                }}
                                variant='bodyMedium'>
                                {device.displayName}
                            </Text>
                            <Text
                                style={{
                                    width          : 64,
                                    display        : 'flex',
                                    flexDirection  : 'row',
                                    justifyContent : 'center',
                                }}
                                variant='bodyMedium'>
                                <FontAwesome6
                                    name='temperature-low'
                                    size={14} />
                                &nbsp;
                                {(telemetryData && telemetryData.filter(telemetry => telemetry.deviceId === device.id && telemetry.dataType === 'temperature')?.map(telemetry => telemetry.value / 100.0)[0]?.toFixed(1)) ?? '-'}°C
                            </Text>
                            <Text
                                style={{
                                    width          : 64,
                                    display        : 'flex',
                                    flexDirection  : 'row',
                                    justifyContent : 'center',
                                }}
                                variant='bodyMedium'>
                                <FontAwesome6
                                    name='droplet'
                                    size={14} />
                                &nbsp;
                                {(telemetryData && telemetryData.filter(telemetry => telemetry.deviceId === device.id && telemetry.dataType === 'humidity')?.map(telemetry => telemetry.value / 100.0)[0]?.toFixed(0)) ?? '-'}%
                            </Text>
                        </View>
                    ))}
                <Divider />
                {configurationsData && (
                        <>
                            <View style={{
                                width          : '100%',
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
                                    <Text variant='bodyMedium'>
                                        {t('label_thermo_target')}
                                    </Text>
                                    <Text variant='titleMedium'>
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
                                width          : '100%',
                                display        : 'flex',
                                flexDirection  : 'row',
                                alignItems     : 'center',
                                justifyContent : 'center',
                            }}>
                                <Text variant='bodyMedium'>
                                    {t('label_thermo_decision_strategy')}
                                </Text>
                                &nbsp;
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
            </View>
        </View>
    );
};
