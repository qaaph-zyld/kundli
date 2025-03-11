import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface KundliState {
  date: string;
  time: string;
  latitude: number | null;
  longitude: number | null;
  city: string;
  timezone: string;
  loading: boolean;
  error: string | null;
  chartData: any | null; // We'll type this properly once we know the exact structure
}

const initialState: KundliState = {
  date: new Date().toISOString().split('T')[0],
  time: new Date().toTimeString().split(' ')[0],
  latitude: null,
  longitude: null,
  city: '',
  timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
  loading: false,
  error: null,
  chartData: null,
};

export const kundliSlice = createSlice({
  name: 'kundli',
  initialState,
  reducers: {
    setDate: (state, action: PayloadAction<string>) => {
      state.date = action.payload;
    },
    setTime: (state, action: PayloadAction<string>) => {
      state.time = action.payload;
    },
    setLocation: (state, action: PayloadAction<{ lat: number; lon: number; city: string; timezone: string }>) => {
      state.latitude = action.payload.lat;
      state.longitude = action.payload.lon;
      state.city = action.payload.city;
      state.timezone = action.payload.timezone;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    setChartData: (state, action: PayloadAction<any>) => {
      state.chartData = action.payload;
    },
  },
});

export const {
  setDate,
  setTime,
  setLocation,
  setLoading,
  setError,
  setChartData,
} = kundliSlice.actions;

export default kundliSlice.reducer;
