<template>
  <router-view
    v-if="is_show_child"
    :current_user="login"
    v-on:success_login="success_login"
    v-on:logout="logout"
  />
</template>

<script lang="coffee">
import window_helpers from './helpers/window.coffee'

export default {
  data: () ->
    return {
      is_tried_to_load: false
      login: undefined
    }

  computed: {
    is_show_child: () ->
      if not @is_tried_to_load
        return false
      return (@$route.name in ['login', 'register']) or @login
  }

  methods: {
    success_login: (login) ->
      await window_helpers.connect()
      @login = String(login)
      @$router.push({name: "chats"})

    logout: () ->
      await window_helpers.send_query({action: "logout"})
      @$router.push({name: "login"})

    try_to_connect: () ->
      flag_result = await window_helpers.connect()
      if flag_result
        route_name = 'chats'
        login = await window_helpers.send_query({action: "get_login"})
        @login = String(login)
      else
        route_name = 'login'
      @$router.push({name: route_name})
      @is_tried_to_load = true
  }

  mounted: () ->
    @try_to_connect()
}
</script>

<style lang="scss">
@import "./css/colors.scss";

body {
  background: $default_background;
  font-family: "Open Sans";
  color: $default_text;
  margin: 0px;
  padding: 0px;
}

a {
  text-decoration: none;
}

input:focus {
  outline: unset;
}

#app {
  min-width: 480px;
  overflow-y: auto;
}

.clear_block {
  clear: both;
}
</style>
