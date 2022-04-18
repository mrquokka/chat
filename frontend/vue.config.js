const { defineConfig } = require('@vue/cli-service');
const fs = require('fs');

module.exports = defineConfig({
  css: {
    loaderOptions: {
      css: {
        modules: {
          mode: 'icss'
        }
      }
    }
  },
  transpileDependencies: true,
  outputDir: './../static/',
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000'
      },
      '/socket.io': {
        target: 'http://localhost:5000',
      },
    }
  },
  configureWebpack: (function(args) {
    return additions = {
      resolve: {
        extensions: ['.coffee']
      },
      module: {
        rules: [
          {
            test: /\.coffee$/,
            loader: 'coffee-loader'
          }
        ]
      }
    };
  })
})
