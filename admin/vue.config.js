module.exports = {
    chainWebpack: config => {
        config.module
          .rule('svg')
          .test(/\.svg$/)
          .use('file-loader')
          .loader('svg-sprite-loader')
          .options({
            symbolId: 'icon-[name]'
          })
    },
    publicPath: "admin-static/",
    devServer: {
      proxy: {
        '^/media': {
          target: 'http://localhost:8000',
          changeOrigin: true
        }
      }
    }
}
