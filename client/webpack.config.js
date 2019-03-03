const webpack = require('webpack');
const path = require('path');

module.exports = {
    context: path.resolve(__dirname, "./src/js"),
    entry: {
        main: './main.js',
    },
    output: {
        path: path.resolve(__dirname, './dist/js'),
        publicPath: '/dist/js/',
        filename: '[name].js'
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
    devtool: 'inline-source-map',
    plugins: [
        new webpack.HotModuleReplacementPlugin()
    ]
};