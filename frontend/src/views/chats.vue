<template>
  <div v-if="chats" class="chats">
    <div class="list">
      <div class="login">
        {{ current_user }}
      </div>
      <div class="chats_container">
        <chat_preview
          v-for="(messages, login_with_bugfix) in sorted_chats"
          :key="login_with_bugfix"
          class="chat_preview"
          :chats="sorted_chats"
          :login="remove_bugfix_prefix(login_with_bugfix)"
          :current_user="current_user"
          :user_messages="messages"
          :selected_user="selected_user"
          v-on:click="selected_user = remove_bugfix_prefix(login_with_bugfix)"
        />
      </div>
      <div class="logout" v-on:click="$emit('logout', $event)">
        <i class="material-icons">exit_to_app</i> <span>Выйти</span>
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

BUGFIX_PREFIX = 'bugfix_'

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
      check_new_messages_func: undefined
    }

  computed: {
    sorted_chats: () ->
      result = {}
      by_users = {}
      for login, messages_infos of @chats
        login_max = 0
        messages_dates = Object.keys(messages_infos)
        messages_dates.sort()
        chat_info = {}
        for timestamp in messages_dates
          chat_info[timestamp] = messages_infos[timestamp]
          if timestamp > login_max
            login_max = timestamp
        if login_max not of by_users
          by_users[login_max] = {}
        by_users[login_max][login] = chat_info
      max_login_values = Object.keys(by_users)
      max_login_values.sort()
      max_login_values.reverse()
      for item in max_login_values
        for login, messages_infos of by_users[item]
          result[BUGFIX_PREFIX + login] = messages_infos
      return result

    messages: () ->
      return @sorted_chats[BUGFIX_PREFIX + @selected_user]
  }

  mounted: () ->
    chats = await window_helpers.send_query({action: 'get_chats'})
    @chats = chats
    @check_new_messages_func = @handler_new_message.bind(@)
    @check_new_user_func = @handler_new_user.bind(@)
    window_helpers.add_linstener('new_message', @check_new_messages_func)
    window_helpers.add_linstener('new_user', @check_new_user_func)

  beforeDestroyed: () ->
    window_helpers.remove_linstener('new_message', @check_new_messages_func)
    window_helpers.remove_linstener('new_user', @check_new_user_func)

  methods: {
    remove_bugfix_prefix: (login) ->
      return login.slice(BUGFIX_PREFIX.length)

    handler_new_user: (login) ->
      if login not of @chats
        @chats[login] = {}
      return

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

    > .login,
    > .logout {
      padding: 20px 20px 20px 24px;
      line-height: 20px;
      font-size: 14px;
      font-weight: bold;
    }

    > .login {
      border-bottom: 1px solid $default_background;
    }

    > .chats_container {
      height: calc(100% - 121px);
      overflow-y: scroll;

      &::-webkit-scrollbar {
        // TODO hover scroll
        // width: 8px;
        width: 0px;
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
      transition: opacity 0.1s;
      cursor: pointer;

      > i,
      > span {
        float: left;
        line-height: 20px;
      }

      > i {
        font-weight: normal;
        padding-right: 10px;
      }

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
