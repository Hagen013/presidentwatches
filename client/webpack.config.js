const webpack = require('webpack');
const path = require('path');


module.exports = (env, argv) => {

    const mode = argv.mode;
    let GEO_SERVICE_HOST = "";

    if (mode === 'production') {
        GEO_SERVICE_HOST = "'http://5.189.227.162:8282'";
    } else {
        GEO_SERVICE_HOST = "'http://localhost:8282'";
    }

    return {
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
                        chunks: 'async'
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
            new webpack.HotModuleReplacementPlugin(),
            new webpack.DefinePlugin({
                'GEO_SERVICE_HOST': GEO_SERVICE_HOST
            })
        ]
    }
}
