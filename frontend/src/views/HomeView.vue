<template>
  <div class="home">
    <div class="vertical_center">
      <form v-on:submit.prevent.stop>
        <div
          v-for="(field_info, field_name) in fields"
          :key="field_name"
          class="field"
        >
          <div class="label" v-html="field_info.label" />
          <input
            v-model="field_info.value"
            :type="field_info.type"
            v-on:input="handler_input(field_name, $event)"
          />
          <div class="error_message">
            <span v-if="!field_info.value" v-html="required_error" />
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="coffee">
export default {
  data: () ->
    return {
      login: undefined
      password: undefined
      is_already_exists: false
    }

  computed: {
    required_error: () ->
      return 'Обязательное поле'

    fields: () ->
      return {
        login: {
          label: 'Логин'
          type: 'text'
          value: @login
        }
        password: {
          label: 'Пароль'
          type: 'password'
          value: @password
        }
      }
  }

  methods: {
    handler_input: (field_name, event) ->
      @[field_name] = event.target.value
  }
}
</script>

<style lang="scss">
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
    }
  }
}
</style>
