<template>
  <div class="user_preview" :style="style_for_icon">
    <i v-if="is_favorites" class="material-icons">star_border</i>
    <template v-else>
      {{ user_preview }}
    </template>
  </div>
</template>

<script lang="coffee">
import colors from "./../css/colors.scss"

export default {
  props: {
    current_user: {type: String, required: true}
    login: {type: String, required: true}
    without_favorites: {type: Boolean, default: false}
  }

  computed: {
    user_preview: () ->
      return @login.slice(0, 2)

    is_favorites: () ->
      if @without_favorites
        return false
      else
        return @current_user == @login

    style_for_icon: () ->
      color_id = String(@login[0].charCodeAt())[0] % 4
      return {
        background: colors['color_' + (color_id + 1)]
      }
  }
}
</script>

<style lang="scss">
.user_preview {
  width: 44px;
  height: 44px;
  line-height: 44px;
  border-radius: 10px;
  text-align: center;

  > i {
    line-height: 44px;
  }
}
</style>
