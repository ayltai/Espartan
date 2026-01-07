import { Dimensions, } from 'react-native';
import { AnimatedCircularProgress, } from 'react-native-circular-progress';
import { Text, } from 'react-native-paper';

import { HEATING_TEMPERATURE_MAX, HEATING_TEMPERATURE_MIN } from '../constants';

const windowWidth = Dimensions.get('window').width;

export const Gauge = ({
    currentTemperature,
    thresholdOn,
    thresholdOff,
    positionOffset = 0,
} : {
    currentTemperature : number,
    thresholdOn        : number,
    thresholdOff       : number,
    positionOffset     : number,
}) => (
    <>
        <AnimatedCircularProgress
            size={180}
            width={16}
            tintColor={currentTemperature < thresholdOn ? '#fbc02d' : currentTemperature > thresholdOff + 0.5 ? '#d32f2f' : '#388e3c'}
            backgroundWidth={2}
            backgroundColor='#607d8b'
            arcSweepAngle={240}
            rotation={240}
            lineCap='round'
            fill={(currentTemperature / 100.0 - HEATING_TEMPERATURE_MIN) / (HEATING_TEMPERATURE_MAX - HEATING_TEMPERATURE_MIN) * 100} />
        <Text
            style={{
                top        : 124,
                left       : windowWidth / 2 - 38 + positionOffset,
                position   : 'absolute',
                fontWeight : 'bold',
                textAlign  : 'center',
            }}
            variant='headlineMedium'>
            {currentTemperature ? (currentTemperature / 100.0).toFixed(1) : '-'}°C
        </Text>
        <Text
            style={{
                top            : 60,
                left           : windowWidth / 2 - 40 + positionOffset,
                display        : 'flex',
                flexDirection  : 'row',
                justifyContent : 'center',
                textAlign      : 'center',
                position       : 'absolute',
            }}
            variant='bodySmall'>
            15°C
        </Text>
        <Text
            style={{
                top            : 60,
                left           : windowWidth / 2 + 24 + positionOffset,
                display        : 'flex',
                flexDirection  : 'row',
                justifyContent : 'center',
                textAlign      : 'center',
                position       : 'absolute',
            }}
            variant='bodySmall'>
            20°C
        </Text>
        <Text
            style={{
                top            : 104,
                left           : windowWidth / 2 - 70 + positionOffset,
                display        : 'flex',
                flexDirection  : 'row',
                justifyContent : 'center',
                textAlign      : 'center',
                position       : 'absolute',
            }}
            variant='bodySmall'>
            10°C
        </Text>
        <Text
            style={{
                top            : 104,
                left           : windowWidth / 2 + 50 + positionOffset,
                display        : 'flex',
                flexDirection  : 'row',
                justifyContent : 'center',
                textAlign      : 'center',
                position       : 'absolute',
            }}
            variant='bodySmall'>
            25°C
        </Text>
        <Text
            style={{
                top            : 160,
                left           : windowWidth / 2 - 56 + positionOffset,
                display        : 'flex',
                flexDirection  : 'row',
                justifyContent : 'center',
                textAlign      : 'center',
                position       : 'absolute',
            }}
            variant='bodySmall'>
            5°C
        </Text>
        <Text
            style={{
                top            : 160,
                left           : windowWidth / 2 + 36 + positionOffset,
                display        : 'flex',
                flexDirection  : 'row',
                justifyContent : 'center',
                textAlign      : 'center',
                position       : 'absolute',
            }}
            variant='bodySmall'>
            30°C
        </Text>
    </>
);
