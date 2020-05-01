<template>
  <v-app>
    <login-dialog v-if="!user" @login="onUserLogin"/>
    <router-view v-else/>
  </v-app>
</template>

<script>
  import LoginDialog from "./components/LoginDialog";
  export default {
    data() {
      return {
        user: null,
      }
    },
    methods: {
      onUserLogin(user) {
        this.user = user
        this.$router.push({path: 'quote'})
      },
    },
    components: {
      LoginDialog
    },
    mounted() {
      if (!this.user) {
        // this.$router.push({path: '/'})
      }
    }
  }
</script>
