import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { ContactState } from './state';

const defaultState: ContactState = {
  contacts: [],
};

export const contactsModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
