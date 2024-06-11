import React, { useEffect } from 'react';
import {
  SafeAreaView,
  StatusBar,
  Text,
} from 'react-native';

import './core/fontawesome';

import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import SplashScreen from './screens/Splash';
import SignInScreen from './screens/SignIn'; 
import HomeScreen from './screens/Home';
import SearchScreen from './screens/Search';
import MessagesScreen from './screens/Messages';
import SignUpScreen from './screens/SignUp';

import useGlobal from './core/global';

const lightTheme = {
  colors: {
    background: 'white',
  },
};

const Stack = createNativeStackNavigator();

function App() {
  const initialized = useGlobal(state => state.authenticated);
  const authenticated = useGlobal(state => state.authenticated);
  const init = useGlobal(state => state.init);

  useEffect(() => {
    init();
  }, [init]);

  return (
    <NavigationContainer theme={lightTheme}>
      <StatusBar barStyle='dark-context' />
      <SafeAreaView style={{ flex: 1 }}>
        <Stack.Navigator>
          {!initialized ? (
            <Stack.Screen name="Splash" component={SplashScreen} />
          ) : !authenticated ? (
            <>
              <Stack.Screen name="SignIn" component={SignInScreen} />
              <Stack.Screen name="SignUp" component={SignUpScreen} />
            </>
          ) : (
            <>
              <Stack.Screen name="Home" component={HomeScreen} />
              <Stack.Screen name="Search" component={SearchScreen} />
              <Stack.Screen name="Messages" component={MessagesScreen} />
            </>
          )}
        </Stack.Navigator>
      </SafeAreaView>
    </NavigationContainer>
  );
}

export default App;
