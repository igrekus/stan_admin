<template>
  <v-container fluid fill-height >
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-5">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Stan admin</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-alert
              :value="alert"
              color="red"
              dark
              icon="error"
              transition="scale-transition"
              outlined
            >
              Wrong login/pass.
            </v-alert>
            <v-form>
              <v-text-field id="login" placeholder="Login" name="login" prepend-icon="person" type="text"
                            v-model="login"></v-text-field>

              <v-text-field id="password" placeholder="Password" name="password" prepend-icon="lock" type="password"
                            v-model="password"></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="onLoginClicked">Login</v-btn>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  export default {
    name: 'login-dialog',

    data: () => ({
      login: '',
      password: '',
      alert: false,
    }),

    methods: {
      onLoginClicked() {
        let me = this
        this.alert = false;
        fetch('http://localhost:5000/api/login',
                {
                  method: 'POST',
                  headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                  },
                  body: JSON.stringify({
                    login: this.login,
                    password: this.password
                  })
                })
                .then(response => {
                  response.json().then(data => {
                    if (data['success']) {
                      me.$emit('login', data['user'])
                    }
                    else {
                      me.alert = true
                    }
                  })
                })
      }
    }
  }
</script>
