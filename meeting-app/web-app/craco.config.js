const path = require('path');
const { getLoader, loaderByName } = require('@craco/craco');

module.exports = {
  webpack: {
    alias: {
      'react-native$': 'react-native-web',
    },
    configure: (webpackConfig, { env, paths }) => {
      const { isFound, match } = getLoader(webpackConfig, loaderByName('babel-loader'));
      if (isFound) {
        match.loader.include = [
          ...match.loader.include,
          path.resolve(__dirname, 'node_modules/react-native-web'), // Utilisez path.resolve pour obtenir un chemin absolu
        ];
      }
      return webpackConfig;
    },
  },
};
