const webpack = require('webpack');
const path = require('path');

module.exports = {
    context: path.resolve(__dirname, "./src/js"),
    entry: {
        main: './main.js',
        productPage: './productPage.js',
        catalogPage: './catalogPage.js',
        cartPage: './cartPage.js'
    },
    output: {
        path: path.resolve(__dirname, './dist/js'),
        publicPath: '/dist/js/',
        filename: '[name].js'
    },
    resolve: {
        extensions: ['.js', '.json'],
        alias: {
            '@': path.join(__dirname, './src/js')
        }
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                  loader: "babel-loader"
                }
            }
        ]
    },
    optimization: {
        runtimeChunk: {
            name: "common"
        },
        splitChunks: {
            cacheGroups: {
                common: {
                    name: 'common',
                    chunks: 'all'
                }
            }
        }
    },
    devServer: {
        contentBase: path.join(__dirname, './src/js'),
        compress: true,
        port: 8080,
        hot: true,
        publicPath: "/static/js/",
        proxy: {
            "/": "http://localhost:8000"
        },
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin()
    ]
};