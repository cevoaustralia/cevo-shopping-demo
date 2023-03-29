import { create } from 'zustand'

import { OptionType } from 'models'

type AppState = {
    persona: OptionType | OptionType[] | null;
    setPersona: (persona: OptionType | OptionType[] | null) => void;
    userId: string;
    setUserId: (userId: string) => void;
  }

export const useStore = create<AppState>()((set) => ({
    persona: { value: "", label: "" },
    setPersona: (value: OptionType | OptionType[] | null) => set((state) => {
        return {
            ...state,
            persona: value
        }
    }),
    userId: "",
    setUserId: (value: string) => set((state) => {
        return {
            ...state,
            userId: value
        }
    }),
}))