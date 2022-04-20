<template>
  <div v-if="color" class="chat_preview">
    <div class="icon" :style="style_for_icon">
      <i v-if="is_favorites" class="material-icons">star_border</i>
      <template v-else>
        {{ user_preview }}
      </template>
    </div>
    <div class="labels">
      <div class="user">{{ login_label }}</div>
      <div class="tooltip">{{ last_message }}</div>
    </div>
    <div class="clear_block" />
  </div>
</template>

<script lang="coffee">
import * as colors from "./../css/colors.scss"

export default {
  props: {
    current_user: {type: String, required: true}
    login: {type: String, required: true}
    chats: {type: Object, required: true}
    user_messages: {type: Object, required: true}
  }

  data: () ->
    return {color: undefined}

  computed: {
    is_favorites: () ->
      return @current_user == @login

    last_message: () ->
      datetimes = Object.keys(@user_messages)
      console.log datetimes
      if datetimes.length == 0
        if @is_favorites
          return 'Здесь вы можете сохранить ваши заметки'
        else
          return @login + ' теперь в Qchat'
      else
        console.log datetimes.length
        return @user_messages[datetimes[datetimes.length - 1]].message

    login_label: () ->
      if @is_favorites
        return 'Избранное'
      return @login

    user_preview: () ->
      return @login.slice(0, 2)

    style_for_icon: () ->
      return {
        background: @color
      }
  }

  mounted: () ->
    @color = @get_random_color()

  methods: {
    get_random_color: () ->
      color_id = Math.floor(Math.random() * 3) + 1
      return colors['color_' + color_id]
  }
}
</script>

<style lang="scss">
@import "./../css/colors.scss";

.chat_preview {
  padding: 20px;
  cursor: pointer;

  > .labels,
  > .icon {
    float: left;
  }

  > .icon {
    width: 44px;
    height: 44px;
    line-height: 44px;
    border-radius: 6px;
    text-align: center;

    > i {
      line-height: 44px;
    }
  }

  > .labels {
    padding-left: 17px;
    width: calc(100% - 62px);
    line-height: 22px;

    > .user {
      font-size: 14px;
    }

    > .tooltip {
      color: $second_text;
      font-size: 12px;
      white-space: nowrap;
      width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }

  &:hover {
    background: $input_background;
  }
}
</style>
