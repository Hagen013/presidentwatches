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
    }
}
