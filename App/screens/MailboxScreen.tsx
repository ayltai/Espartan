import { MaterialCommunityIcons, } from '@expo/vector-icons';
import { formatDistanceToNow, intlFormat, } from 'date-fns';
import React, { useEffect, } from 'react';
import { View, } from 'react-native';
import { List, ProgressBar, Surface, Text, } from 'react-native-paper';

import { useGetDeviceQuery, useGetHistoricalTelemetryQuery, useGetRecentTelemetryQuery, } from '../apis';
import { API_POLLING_INTERVAL_FAST, DEVICE_MAILBOX, } from '../constants';
import { locale, t, } from '../i18n';
import { handleError, } from '../utils';

export const MailboxScreen = () => {
    const { data : deviceData, error : deviceError, } = useGetDeviceQuery(DEVICE_MAILBOX, {
        pollingInterval : API_POLLING_INTERVAL_FAST,
    });

    const { data : telemetryData, error : telemetryError, } = useGetRecentTelemetryQuery(24 * 60 * 60, {
        pollingInterval : API_POLLING_INTERVAL_FAST,
    });

    const { data : historyData, error : historyError, } = useGetHistoricalTelemetryQuery({
        deviceId : DEVICE_MAILBOX,
        offset   : 7 * 24 * 60 * 60,
    }, {
        pollingInterval : API_POLLING_INTERVAL_FAST,
    });

    const status = telemetryData?.filter(item => item.deviceId === DEVICE_MAILBOX && item.dataType === 'mail')[0].value;

    useEffect(() => {
        if (deviceError) handleError(deviceError);
    }, [ deviceError, ]);

    useEffect(() => {
        if (telemetryError) handleError(telemetryError);
    }, [ telemetryError, ]);

    useEffect(() => {
        if (historyError) handleError(historyError);
    }, [ historyError, ]);

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
                            {t(status === 100 || status === -100 ? 'label_mail_status_new_mail' : status === 200 || status === -200 ? 'label_mail_status_empty' : 'label_mail_status_unknown')}
                        </Text>
                        <MaterialCommunityIcons
                            name={status === 100 || status === -100 ? 'email-multiple' : status === 200 || status === -200 ? 'email-off' : 'email-alert-outline'}
                            size={100} />
                    </View>
                    <Surface
                        style={{
                            flexGrow : 1,
                        }}
                        mode='flat'>
                        <List.Section>
                            {historyData && (
                                <List.Accordion title={t('label_mail_history')}>
                                    {historyData.map(item => (
                                        <List.Item
                                            key={item.id}
                                            title={item.value === 100 ? t('label_mail_status_inbox_opened') : item.value === -100 ? 'label_mail_status_inbox_closed' : item.value === 200 ? t('label_mail_status_outbox_opened') : item.value === -200 ? t('label_mail_status_outbox_closed') : t('label_mail_status_unknown')}
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
