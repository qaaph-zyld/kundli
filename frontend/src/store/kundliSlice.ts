import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Location {
  city: string;
  latitude: number;
  longitude: number;
  timezone: string;
}

export interface Planet {
  name: string;
  sign: number;
  degree: number;
  longitude: number;
  dignity?: string;
  nakshatra?: string;
  pada?: number;
}

export interface House {
  number: number;
  sign: number;
  longitude: number;
  degree: number;
}

export interface TimeInfo {
  local: string;
  utc: string;
  ghati: number;
  vighati: number;
  pal: number;
  ayanamsa: number;
}

export interface ChartData {
  ascendant: {
    sign: string;
    degree: number;
    longitude: number;
    nakshatra?: string;
    pada?: number;
  };
  planets: Planet[];
  houses: House[];
  timeInfo: TimeInfo;
}

export interface SavedKundli {
  id: string;
  name: string;
  date: string;
  time: string;
  city: string;
  latitude: number;
  longitude: number;
  timezone: string;
  chartData: ChartData;
  ayanamsa?: string;
  houseSystem?: string;
}

interface KundliState {
  date: string;
  time: string;
  seconds: string;
  amPm: 'AM' | 'PM';
  city: string;
  cityInput: string;
  latitude: number | null;
  longitude: number | null;
  timezone: string;
  manualCoordinates: boolean;
  ayanamsa: string;
  houseSystem: string;
  loading: boolean;
  error: string | null;
  chartData: ChartData | null;
  savedKundlis: SavedKundli[];
}

// Set default date and time to current
const now = new Date();
const today = now.toISOString().split('T')[0];
const currentTime = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
const currentSeconds = now.getSeconds().toString().padStart(2, '0');
const currentAmPm = now.getHours() >= 12 ? 'PM' : 'AM';

const initialState: KundliState = {
  date: today,
  time: currentTime,
  seconds: currentSeconds,
  amPm: currentAmPm,
  city: '',
  cityInput: '',
  latitude: null,
  longitude: null,
  timezone: '',
  manualCoordinates: false,
  ayanamsa: 'Lahiri',
  houseSystem: 'W', // Whole sign system default
  loading: false,
  error: null,
  chartData: null,
  savedKundlis: []
};

const kundliSlice = createSlice({
  name: 'kundli',
  initialState,
  reducers: {
    setDate: (state, action: PayloadAction<string>) => {
      state.date = action.payload;
    },
    setTime: (state, action: PayloadAction<string>) => {
      state.time = action.payload;
    },
    setSeconds: (state, action: PayloadAction<string>) => {
      state.seconds = action.payload;
    },
    setAmPm: (state, action: PayloadAction<'AM' | 'PM'>) => {
      state.amPm = action.payload;
    },
    setLocation: (state, action: PayloadAction<Location>) => {
      state.city = action.payload.city;
      state.latitude = action.payload.latitude;
      state.longitude = action.payload.longitude;
      state.timezone = action.payload.timezone;
    },
    setCityInput: (state, action: PayloadAction<string>) => {
      state.cityInput = action.payload;
    },
    setManualCoordinates: (state, action: PayloadAction<boolean>) => {
      state.manualCoordinates = action.payload;
    },
    setLatitude: (state, action: PayloadAction<number>) => {
      state.latitude = action.payload;
    },
    setLongitude: (state, action: PayloadAction<number>) => {
      state.longitude = action.payload;
    },
    setTimezone: (state, action: PayloadAction<string>) => {
      state.timezone = action.payload;
    },
    setAyanamsa: (state, action: PayloadAction<string>) => {
      state.ayanamsa = action.payload;
    },
    setHouseSystem: (state, action: PayloadAction<string>) => {
      state.houseSystem = action.payload;
    },
    startCalculation: (state) => {
      state.loading = true;
      state.error = null;
    },
    setChartData: (state, action: PayloadAction<ChartData>) => {
      state.chartData = action.payload;
      state.loading = false;
      state.error = null;
    },
    calculationError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.loading = false;
    },
    addSavedKundli: (state, action: PayloadAction<SavedKundli>) => {
      state.savedKundlis.push(action.payload);
    },
    removeSavedKundli: (state, action: PayloadAction<string>) => {
      state.savedKundlis = state.savedKundlis.filter(k => k.id !== action.payload);
    },
    loadKundli: (state, action: PayloadAction<SavedKundli>) => {
      state.date = action.payload.date;
      state.time = action.payload.time;
      state.city = action.payload.city;
      state.cityInput = action.payload.city;
      state.latitude = action.payload.latitude;
      state.longitude = action.payload.longitude;
      state.timezone = action.payload.timezone;
      state.chartData = action.payload.chartData;
      if (action.payload.ayanamsa) {
        state.ayanamsa = action.payload.ayanamsa;
      }
      if (action.payload.houseSystem) {
        state.houseSystem = action.payload.houseSystem;
      }
    }
  }
});

export const {
  setDate,
  setTime,
  setSeconds,
  setAmPm,
  setLocation,
  setCityInput,
  setManualCoordinates,
  setLatitude,
  setLongitude,
  setTimezone,
  setAyanamsa,
  setHouseSystem,
  startCalculation,
  setChartData,
  calculationError,
  addSavedKundli,
  removeSavedKundli,
  loadKundli
} = kundliSlice.actions;

export default kundliSlice.reducer;
