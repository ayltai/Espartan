import { useFont, } from '@shopify/react-native-skia';
import { intlFormat, } from 'date-fns';
import { View, } from 'react-native';
import { CartesianChart, Line, } from 'victory-native';

import type { Device, Telemetry, } from '../models';

export const DeviceChart = ({
    devices,
    telemetries,
    colours,
} : {
    devices     : Device[],
    telemetries : Telemetry[],
    colours     : string[],
}) => {
    const font = useFont(require('../assets/RobotoCondensed-Regular.ttf'));

    const data : Record<string, number>[] = [];

    const yesterday   = new Date().getTime() - 24 * 60 * 60 * 1000;
    const currentHour = new Date().setMinutes(0, 0, 0);

    telemetries.filter(telemetry => telemetry.dataType === 'temperature').filter(telemetry => new Date(telemetry.timestamp).getTime() >= yesterday).sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()).forEach(telemetry => {
        const existingEntry = data.find(d => d.timestamp === new Date(telemetry.timestamp).getTime());
        if (existingEntry) {
            existingEntry[telemetry.deviceId] = telemetry.value / 100;
        } else {
            const entry : Record<string, number> = {
                timestamp : new Date(telemetry.timestamp).getTime(),
            };

            entry[telemetry.deviceId] = telemetry.value / 100;

            data.push(entry);
        }
    });

    return (
        <View style={{
            width  : '100%',
            height : 300,
        }}>
            <CartesianChart
                data={data}
                xKey='timestamp'
                yKeys={devices.map(device => device.id)}
                xAxis={{
                    tickCount    : 13,
                    tickValues   : [
                        currentHour - 24 * 60 * 60 * 1000,
                        currentHour - 20 * 60 * 60 * 1000,
                        currentHour - 16 * 60 * 60 * 1000,
                        currentHour - 12 * 60 * 60 * 1000,
                        currentHour - 8 * 60 * 60 * 1000,
                        currentHour - 4 * 60 * 60 * 1000,
                        currentHour,
                    ],
                    formatXLabel : value => intlFormat(value, {
                        timeStyle : 'short',
                        hour12    : true,
                    }),
                    font         : font,
                }}
                yAxis={[
                    {
                        tickCount    : 6,
                        tickValues   : [
                            12,
                            14,
                            16,
                            18,
                            20,
                            22,
                            24,
                            26,
                        ],
                        formatYLabel : value => `${value}°C`,
                        font         : font,
                    },
                ]}
                frame={{
                }}
                domain={{
                    x : [
                        yesterday,
                        Math.max(...(telemetries.filter(telemetry => telemetry.dataType === 'temperature').map(telemetry => new Date(telemetry.timestamp).getTime()))),
                    ],
                    y : [
                        12,
                        26,
                    ],
                }}>
                {({ points, }) => devices.map(device => device.id).map((id, index) => (
                    <Line
                        connectMissingData
                        key={id}
                        curveType='natural'
                        strokeWidth={2}
                        color={colours[index % colours.length]}
                        points={points[id]} />
                ))}
            </CartesianChart>
        </View>
    );
};
