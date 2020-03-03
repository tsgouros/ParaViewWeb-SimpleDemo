var path = require('path');
var HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: ['./src/index.js'],
  output: {
    path: path.resolve(__dirname, 'www'), // Was __dirname + '/www'
    filename: 'SimpleDemoClient.js'

  },

  devtool: 'source-map',

  module: {
    rules: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        options: { presets: ['@babel/preset-env', '@babel/preset-react'] }
      },
      {
        test: /\.m?css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.(eot|svg|ttf|woff|woff2)$/,
        loader: 'file-loader?name=public/fonts/[name].[ext]'
      }
    ]
  },

  resolve: {
    alias: {
      PVWStyle: path.resolve('./node_modules/paraviewweb/style'),
    },
  },

  stats: {
    errorDetails: true
  },

  plugins: [
    new HtmlWebpackPlugin({
      title: "ParaViewWeb-SimpleDemo",
      filename: 'index.html'
    }),
  ]
};
