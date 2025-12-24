import { combineReducers, configureStore, } from '@reduxjs/toolkit';

import { espartanService, } from '../apis';

const makeStore = () => configureStore({
    reducer    : combineReducers({
        [espartanService.reducerPath]: espartanService.reducer,
    }),
    middleware : getDefaultMiddleware => getDefaultMiddleware().concat(espartanService.middleware),
});

export const store = makeStore();

export type AppState    = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
