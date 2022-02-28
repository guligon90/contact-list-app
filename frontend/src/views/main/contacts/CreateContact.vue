<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Criar Contato</div>
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
import {
  IContact,
  IContactUpdate,
  IContactCreate,
} from '@/interfaces';
import { dispatchGetContacts, dispatchCreateContact } from '@/store/contacts/actions';

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
    this.name = '';
    this.description = '';
    this.phoneNumber = '';
    this.email = '';
    this.deleted = false;
    this.groupTag = GroupTags().defaultTag().label;
    this.$validator.reset();
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedContact: IContactCreate = {
        name: this.name,
        phone_number: this.phoneNumber,
        deleted: this.deleted,
        group_tag: GroupTags().slugByLabel(this.groupTag),
        ...(this.description && { description: this.description }),
        ...(this.email && { email: this.email }),
      };

      await dispatchCreateContact(this.$store, updatedContact);

      this.$router.push('/main/contacts/all');
    }
  }
}
</script>
