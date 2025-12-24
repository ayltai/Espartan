import { FontAwesome5, MaterialCommunityIcons, MaterialIcons, } from '@expo/vector-icons';
import { init, } from '@sentry/react-native';
import React, { useState, } from 'react';
import { Appbar, BottomNavigation, MD3LightTheme, PaperProvider, } from 'react-native-paper';
import { Provider, } from 'react-redux';

import { t, } from './i18n';
import { FrontDoorScreen, MailboxScreen, ThermostatScreen } from './screens';
import { store, } from './states';

init({
    dsn            : process.env.EXPO_PUBLIC_SENTRY_DSN,
    sendDefaultPii : true,
    enableLogs     : false,
});

export const App = () => {
    const [ index, setIndex, ] = useState<number>(0);

    const [ routes, ] = useState([
        {
            key           : 'thermo',
            title         : t('tab_thermo'),
            focusedIcon   : () => (
                <FontAwesome5
                    name='temperature-high'
                    size={24} />
            ),
            unfocusedIcon : () => (
                <FontAwesome5
                    name='temperature-low'
                    size={24} />
            ),
        }, {
            key           : 'mail',
            title         : t('tab_mail'),
            focusedIcon   : () => (
                <MaterialIcons
                    name='mail'
                    size={24} />
            ),
            unfocusedIcon : () => (
                <MaterialIcons
                    name='mail-outline'
                    size={24} />
            ),
        }, {
            key           : 'door',
            title         : t('tab_door'),
            focusedIcon   : () => (
                <MaterialCommunityIcons
                    name='door-open'
                    size={24} />
            ),
            unfocusedIcon : () => (
                <MaterialCommunityIcons
                    name='door-closed'
                    size={24} />
            ),
        },
    ]);

    return (
        <Provider store={store}>
            <PaperProvider theme={{
                ...MD3LightTheme,
                colors: {
                    ...MD3LightTheme.colors,
                    primary   : '#ff9800',
                    secondary : '#2196f3',
                },
            }}>
                <Appbar.Header>
                    <Appbar.Content title={routes[index].title} />
                </Appbar.Header>
                <BottomNavigation
                    navigationState={{
                        index,
                        routes,
                    }}
                    renderScene={BottomNavigation.SceneMap({
                        thermo : ThermostatScreen,
                        mail   : MailboxScreen,
                        door   : FrontDoorScreen,
                    })}
                    onIndexChange={setIndex} />
            </PaperProvider>
        </Provider>
    );
};
