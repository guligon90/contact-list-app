import { ActionContext } from 'vuex';
import { getStoreAccessors } from 'typesafe-vuex';

import { api } from '@/api';
import { IContactCreate, IContactUpdate } from '@/interfaces';
import { State } from '../state';
import { ContactState } from './state';
import { dispatchCheckApiError } from '../main/actions';
import { commitAddNotification, commitRemoveNotification } from '../main/mutations';
import { commitSetContact, commitSetContacts } from './mutations';
import { AxiosError } from 'axios';

type MainContext = ActionContext<ContactState, State>;

export const actions = {
    async actionCreateContact(context: MainContext, payload: IContactCreate) {
        try {
            const loadingNotification = { content: 'Salvando...', showProgress: true };

            commitAddNotification(context, loadingNotification);

            const response = (await Promise.all([
                api.contacts.createContact(context.rootState.main.token, payload),
                await new Promise<void>((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];

            commitSetContact(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Contato criado com sucesso', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error as AxiosError);
        }
    },
    async actionDeleteContact(context: MainContext, contactId: number) {
        try {
            const response = await api.contacts.deleteContact(context.rootState.main.token, contactId);

            if (response) {
                commitSetContacts(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error as AxiosError);
        }
    },
    async actionGetContact(context: MainContext, contactId: number) {
        try {
            const response = await api.contacts.getContact(context.rootState.main.token, contactId);

            if (response) {
                commitSetContact(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error as AxiosError);
        }
    },
    async actionGetContacts(context: MainContext) {
        try {
            const response = await api.contacts.getContacts(context.rootState.main.token);

            if (response) {
                commitSetContacts(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error as AxiosError);
        }
    },
    async actionUpdateContact(context: MainContext, payload: { id: number, contact: IContactUpdate }) {
        try {
            const loadingNotification = { content: 'Salvando...', showProgress: true };

            commitAddNotification(context, loadingNotification);

            const response = (await Promise.all([
                api.contacts.updateContact(context.rootState.main.token, payload.id, payload.contact),
                await new Promise<void>((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];

            commitSetContact(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Contato atualizado com sucesso', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error as AxiosError);
        }
    },
};

const { dispatch } = getStoreAccessors<ContactState, State>('');

export const dispatchCreateContact = dispatch(actions.actionCreateContact);
export const dispatchDeleteContact = dispatch(actions.actionDeleteContact);
export const dispatchGetContact = dispatch(actions.actionGetContact);
export const dispatchGetContacts = dispatch(actions.actionGetContacts);
export const dispatchUpdateContact = dispatch(actions.actionUpdateContact);
