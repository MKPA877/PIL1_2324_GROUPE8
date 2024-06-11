const path = require('path');
const { getLoader, loaderByName } = require('@craco/craco');

module.exports = {
  webpack: {
    alias: {
      'react-native$': 'react-native-web',
      '@core': path.resolve(__dirname, 'src/core/'),
      '@assets': path.resolve(__dirname, 'src/assets/'),
      '@common': path.resolve(__dirname, 'src/common/'),
      '@screens': path.resolve(__dirname, 'src/screens/'),
    },
    configure: (webpackConfig, { env, paths }) => {
      const { isFound, match } = getLoader(webpackConfig, loaderByName('babel-loader'));
      if (isFound) {
        match.loader.include = [
          ...(Array.isArray(match.loader.include) ? match.loader.include : [match.loader.include]),
          path.resolve(__dirname, 'node_modules/react-native-web'), // Utilisez path.resolve pour obtenir un chemin absolu
        ];
      }
      return webpackConfig;
    },
  },
};
