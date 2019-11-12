var path = require('path');
var HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: './src/index.jsx',
    output: {
        path: path.resolve('dist'),
        filename: 'bundle.js'
    },
    resolve: {
        extensions: ['.js', '.jsx']
    },
    module: {
        rules: [
			{
				test: /\.css$/,
				use: ['style-loader', 'css-loader']
			},
            {
                test: /\.jsx?$/,
                exclude: /(node_modules|bower_components)/,
                loader: 'babel-loader',
                query: {
                    presets: ['react', 'es2015', 'stage-3']
                }
            },
            { 
				test: /\.json$/, 
				loader: 'json-loader' 
			},
        ]
    },
    plugins: [new HtmlWebpackPlugin({
        template: './src/index.html',
        filename: 'index.html',
        inject: 'body'
    })],
    devtool: config.build.productionSourceMap ? config.build.devtool : false,
    devServer: {
	disableHostCheck: true,
        clientLogLevel: 'warning',
        historyApiFallback: true, 
	hot: false,
        host: '0.0.0.0',
        port: process.env.PORT || config.dev.port,
        open: false,
        overlay: false,
        publicPath: config.dev.assetsPublicPath,
        proxy: config.dev.proxyTable,
        quiet: true
    },
    externals: {
        // global app config object
        config: JSON.stringify({
            apiUrl: 'https://oceaneyesbe.herokuapp.com'
        })
    }
}
