<template>
  <div class="chat">
    <div ref="messages_container" class="messages">
      <div
        v-for="(message_info, timestamp) in messages"
        :key="timestamp"
        class="message_container"
        :class="{ is_receiver: message_info.receiver == current_user }"
      >
        <div class="message">
          <div class="text">{{ message_info.message }}</div>
          <div class="time_readed_info">
            <span>{{ print_date(timestamp) }}</span>
            <i
              v-if="!is_favorites"
              class="material-icons"
              v-html="get_read_icon(message_info)"
            />
          </div>
          <div class="clear_block" />
        </div>
        <user_preview
          :current_user="current_user"
          :login="message_info.receiver"
          :without_favorites="true"
        />
      </div>
    </div>
    <form class="text_container" v-on:submit.prevent.stop="confirm_form">
      <div
        ref="input"
        contenteditable="true"
        v-on:input="edit_text"
        v-on:keyup="handler_keyup"
      />
      <button><i class="material-icons">send</i></button>
    </form>
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
    selected_user: {type: String, required: true}
    messages: {type: Object, required: true}
  }

  emits: ['send_message']

  data: () ->
    return {
      current_text: ''
    }

  computed: {
    is_favorites: () ->
      return @current_user == @selected_user
  }

  mounted: () ->
    @$refs.input.focus()
    @scroll_to_bottom()

  watch: {
    messages: {
      deep: true

      handler: () ->
        @scroll_to_bottom()
    }
  }

  methods: {
    get_read_icon: (message_info) ->
      return main_helpers.get_read_icon(message_info.is_readed)

    scroll_to_bottom: () ->
      setTimeout(() =>
        messages_container = @$refs.messages_container
        messages_container.scrollTop = messages_container.scrollHeight
      )

    handler_keyup: (event) ->
      if event.code == 'Enter' and not event.ctrlKey and not event.shiftKey
        @confirm_form()
      return

    print_date: (unix_time) ->
      return main_helpers.print_date(unix_time, false)

    edit_text: (event) ->
      @current_text = event.target.innerText

    confirm_form: () ->
      text = @current_text.trim()
      if text.length == 0
        return
      @$emit('send_message', text)
      @current_text = ''
      @$refs.input.innerText = null
  }
}
</script>

<style lang="scss">
@import "./../css/colors.scss";

.chat {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;

  > .messages {
    overflow-y: auto;
    flex: 1 1 auto;
    padding: 20px;

    > .message_container {
      clear: both;
      position: relative;
      float: right;

      > .message {
        clear: both;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        background: $form_background;
        margin-right: 50px;

        > .text {
          word-break: break-all;
        }

        > .time_readed_info {
          font-size: 12px;
          padding-top: 10px;
          color: $active_button_background;
          float: right;

          > i {
            font-size: 17px;
            padding-left: 5px;
            display: block;
            float: right;
          }
        }
      }

      > .user_preview {
        position: absolute;
        bottom: 22px;
        right: 0px;
      }

      &.is_receiver {
        float: left;

        > .message {
          margin-right: unset;
          margin-left: 50px;

          > .time_readed_info {
            float: left;
          }
        }

        > .user_preview {
          right: unset;
          left: 0px;
        }
      }
    }
  }

  > .text_container {
    flex: 0 0 auto;
    background: #1e1e2d;
    border-left: 1px solid $default_background;
    position: relative;

    > div,
    > button {
      color: $default_text;
      background: unset;
      outline: none;
      border: none;
    }

    > div {
      padding: 25px 90px 25px 20px;
      width: calc(100% - 110px);
    }

    > button {
      position: absolute;
      bottom: 0px;
      right: 20px;
      cursor: pointer;

      > i {
        font-size: 24px;
        line-height: 56px;
        color: $active_hover_button_background;
      }
    }
  }
}
</style>
