import React from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  TouchableOpacity, 
  SafeAreaView, 
  StatusBar 
} from 'react-native';

export default function TelaInicial({ navigation }) {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#131422" />
      
      {/* Container do Logotipo e Subtítulo */}
      <View style={styles.logoContainer}>
        <Text style={styles.logoText}>PAMIA</Text>
        <Text style={styles.subtitleText}>Mobilidade Inteligente</Text>
      </View>

      {/* Container dos Botões de Navegação */}
      <View style={styles.buttonsContainer}>
        {/* Botão Passageiro (Usuário) */}
        <TouchableOpacity 
          style={styles.primaryButton}
          onPress={() => navigation.navigate('Login', { userType: 'passageiro' })}
        >
          <Text style={styles.buttonText}>Passageiro</Text>
        </TouchableOpacity>

        {/* Botão Motorista */}
        <TouchableOpacity 
          style={styles.secondaryButton}
          onPress={() => navigation.navigate('Login', { userType: 'motorista' })}
        >
          <Text style={styles.buttonText}>Motorista</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

// Folha de Estilos
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#131422', // Fundo escuro focado na identidade sóbria
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 30,
  },
  logoContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  logoText: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#6C63FF', // Cor de destaque principal (Azul/Roxo)
    letterSpacing: 2,
    marginBottom: 10,
  },
  subtitleText: {
    fontSize: 14,
    color: '#FFFFFF',
    fontWeight: '500',
  },
  buttonsContainer: {
    width: '100%',
    paddingBottom: 60,
    gap: 20, // Espaçamento entre os botões
  },
  primaryButton: {
    backgroundColor: '#6C63FF',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
    width: '100%',
  },
  secondaryButton: {
    backgroundColor: '#2A2A40', // Cor secundária para contraste tátil
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
    width: '100%',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
});