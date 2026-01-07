import { MaterialCommunityIcons, } from '@expo/vector-icons';
import { compareAsc, formatDistanceToNow, intlFormat, } from 'date-fns';
import { LinearGradient, } from 'expo-linear-gradient';
import React, { useEffect, } from 'react';
import { ScrollView, View, } from 'react-native';
import { List, ProgressBar, Surface, Text, } from 'react-native-paper';

import { useGetDeviceQuery, useGetHistoricalTelemetryQuery, } from '../apis';
import { API_POLLING_INTERVAL_FAST, DEVICE_MAILBOX, } from '../constants';
import { locale, t, } from '../i18n';
import { capitaliseFirstLetter, } from '../utils/strings';
import { handleError, } from '../utils';

export const MailboxScreen = () => {
    const { data : deviceData, error : deviceError, } = useGetDeviceQuery(DEVICE_MAILBOX, {
        pollingInterval : API_POLLING_INTERVAL_FAST,
    });

    const { data : historyData, error : historyError, } = useGetHistoricalTelemetryQuery({
        deviceId : DEVICE_MAILBOX,
        offset   : 7 * 24 * 60 * 60,
    }, {
        pollingInterval : API_POLLING_INTERVAL_FAST,
    });

    const lastInboxOpenedData  = historyData?.find(item => item.value === 100);
    const lastOutboxOpenedData = historyData?.find(item => item.value === 200);

    const status = compareAsc(lastInboxOpenedData ? new Date(lastInboxOpenedData.timestamp) : new Date(0), lastOutboxOpenedData ? new Date(lastOutboxOpenedData.timestamp) : new Date(0));

    useEffect(() => {
        if (deviceError) handleError(deviceError);
    }, [ deviceError, ]);

    useEffect(() => {
        if (historyError) handleError(historyError);
    }, [ historyError, ]);

    return (
        <ScrollView contentContainerStyle={{
            flexGrow : 1,
        }}>
            <View style={{
                width         : '100%',
                display       : 'flex',
                flexDirection : 'column',
            }}>
                {deviceData && (
                    <View style={{
                        width   : '100%',
                        padding : 16,
                    }}>
                        <Surface
                            style={{
                                width        : '100%',
                                borderRadius : 16,
                            }}
                            elevation={2}>
                            <LinearGradient
                                style={{
                                    minHeight      : 212,
                                    borderRadius   : 16,
                                    alignItems     : 'center',
                                    justifyContent : 'center',
                                    flexDirection  : 'column',
                                }}
                                colors={status === -1 ? [
                                    '#b2dfdb',
                                    '#4db6ac',
                                ] : status === 1 ? [
                                    '#fff9c4',
                                    '#fff176',
                                ] : [
                                    '#f8bbd0',
                                    '#f06292',
                                ]}>
                                <Text variant='headlineLarge'>
                                    {t(status === -1 ? 'label_mail_status_empty' : status === 1 ? 'label_mail_status_new_mail' : 'label_mail_status_unknown')}
                                </Text>
                                <View style={{
                                    height : 16,
                                }} />
                                <MaterialCommunityIcons
                                    name={status === -1 ? 'email-off-outline' : status === 1 ? 'email-multiple' : 'email-alert-outline'}
                                    size={100} />
                            </LinearGradient>
                        </Surface>
                        <View style={{
                            flexGrow : 1,
                        }}>
                            <List.Section>
                                {historyData && (
                                    <List.Accordion title={t('label_mail_history')}>
                                        {historyData.map(item => (
                                            <List.Item
                                                key={item.id}
                                                title={item.value === 100 ? t('label_mail_status_inbox_opened') : item.value === -100 ? t('label_mail_status_inbox_closed') : item.value === 200 ? t('label_mail_status_outbox_opened') : item.value === -200 ? t('label_mail_status_outbox_closed') : t('label_mail_status_unknown')}
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
                        </View>
                    </View>
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
        </ScrollView>
    );
};
