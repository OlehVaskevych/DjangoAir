const path = require('path')
const {VueLoaderPlugin} = require("vue-loader");

module.exports = {
    entry: {
        main: './assets/scripts/index.js',
    },
    output: {
        filename: "[name].bundle.js",
        path: path.resolve(__dirname, 'static')
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: /node_modules/,
            },
            {
                test: /\.css$/,
                oneOf: [
                    // Якщо CSS імпортується з .vue файлів
                    {
                        resourceQuery: /vue/,
                        use: ['vue-style-loader', 'css-loader']
                    },
                    // Якщо це звичайний CSS (наприклад bootstrap.css)
                    {
                        use: ['style-loader', 'css-loader']
                    }
                ]
            },
            {
              test: /\.(png|jpe?g|gif|svg)$/i,
              type: 'asset/resource',
              generator: {
                filename: 'images/[name][ext]'
              }
            }
        ]
    },
    resolve: {
        alias: {
            '@': path.resolve(__dirname, 'assets'),
            vue: '@vue/runtime-dom'
        },
        extensions: ['.js', '.vue']
    },
    plugins: [
        new VueLoaderPlugin()
    ],
    mode: 'development'
};