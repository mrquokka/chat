<template>
  <router-view v-if="is_tried_to_load" v-on:success_login="try_to_connect" />
</template>

<script lang="coffee">
import window_helpers from './helpers/window.coffee'

export default {
  data: () ->
    return {
      is_tried_to_load: false
      login: undefined
    }

  methods: {
    try_to_connect: () ->
      login = await window_helpers.connect()
      @login = login
      if login?
        route_name = 'chats'
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
