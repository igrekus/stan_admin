<template>
    <v-content>
      <v-container fluid class="pt-12">
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md7 class="elevation-4">
              <v-card>
                  <v-card-title dense>
                      Quotes
                      <v-spacer></v-spacer>
                      <v-text-field
                              v-model="search"
                              label="Search"
                              single-line
                              hide-details
                              dense
                      ></v-text-field>
                  </v-card-title>
                  <v-data-table
                          :headers="headers"
                          :items="quotes"
                          :search="search"
                          :items-per-page="-1"
                          hide-default-footer
                          dense
                          class="pb-3"
                  ></v-data-table>
              </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
</template>

<script>
    export default {
      name: "Quote",
      data() {
        return {
          search: '',
          headers: [
            {
              text: 'id',
              sortable: false,
              value: 'id',
              divider: true,
              width: '5%'
            },
            {text: 'message_id', value: 'message_id', sortable: false, width: '5%'},
            {text: 'text', value: 'text', sortable: false},
          ],
          quotes: [
            {
              text: 'Frozen Yogurt',
              message_id: 159,
              id: 6.0,
            },
            {
              text: 'Ice cream sandwich',
              message_id: 237,
              id: 9.0,
            },
            {
              text: 'Eclair',
              message_id: 262,
              id: 16.0,
            },
          ],
        }
      }
    }
</script>

<style scoped>

</style>