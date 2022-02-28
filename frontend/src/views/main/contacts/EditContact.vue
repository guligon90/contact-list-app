<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Editar Contato</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field
              label="Nome"
              v-model="name"
              v-validate="{required: true}"
              data-vv-name="name"
              :error-messages="errors.collect('name')">
            </v-text-field>
            <v-text-field
              label="Descrição"
              v-model="description">
            </v-text-field>
            <v-text-field
              label="E-mail"
              type="email"
              v-validate="'email'"
              v-model="email"
              data-vv-name="email">
            </v-text-field>
            <v-text-field
              label="Telefone"
              v-model="phoneNumber"
              v-validate="{required: true}"
              v-mask="'(##) #####-####'"
              data-vv-name="phoneNumber"
              :error-messages="errors.collect('phoneNumber')">
            </v-text-field>
            <v-checkbox
              label="Ativo?"
              v-model="deleted">
            </v-checkbox>
            <v-select
              label="Grupo"
              filled
              :items="groupTags"
              v-model="groupTag">
            </v-select>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancelar</v-btn>
        <v-btn @click="reset">Desfazer</v-btn>
        <v-btn @click="submit" :disabled="!valid">
              Salvar
            </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { GroupTags } from '@/types';
import { IContact, IContactUpdate } from '@/interfaces';
import { dispatchGetContacts, dispatchUpdateContact } from '@/store/contacts/actions';
import { readOneContact } from '@/store/contacts/getters';

@Component
export default class CreateContact extends Vue {
  public valid = false;
  public name: string = '';
  public description = '';
  public email: string = '';
  public phoneNumber: string = '';
  public deleted: boolean = false;
  public groupTag: string = GroupTags().defaultTag().label;
  public groupTags = GroupTags().labels();

  public async mounted() {
    await dispatchGetContacts(this.$store);
    this.reset();
  }

  public reset() {
    this.$validator.reset();

    if (this.contact) {
      this.name = this.contact.name;
      this.description = this.contact.description;
      this.email = this.contact.email;
      this.phoneNumber = this.contact.phone_number;
      this.groupTag = GroupTags().labelBySlug(this.contact.group_tag);
      this.deleted = this.contact.deleted;
    }
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (this.contact && await this.$validator.validateAll()) {
      const updatedContact: IContactUpdate = {
        ...(this.deleted !== this.contact.deleted && { deleted: this.deleted }),
        ...(this.name !== this.contact.name && { name: this.name }),
        ...(this.phoneNumber !== this.contact.phone_number && { phone_number: this.phoneNumber }),
        ...(this.description !== this.contact.description && { description: this.description }),
        ...(this.email !== this.contact.email && { email: this.email }),
        ...(this.groupTag !== this.contact.group_tag && { group_tag: GroupTags().slugByLabel(this.groupTag) }),
      };

      await dispatchUpdateContact(this.$store, { id: this.contact!.id, contact: updatedContact });

      this.$router.push('/main/contacts/all');
    }
  }

  get contact() {
    return readOneContact(this.$store)(+this.$router.currentRoute.params.id);
  }
}
</script>
