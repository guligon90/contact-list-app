<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Gerenciar Contatos
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/contacts/create">Criar Contato</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="contacts">
      <template slot="items" slot-scope="props">
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.email }}</td>
        <td>{{ props.item.phone_number }}</td>
        <td>{{ props.item.tag_label }}</td>
        <td><v-icon v-if="props.item.deleted">checkmark</v-icon></td>
        <td class="justify-center layout px-0">
          <v-tooltip top>
            <span>Edit</span>
            <v-btn slot="activator" flat :to="{name: 'main-contacts-edit', params: {id: props.item.id}}">
              <v-icon>edit</v-icon>
            </v-btn>
          </v-tooltip>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { GroupTags } from '@/types';
import { IContact } from '@/interfaces';
import { readContacts } from '@/store/contacts/getters';
import { dispatchGetContacts } from '@/store/contacts/actions';

@Component
export default class ManageContacts extends Vue {
  public headers = [
    {
      text: 'Nome',
      sortable: true,
      value: 'name',
      align: 'left',
    },
    {
      text: 'E-mail',
      sortable: true,
      value: 'email',
      align: 'left',
    },
    {
      text: 'Telefone',
      sortable: true,
      value: 'phone_number',
      align: 'left',
    },
    {
      text: 'Grupo',
      sortable: true,
      value: 'tag_label',
      align: 'left',
    },
    {
      text: 'Ativo?',
      sortable: true,
      value: 'deleted',
      align: 'left',
    },
    {
      text: 'Ações',
      value: 'id',
    },
  ];

  get contacts() {
    const results = readContacts(this.$store);

    return results.map((contact: IContact) => {
      contact.tag_label = GroupTags().labelBySlug(contact.group_tag);
      return contact;
    });
  }

  public async mounted() {
    await dispatchGetContacts(this.$store);
  }
}
</script>
