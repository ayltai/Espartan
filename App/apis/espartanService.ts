import { createApi, fetchBaseQuery, } from '@reduxjs/toolkit/query/react';

import { API_MAX_RETRIES, BASE_API_URL, } from '../constants';
import type { Configuration, Device, Telemetry, } from '../models';
import { camelCaseToSnakeCase, snakeCaseToCamelCase, } from '../utils/strings';

export const espartanService = createApi({
    reducerPath : 'espartanService',
    baseQuery   : fetchBaseQuery({
        baseUrl: BASE_API_URL,
    }),
    endpoints   : build => ({
        getConfigurations      : build.query<Configuration, void>({
            query             : () => '/settings/1',
            transformResponse : (response : any) => snakeCaseToCamelCase(response) as Configuration,
            extraOptions      : {
                maxRetries : API_MAX_RETRIES,
            },
            providesTags      : [
                // @ts-ignore
                'config',
            ],
        }),
        setConfigurations      : build.mutation<void, Configuration>({
            query           : configurations => ({
                url    : '/settings/1',
                method : 'PUT',
                body   : camelCaseToSnakeCase(configurations),
            }),
            invalidatesTags : [
                // @ts-ignore
                'config',
            ],
        }),
        getCurrentState        : build.query<number, string>({
            query        : deviceId => `/relays/current/${deviceId}`,
            extraOptions : {
                maxRetries : API_MAX_RETRIES,
            },
        }),
        setDevice              : build.mutation<void, Device>({
            query           : device => ({
                url    : `/devices/${ device.id }`,
                method : 'PUT',
                body   : camelCaseToSnakeCase(device),
            }),
            invalidatesTags : [
                // @ts-ignore
                'device',
            ],
        }),
        getDevice              : build.query<Device, string>({
            query             : deviceId => `/devices/${deviceId}`,
            transformResponse : (response : any) => snakeCaseToCamelCase(response) as Device,
            providesTags      : [
                // @ts-ignore
                'device',
            ],
            extraOptions      : {
                maxRetries : API_MAX_RETRIES,
            },
        }),
        getDevices             : build.query<Device[], void>({
            query             : () => '/devices',
            transformResponse : (response : any) => response.map((item : any) => snakeCaseToCamelCase(item)),
            extraOptions      : {
                maxRetries : API_MAX_RETRIES,
            },
        }),
        getTelemetries         : build.query<Telemetry[], void>({
            query             : () => '/telemetry?order_by=timestamp desc&limit=2300',
            transformResponse : (response : any) => response.map((item : any) => snakeCaseToCamelCase(item)),
            extraOptions      : {
                maxRetries : API_MAX_RETRIES,
            },
        }),
        getRecentTelemetry     : build.query<Telemetry[], number>({
            query             : offset => `/telemetry/recent?offset=${offset}`,
            transformResponse : (response : any) => response.map((item : any) => snakeCaseToCamelCase(item)),
            extraOptions      : {
                maxRetries : API_MAX_RETRIES,
            },
        }),
        getHistoricalTelemetry : build.query<Telemetry[], {
            deviceId : string,
            offset   : number,
        }>({
            query             : ({
                deviceId,
                offset,
            }) => `/telemetry/history?device_id=${deviceId}&offset=${offset}`,
            transformResponse : (response : any) => response.map((item : any) => snakeCaseToCamelCase(item)),
            extraOptions      : {
                maxRetries : API_MAX_RETRIES,
            },
        }),
    }),
    tagTypes    : [
        'config',
        'device',
    ],
});

export const { useGetConfigurationsQuery, useGetCurrentStateQuery, useGetDeviceQuery, useGetDevicesQuery, useGetHistoricalTelemetryQuery, useGetRecentTelemetryQuery, useGetTelemetriesQuery, useSetConfigurationsMutation, useSetDeviceMutation, } = espartanService;
