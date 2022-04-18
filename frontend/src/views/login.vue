<template>
  <div class="home">
    <div class="vertical_center">
      <form v-on:submit.prevent.stop="confirm_form">
        <div class="header">
          <div class="label" v-html="header_text" />
          <span class="inactive" v-html="inactive_header" />
          <router-link
            class="register_label"
            :to="{ name: header_route_name }"
            v-html="header_link"
          />
        </div>

        <div
          v-for="(field_info, field_name) in fields"
          :key="field_name"
          class="field"
        >
          <div class="label" v-html="field_info.label" />
          <input
            v-model="field_info.value"
            :class="{ with_error: field_info.error }"
            :type="field_info.type"
            v-on:input="handler_input(field_name, $event)"
          />
          <div class="error_message">
            <span v-html="field_info.error" />
          </div>
        </div>
        <button>
          Войти
        </button>
      </form>
    </div>
  </div>
</template>

<script lang="coffee">
import window_helpers from './../helpers/window.coffee'

export default {
  emits: ['success_login']

  data: () ->
    return {
      login: undefined
      password: undefined
      is_already_exists: false
      is_show_password_error: false
      exists_logins: []
    }

  computed: {
    header_text: () ->
      if @is_on_register
        return 'Регистрация'
      else
        return 'Добро пожаловать в QChat'

    inactive_header: () ->
      if @is_on_register
        return 'Уже зарегестрированы?'
      else
        return 'Впервые?'

    header_link: () ->
      if @is_on_register
        return 'Войти в систему'
      else
        return 'Создать аккаунт'

    header_route_name: () ->
      if @is_on_register
        return 'login'
      else
        return 'register'

    is_on_register: () ->
      return @$route.name == 'register'

    required_error: () ->
      return 'Обязательное поле'

    invalid_login_password: () ->
      return 'Неверный логин/пароль'

    password_error: () ->
      if @is_show_password_error
        return @invalid_login_password
      else if @is_empty_value(@password)
        return @required_error
      else
        return undefined

    name_error: () ->
      if @is_empty_value(@login)
        return @required_error
      else if @is_on_register and @login in @exists_logins
        return 'Это имя уже занято'
      else if @is_show_password_error
        return @invalid_login_password
      else
        return undefined

    fields: () ->
      return {
        login: {
          label: 'Логин'
          type: 'text'
          value: @login
          error: @name_error
        }
        password: {
          label: 'Пароль'
          type: 'password'
          value: @password
          error: @password_error
        }
      }
  }

  methods: {
    is_empty_value: (value) ->
      return not value? or value.trim().length == 0

    handler_input: (field_name, event) ->
      @[field_name] = event.target.value
      @is_show_password_error = false

    confirm_form: () ->
      if @name_error? or @password_error?
        return
      if @is_on_register
        action = 'register'
      else
        action = 'login'
      result = await window_helpers.send_query({
        action: action
        login: @login
        password: @password
      })
      if result == 'OK'
        @$emit("success_login", true)
      else if result == 'invalid password'
        console.log 'set'
        @is_show_password_error = true
      else if result == 'error_is_busy'
        @exists_logins.push(@login)
      return
  }
}
</script>

<style lang="scss">
@import "./../css/colors.scss";

.home {
  display: table;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;

  > .vertical_center {
    display: table-cell;
    vertical-align: middle;

    > form {
      margin: 0 auto;
      width: fit-content;
      background: $form_background;
      border-radius: 6px;
      padding: 30px 40px;

      > .header {
        margin: 0 auto;
        text-align: center;
        padding-bottom: 32px;

        > div {
          font-weight: bold;
          padding-bottom: 10px;
        }

        > .inactive {
          color: $inactive_text;
          padding-right: 3px;
        }

        > .register_label {
          color: $active_button_background;
          cursor: pointer;
          text-decoration: none;
        }
      }

      > .field {
        padding-bottom: 32px;

        > .label {
          font-size: 14px;
          font-weight: bold;
          padding-bottom: 7px;
        }

        > input {
          background: $input_background;
          color: $input_color;
          padding: 10px 20px;
          border: unset;
          border-radius: 8px;
          width: 360px;

          &.with_error {
            box-shadow: 0px 0px 2px $error_color;
          }
        }

        > .error_message {
          font-size: 12px;
          height: 16px;
          line-height: 16px;
          color: $error_color;
        }
      }

      > button {
        font-size: 12px;
        color: $default_text;
        background: $active_button_background;
        border: unset;
        border-radius: 8px;
        width: 100%;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;

        &:hover {
          background: $active_hover_button_background;
        }
      }
    }
  }
}
</style>
