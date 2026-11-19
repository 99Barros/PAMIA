import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

// Importe a tela que criamos
import TelaInicial from './TelaInicial'; 

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {/* A Tela Inicial é a primeira a carregar */}
        <Stack.Screen name="Inicial" component={TelaInicial} />
        
        {/* Placeholder para a próxima tela que faremos */}
        <Stack.Screen name="Login" component={TelaInicial} /> 
      </Stack.Navigator>
    </NavigationContainer>
  );
}