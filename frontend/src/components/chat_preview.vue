<template>
  <div class="chat_preview" :class="{ is_current: is_current }">
    <user_preview :current_user="current_user" :login="login" />
    <div class="labels">
      <div class="user">{{ login_label }}</div>
      <div class="tooltip" :class="{ short: message_time }">
        <div class="last_message">
          {{ last_message }}
        </div>
        <div v-if="message_time" class="message_time" v-html="message_time" />
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
    message_time: () ->
      unix_times = Object.keys(@user_messages)
      if unix_times.length == 0
        return undefined
      else
        return main_helpers.print_date(unix_times[0], true)

    is_current: () ->
      return @selected_user == @login

    is_favorites: () ->
      return @current_user == @login

    last_message: () ->
      datetimes = Object.keys(@user_messages)
      if datetimes.length == 0
        if @is_favorites
          return 'Здесь вы можете сохранить ваши заметки'
        else
          return @login + ' теперь в Qchat'
      else
        return @user_messages[datetimes[datetimes.length - 1]].message

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
    }

    > .tooltip {
      color: $second_text;
      font-size: 12px;

      &.short {
        display: flex;
        flex-direction: row;

        > .last_message {
          flex: 1 1 auto;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        > .message_time {
          flex: 0 0 auto;
        }
      }
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

    > .labels > .tooltip {
      color: $second_hover;
    }
  }
}
</style>
