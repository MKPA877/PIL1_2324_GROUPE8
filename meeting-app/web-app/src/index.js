import React from 'react';
import ReactDOM from 'react-dom';
import { AppRegistry } from 'react-native';
import App from './App';
import { BrowserRouter } from 'react-router-dom';
import appConfig from './app.json';  

// Utilisez la propriété name de l'objet app.json
const { name: appName } = appConfig;

// Enregistrez le composant racine de votre application avec AppRegistry
AppRegistry.registerComponent(appName, () => App);

// Définissez le WrapperComponent comme BrowserRouter
const rootTag = document.getElementById('root');
AppRegistry.runApplication(appName, {
  initialProps: {},
  rootTag,
  WrapperComponent: BrowserRouter,
});


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
//reportWebVitals();
