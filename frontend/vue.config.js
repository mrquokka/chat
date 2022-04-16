const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: './../static/',
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000'
      },
    }
  }
})
