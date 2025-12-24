import { type TypedUseSelectorHook, useDispatch, useSelector, } from 'react-redux';

import type { AppDispatch, AppState, } from '../states';

export const useAppDispatch : () => AppDispatch = useDispatch;

export const useAppSelector : TypedUseSelectorHook<AppState> = useSelector;
