// src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import { AppRegistry } from 'react-native';
import App from './App';
import { BrowserRouter } from 'react-router-dom';
import { name as appName } from './app.json';  // Assurez-vous que app.json contient le nom de votre application

AppRegistry.registerComponent(appName, () => App);

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
