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
export const menuStore = defineStore('menuStore', {
    state: () => ({
        name: "1",
    }),
    actions: {
        update(value) {
            this.name = value;
        }
    },
    persist: true
});