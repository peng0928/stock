// stores/useCounterStore.js
import {defineStore} from 'pinia';

export const useInputStore = defineStore('stock', {
    state: () => ({
        name: "",
    }),
    actions: {
        updateInputValue(value) {
            this.name = value;
        }
    },
    persist: true
});