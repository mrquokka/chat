<template>
  <div class="chat_preview" :class="{ is_current: is_current }">
    <user_preview :current_user="current_user" :login="login" />
    <div class="labels">
      <div class="user" :class="{ short: message_time }">
        <div class="login_label">
          {{ login_label }}
        </div>
        <div v-if="message_time" class="message_time_and_readed">
          <i v-if="readed_icon" class="material-icons" v-html="readed_icon" />
          {{ message_time }}
        </div>
      </div>
      <div class="tooltip">
        {{ last_message_description }}
      </div>
    </div>
    <div class="clear_block" />
  </div>
</template>

<script lang="coffee">
import user_preview from './user_preview.vue'
import main_helpers from './../helpers/main.coffee'

export default {
  components: {
    user_preview: user_preview
  }

  props: {
    current_user: {type: String, required: true}
    selected_user: {type: String, default: () -> return undefined}
    login: {type: String, required: true}
    chats: {type: Object, required: true}
    user_messages: {type: Object, required: true}
  }

  computed: {
    last_message_time: () ->
      unix_times = Object.keys(@user_messages)
      if unix_times.length == 0
        return undefined
      else
        return unix_times[unix_times.length - 1]

    last_message: () ->
      if @last_message_time?
        return @user_messages[@last_message_time]
      else
        return undefined

    last_message_description: () ->
      if @last_message?
        description = @last_message.message
        if @last_message.sender == @current_user
          description = 'Вы: ' + description
        return description
      else
        if @is_favorites
          return 'Здесь вы можете сохранить ваши заметки'
        else
          return @login + ' теперь в Qchat'

    readed_icon: () ->
      if @last_message? and not @is_favorites
        if @last_message.is_readed
          return 'done_all'
        else
          return 'done'
      else
        return undefined

    message_time: () ->
      if @last_message?
        return main_helpers.print_date(@last_message_time, true)
      else
        return undefined

    is_current: () ->
      return @selected_user == @login

    is_favorites: () ->
      return @current_user == @login

    login_label: () ->
      if @is_favorites
        return 'Избранное'
      return @login
  }
}
</script>

<style lang="scss">
@import "./../css/colors.scss";

.chat_preview {
  padding: 20px;
  cursor: pointer;

  > .labels,
  > .user_preview {
    float: left;
  }

  > .labels {
    padding-left: 17px;
    width: calc(100% - 62px);
    line-height: 22px;

    > .user,
    > .tooltip,
    > .last_message {
      white-space: nowrap;
      width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    > .user {
      font-size: 14px;

      &.short {
        display: flex;
        flex-direction: row;

        > .login_label {
          flex: 1 1 auto;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        > .message_time_and_readed {
          flex: 0 0 auto;

          > i {
            font-size: 12px;
          }
        }
      }
    }

    > .tooltip,
    > .user > .message_time_and_readed {
      color: $second_text;
      font-size: 12px;
    }
  }

  &:hover {
    background: $input_background;
  }

  &.is_current {
    background: $active_button_background;

    > .user_preview {
      box-shadow: 0px 0px 4px $second_text;
    }

    > .labels {
      > .user > .message_time,
      > .tooltip {
        color: $second_hover;
      }
    }
  }
}
</style>
