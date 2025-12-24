import { FontAwesome5, } from '@expo/vector-icons';
import { formatDistanceToNow, intlFormat, } from 'date-fns';
import React, { useEffect, } from 'react';
import { View, } from 'react-native';
import { List, ProgressBar, Surface, Switch, Text, } from 'react-native-paper';

import { useGetDeviceQuery, useGetHistoricalTelemetryQuery, useGetRecentTelemetryQuery, useSetDeviceMutation, } from '../apis';
import { API_POLLING_INTERVAL_FAST, DEVICE_FRONT_DOOR, } from '../constants';
import { locale, t, } from '../i18n';
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
                <>
                    <View style={{
                        height         : 200,
                        alignItems     : 'center',
                        justifyContent : 'center',
                        flex           : 1,
                        flexDirection  : 'column',
                    }}>
                        <Text variant='headlineLarge'>
                            {t(status === 100 ? 'label_door_status_open' : status === 200 ? 'label_door_status_warning' : status === 300 ? 'label_door_status_critical' : 'label_door_status_closed')}
                        </Text>
                        <FontAwesome5
                            name={status === 0 ? 'door-closed' : 'door-open'}
                            size={100} />
                    </View>
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
                                    {historyData.map(item => (
                                        <List.Item
                                            key={item.id}
                                            title={item.value === 100 ? t('label_door_status_open') : item.value === 200 ? t('label_door_status_warning') : item.value === 300 ? t('label_door_status_critical') : t('label_door_status_closed')}
                                            description={`${formatDistanceToNow(new Date(item.timestamp), {
                                                addSuffix : true,
                                            })} • ${intlFormat(item.timestamp, {
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
                </>
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
