import Vue from 'vue';
import Vuex, { StoreOptions } from 'vuex';

import { mainModule } from './main';
import { State } from './state';
import { adminModule } from './admin';
import { contactsModule } from './contacts';

Vue.use(Vuex);

const storeOptions: StoreOptions<State> = {
  modules: {
    admin: adminModule,
    contacts: contactsModule,
    main: mainModule,
  },
};

export const store = new Vuex.Store<State>(storeOptions);

export default store;
