import { FontAwesome6, } from '@expo/vector-icons';
import { View, } from 'react-native';
import { Text, } from 'react-native-paper';

import type { Device, Telemetry, } from '../models';

const ORDER = [
    'Entrance',
    'Kitchen',
    'Living Room',
    'Guest Room',
    'Harold',
    'Loft',
];

export const DeviceList = ({
    devices,
    telemetries,
    colours,
} : {
    devices     : Device[],
    telemetries : Telemetry[],
    colours     : string[],
}) => devices.filter(device => device.capabilities && device.capabilities.indexOf('temperature') >= 0).slice().sort((a, b) => {
    const indexA = a.displayName ? ORDER.indexOf(a.displayName) : -1;
    const indexB = b.displayName ? ORDER.indexOf(b.displayName) : -1;

    if (indexA === -1 && indexB === -1) return devices.indexOf(a) - devices.indexOf(b);

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
                color       : colours[devices.indexOf(device) % colours.length],
            }}
            variant='bodyMedium'>
            {device.displayName}
        </Text>
        <Text
            style={{
                minWidth       : 72,
                display        : 'flex',
                flexDirection  : 'row',
                justifyContent : 'center',
                color          : colours ? colours[devices.indexOf(device) % colours.length] : undefined,
            }}
            variant='bodyMedium'>
            <FontAwesome6
                size={14}
                color={colours ? colours[devices.indexOf(device) % colours.length] : undefined}
                name='temperature-low' />
            &nbsp;
            {(telemetries.filter(telemetry => telemetry.deviceId === device.id && telemetry.dataType === 'temperature')?.map(telemetry => telemetry.value / 100.0)[0]?.toFixed(1)) ?? '-'}°C
        </Text>
        <Text
            style={{
                minWidth       : 64,
                display        : 'flex',
                flexDirection  : 'row',
                justifyContent : 'center',
                color          : colours ? colours[devices.indexOf(device) % colours.length] : undefined,
            }}
            variant='bodyMedium'>
            <FontAwesome6
                size={14}
                color={colours ? colours[devices.indexOf(device) % colours.length] : undefined}
                name='droplet' />
            &nbsp;
            {(telemetries.filter(telemetry => telemetry.deviceId === device.id && telemetry.dataType === 'humidity')?.map(telemetry => telemetry.value / 100.0)[0]?.toFixed(0)) ?? '-'}%
        </Text>
    </View>
));
