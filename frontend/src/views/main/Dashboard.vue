<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Dashboard</div>
      </v-card-title>
      <v-card-text>
        <div class="headline font-weight-light ma-5">Bem-vindo(a), {{greetedUser}}!</div>
      </v-card-text>
      <v-card-actions>
        <v-btn to="/main/profile/view">Ver Perfil</v-btn>
        <v-btn to="/main/profile/edit">Editar Perfil</v-btn>
        <v-btn to="/main/profile/password">Alterar Senha</v-btn>
        <v-btn to="/main/contacts/all">Gerenciar Contatos</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { readUserProfile } from '@/store/main/getters';

@Component
export default class Dashboard extends Vue {
  get greetedUser() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile) {
      if (userProfile.full_name) {
        return userProfile.full_name;
      } else {
        return userProfile.email;
      }
    }
  }
}
</script>
