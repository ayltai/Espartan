import { FontAwesome5, } from '@expo/vector-icons';
import { formatDistanceToNow, intlFormat, } from 'date-fns';
import { LinearGradient, } from 'expo-linear-gradient';
import React, { useEffect, } from 'react';
import { ScrollView, View, } from 'react-native';
import { List, ProgressBar, Surface, Switch, Text, } from 'react-native-paper';

import { useGetDeviceQuery, useGetHistoricalTelemetryQuery, useGetRecentTelemetryQuery, useSetDeviceMutation, } from '../apis';
import { API_POLLING_INTERVAL_FAST, DEVICE_FRONT_DOOR, } from '../constants';
import { locale, t, } from '../i18n';
import { capitaliseFirstLetter, } from '../utils/strings';
import { handleError, } from '../utils';

export const FrontDoorScreen = () => {
    const { data : deviceData, error : deviceError, } = useGetDeviceQuery(DEVICE_FRONT_DOOR, {
        pollingInterval : API_POLLING_INTERVAL_FAST,
    });

    const { data : telemetryData, error : telemetryError, } = useGetRecentTelemetryQuery(24 * 60 * 60, {
        pollingInterval : API_POLLING_INTERVAL_FAST,
    });

    const { data : historyData, error : historyError, } = useGetHistoricalTelemetryQuery({
        deviceId : DEVICE_FRONT_DOOR,
        offset   : 7 * 24 * 60 * 60,
    }, {
        pollingInterval : API_POLLING_INTERVAL_FAST,
    });

    const [ setDevice, { isLoading : isUpdatingDevice, error : setDeviceError, }, ] = useSetDeviceMutation();

    const status = telemetryData?.filter(item => item.deviceId === DEVICE_FRONT_DOOR && item.dataType === 'door_open')[0].value;

    const handleToggleDetection = () => {
        setDevice({
            ...deviceData!,
            parameters : {
                ...deviceData!.parameters,
                detectionEnabled : !deviceData!.parameters!.detectionEnabled,
            },
        });
    };

    useEffect(() => {
        if (deviceError) handleError(deviceError);
    }, [ deviceError, ]);

    useEffect(() => {
        if (telemetryError) handleError(telemetryError);
    }, [ telemetryError, ]);

    useEffect(() => {
        if (historyError) handleError(historyError);
    }, [ historyError, ]);

    useEffect(() => {
        if (setDeviceError) handleError(setDeviceError);
    }, [ setDeviceError, ]);

    return (
        <View style={{
            width         : '100%',
            display       : 'flex',
            flex          : 1,
            flexDirection : 'column',
        }}>
            {deviceData && (
                <ScrollView contentContainerStyle={{
                    flexGrow : 1,
                }}>
                    <LinearGradient
                        style={{
                            minHeight      : 200,
                            alignItems     : 'center',
                            justifyContent : 'center',
                            flex           : 1,
                            flexDirection  : 'column',
                        }}
                        colors={status === 100 ? [
                            '#fff9c4',
                            '#fff176',
                        ] : status === 200 ? [
                            '#ffe0b2',
                            '#ffb74d',
                        ] : status === 300 ? [
                            '#f8bbd0',
                            '#f06292',
                        ] : [
                            '#bbdefb',
                            '#64b5f6',
                        ]}>
                        <Text variant='headlineLarge'>
                            {t(status === 100 ? 'label_door_status_open' : status === 200 ? 'label_door_status_warning' : status === 300 ? 'label_door_status_critical' : 'label_door_status_closed')}
                        </Text>
                        <View style={{
                            height : 16,
                        }} />
                        <FontAwesome5
                            name={status === 0 ? 'door-closed' : 'door-open'}
                            size={100} />
                    </LinearGradient>
                    <Surface
                        style={{
                            flexGrow : 1,
                        }}
                        mode='flat'>
                        <List.Section>
                            <List.Item
                                title={t('label_door_sensor')}
                                right={props => (
                                    <Switch
                                        {...props}
                                        disabled={isUpdatingDevice}
                                        value={deviceData.parameters?.detectionEnabled as boolean ?? false}
                                        onValueChange={handleToggleDetection} />
                                )} />
                            {historyData && (
                                <List.Accordion title={t('label_door_history')}>
                                    {historyData.filter(item => item.dataType === 'door_open' || item.dataType === 'motion' && item.value === 100).map(item => (
                                        <List.Item
                                            key={item.id}
                                            title={item.value === 100 ? item.dataType === 'motion' ? t('label_door_status_motion_detected') : t('label_door_status_open') : item.value === 200 ? t('label_door_status_warning') : item.value === 300 ? t('label_door_status_critical') : t('label_door_status_closed')}
                                            description={`${capitaliseFirstLetter(formatDistanceToNow(new Date(item.timestamp), {
                                                addSuffix : true,
                                            }))} • ${intlFormat(item.timestamp, {
                                                dateStyle : 'medium',
                                                timeStyle : 'medium',
                                            }, {
                                                locale,
                                            })}`} />
                                    ))}
                                </List.Accordion>
                            )}
                        </List.Section>
                    </Surface>
                </ScrollView>
            )}
            {!deviceData && (
                <View style={{
                    flexGrow       : 1,
                    alignItems     : 'center',
                    justifyContent : 'center',
                }}>
                    <ProgressBar
                        indeterminate
                        style={{
                            width : '80%',
                        }} />
                </View>
            )}
        </View>
    );
};
