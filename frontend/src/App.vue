<template>
  <div>
    <router-view />
  </div>
</template>

<style lang="scss">
export default {
}
</style>

<style lang="scss">
@import "./css/colors.scss";

body {
  background: $default_background;
  font-family: "Open Sans";
  color: $default_text;
  margin: 0px;
  padding: 0px;
}

a {
  text-decoration: none;
}

input:focus {
  outline: unset;
}
</style>
