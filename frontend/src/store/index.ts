import { configureStore } from '@reduxjs/toolkit';
import kundliReducer from './kundliSlice';

export const store = configureStore({
  reducer: {
    kundli: kundliReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
