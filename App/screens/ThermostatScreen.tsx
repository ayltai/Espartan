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

    const handleIncrementThreshold = () => {
        setConfiguration({
            thresholdOn      : configurationsData!.thresholdOn + 0.5,
            thresholdOff     : configurationsData!.thresholdOff + 0.5,
            decisionStrategy : configurationsData!.decisionStrategy,
        });
    };

    const handleDecrementThreshold = () => {
        setConfiguration({
            thresholdOn      : configurationsData!.thresholdOn - 0.5,
            thresholdOff     : configurationsData!.thresholdOff - 0.5,
            decisionStrategy : configurationsData!.decisionStrategy,
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
                <AnimatedCircularProgress
                    size={180}
                    width={16}
                    backgroundWidth={4}
                    arcSweepAngle={240}
                    rotation={240}
                    lineCap='round'
                    fill={((configurationsData?.decisionStrategy === 'avg' ? averageTemperature : lowestTemperature) / 100.0 - HEATING_TEMPERATURE_MIN) / (HEATING_TEMPERATURE_MAX - HEATING_TEMPERATURE_MIN) * 100}
                    />
            </View>
            <View style={{
                display       : 'flex',
                flexDirection : 'column',
                flexGrow      : 1,
                alignItems    : 'center',
            }}>
                <View>
                    <FontAwesome6
                        name='fire-flame-curved'
                        size={32}
                        color={currentStateData === 1 ? '#d32f2f' : '#546e7a'} />
                    <Text variant='headlineSmall'>
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
                            <Text variant='bodyMedium'>
                                {device.displayName}
                            </Text>
                            <Text variant='bodyMedium'>
                                <FontAwesome6
                                    name='temperature-low'
                                    size={14} />
                                {(telemetryData && telemetryData.filter(telemetry => telemetry.deviceId === device.id && telemetry.dataType === 'temperature')?.map(telemetry => telemetry.value / 100.0)[0]?.toFixed(1)) ?? '-'}°C
                            </Text>
                            <Text variant='bodyMedium'>
                                <FontAwesome6
                                    name='droplet'
                                    size={14} />
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
                                    icon='sort-down'
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
                                    icon='sort-up'
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
                                    onValueChange={value => {
                                        setConfiguration({
                                            thresholdOn      : configurationsData.thresholdOn,
                                            thresholdOff     : configurationsData.thresholdOff,
                                            decisionStrategy : value,
                                        });
                                    }} />
                            </View>
                        </>
                    )}
            </View>
        </View>
    );
};
