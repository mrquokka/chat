<template>
  <div v-if="chats" class="chats">
    <div class="list">
      <div class="chats_container">
        <chat_preview
          v-for="login in Object.keys(chats)"
          :key="login"
          class="chat_preview"
          :chats="chats"
          :login="login"
          v-on:click="selected_user = login"
        />
      </div>
      <div class="logout" v-on:click="$emit('logout', $event)">
        Выйти
      </div>
    </div>
    <div class="content">
      <chat
        v-if="selected_user"
        :key="'chat' + selected_user"
        :messages="messages"
        :current_user="current_user"
        :selected_user="selected_user"
        v-on:send_message="handler_send_message"
      />
      <div v-else class="placeholder">
        <div class="label">
          Выберите, кому вы хотели бы написать
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="coffee">
import window_helpers from "./../helpers/window.coffee"
import chat_preview from "./../components/chat_preview.vue"
import chat from "./../components/chat.vue"

export default {
  components: {
    chat_preview: chat_preview
    chat: chat
  }

  props: {
    current_user: {type: String, required: true}
  }

  emits: ['logout', 'send_message']

  data: () ->
    return {
      chats: undefined
      selected_user: undefined
      check_func: undefined
    }

  computed: {
    messages: () ->
      return @chats[@selected_user]
  }

  mounted: () ->
    chats = await window_helpers.send_query({action: 'get_chats'})
    @chats = chats
    @check_func = @handler_new_message.bind(@)
    window_helpers.add_linstener('new_message', @check_func)

  beforeDestroyed: () ->
    window_helpers.remove_linstener('new_message', @check_func)

  methods: {
    handler_new_message: (data) ->
      unix_time = data.unix_time
      delete data.unix_time
      if data.sender == @current_user
        key = data.receiver
      else
        key = data.sender
      @chats[key][unix_time] = data

    handler_send_message: (message) ->
      window_helpers.send_query({
        action: 'send_message'
        receiver: @selected_user
        message: message
      })

  }
}
</script>

<style lang="scss">
@import "./../css/colors.scss";

.chats {
  height: 100vh;

  > .list,
  > .content {
    float: left;
    height: 100%;
  }

  > .list {
    width: 30%;
    background: $form_background;

    > .chats_container {
      height: calc(100% - 60px);
      overflow-y: scroll;

      &::-webkit-scrollbar {
        width: 8px;
      }

      &:hover {
        &::-webkit-scrollbar-thumb {
          background: $inactive_text;
          border-right: 4px solid $form_background;
          border-radius: 2px 5px 5px 2px;
        }
      }
    }

    > .logout {
      padding: 20px;
      font-size: 14px;
      font-weight: bold;
      line-height: 20px;
      cursor: pointer;
      transition: opacity 0.1s;

      &:hover {
        color: $error_color;
      }
    }
  }

  > .content {
    display: table;
    width: 70%;
    height: 100%;

    > .placeholder {
      display: table-cell;
      vertical-align: middle;
      font-size: 14px;
      text-align: center;

      > .label {
        display: inline-block;
        background: $form_background;
        color: $default_text;
        border-radius: 15px;
        padding: 5px 10px;
      }
    }
  }
}
</style>
