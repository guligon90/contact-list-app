import axios from 'axios';

import { apiUrl } from '@/env';
import { authHeaders } from './common';
import { IContact, IContactUpdate, IContactCreate } from '../interfaces';

const contactsApi = {
  async createContact(token: string, data: IContactCreate) {
    return axios.post(`${apiUrl}/api/v1/contacts/`, data, authHeaders(token));
  },
  async deleteContact(token: string, contactId: number) {
    return axios.delete(`${apiUrl}/api/v1/contacts/${contactId}`, authHeaders(token));
  },
  async getContact(token: string, contactId: number) {
    return axios.get<IContact>(`${apiUrl}/api/v1/contacts/${contactId}`, authHeaders(token));
  },
  async getContacts(token: string) {
    return axios.get<IContact[]>(`${apiUrl}/api/v1/contacts/`, authHeaders(token));
  },
  async updateContact(token: string, contactId: number, data: IContactUpdate) {
    return axios.put(`${apiUrl}/api/v1/contacts/${contactId}`, data, authHeaders(token));
  },
};

export default contactsApi;
