export interface IContact {
  id: number;
  name: string;
  description: string;
  email: string;
  phone_number: string;
  group_tag: string;
  deleted: boolean;
  owner_id: number;
  tag_label?: string; // TODO: Just for frontend purposes. Find a better way
}

export interface IContactCreate {
  name: string;
  phone_number: string;
  description?: string;
  email?: string;
  group_tag?: string;
  deleted?: boolean;
}

export interface IContactUpdate {
  name?: string;
  phone_number?: string;
  description?: string;
  email?: string;
  group_tag?: string;
  deleted?: boolean;
}
