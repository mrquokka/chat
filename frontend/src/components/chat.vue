<template>
  <div class="chat">
    <div class="messages">
      <div
        v-for="(message_info, timestamp) in parsed_messages"
        :key="timestamp"
        class="message"
        :class="{ is_receiver: message_info.receiver == current_user }"
      >
        {{ message_info.message }}
        <div class="datetime" v-html="timestamp" />
      </div>
    </div>
    <form class="text_container" v-on:submit.prevent.stop="confirm_form">
      <div contenteditable="true" v-on:input="edit_text" />
      <button><i class="material-icons">send</i></button>
    </form>
  </div>
</template>
<script lang="coffee">
export default {
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
    parsed_messages: () ->
      dates = []
      for timestamp in Object.keys(@messages)
        dates.push(timestamp)
      dates.sort()
      result = {}
      for date in dates
        result[new Date(date * 1000).toString()] = @messages[date]
      return result
  }

  methods: {
    edit_text: (event) ->
      @current_text = event.target.innerText

    confirm_form: () ->
      text = @current_text.trim()
      if text.length == 0
        return
      @$emit('send_message', text)
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

    > .message {
      float: left;
      clear: both;
      border-radius: 20px;
      padding: 20px;
      margin-bottom: 20px;
      background: $form_background;

      & > .datetime {
      }

      &.is_receiver {
        float: right;
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
