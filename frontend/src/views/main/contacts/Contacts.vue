<template>
    <router-view></router-view>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { store } from '@/store';

const routeGuardContacts = async (to, from, next) => {
  next('/main');
};

@Component
export default class Contacts extends Vue {
  public beforeRouteEnter(to, from, next) {
    routeGuardContacts(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    routeGuardContacts(to, from, next);
  }
}
</script>
