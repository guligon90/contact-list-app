import { IContact } from '@/interfaces';
import { ContactState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
    setContacts(state: ContactState, payload: IContact[]) {
        state.contacts = payload;
    },
    setContact(state: ContactState, payload: IContact) {
        const contacts = state.contacts.filter((contact: IContact) => contact.id !== payload.id);
        contacts.push(payload);
        state.contacts = contacts;
    },
};

const { commit } = getStoreAccessors<ContactState, State>('');

export const commitSetContact = commit(mutations.setContact);
export const commitSetContacts = commit(mutations.setContacts);
