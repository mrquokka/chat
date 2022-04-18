<template>
  <div v-if="chats" class="chats">
    <div class="list">
      <chat_preview
        v-for="login in Object.keys(chats)"
        :key="login"
        class="chat_preview"
        :chats="chats"
        :login="login"
      />
    </div>
    <div class="content">
      <chat v-if="selected_user" />
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

  data: () ->
    return {
      chats: undefined
      selected_user: undefined
    }

  mounted: () ->
    chats = await window_helpers.get_chats()
    @chats = chats
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
