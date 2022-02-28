import { ContactState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    contacts: (state: ContactState) => state.contacts,
    oneContact: (state: ContactState) => (contactId: number) => {
        const filteredContacts = state.contacts.filter((contact) => contact.id === contactId);

        if (filteredContacts.length > 0) {
            return { ...filteredContacts[0] };
        }
    },
};

const { read } = getStoreAccessors<ContactState, State>('');

export const readOneContact = read(getters.oneContact);
export const readContacts = read(getters.contacts);
