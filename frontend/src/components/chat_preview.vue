<template>
  <div v-if="color" class="chat_preview">
    <div class="icon" :style="style_for_icon">
      {{ user_preview }}
    </div>
    <div class="labels">
      <div class="user">{{ login }}</div>
      <div class="tooltip">ds</div>
    </div>
    <div class="clear_block" />
  </div>
</template>

<script lang="coffee">
import * as colors from "./../css/colors.scss"

export default {
  props: {
    login: {type: String, required: true}
    chats: {type: Object, required: true}
  }

  data: () ->
    return {color: undefined}

  computed: {
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
    }
  }

  &:hover {
    background: $input_background;
  }
}
</style>
