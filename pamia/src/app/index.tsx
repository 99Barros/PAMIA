import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  SafeAreaView,
  StatusBar,
  StyleSheet,
} from 'react-native';
import { useRouter } from 'expo-router';

export default function TelaInicial() {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#131422" />

      <View style={styles.logoContainer}>
        <Text style={styles.logoText}>PAMIA</Text>
        <Text style={styles.subtitleText}>Prevenção ao Assédio contra Mulheres com Inteligência Artificial</Text>
      </View>

      <View style={styles.buttonsContainer}>
        <TouchableOpacity
          style={styles.primaryButton}
          onPress={() =>
            router.push({ pathname: '/login', params: { userType: 'passageiro' } } as any)
          }
        >
          <Text style={styles.buttonText}>Passageiro</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.secondaryButton}
          onPress={() =>
            router.push({ pathname: '/login', params: { userType: 'motorista' } } as any)
          }
        >
          <Text style={styles.buttonText}>Motorista</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#131422',
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
    color: '#6C63FF',
    letterSpacing: 2,
    marginBottom: 10,
  },
  subtitleText: {
    fontSize: 13,
    color: '#FFFFFF',
    fontWeight: '500',
    textAlign: 'center',
    paddingHorizontal: 20,
  },
  buttonsContainer: {
    width: '100%',
    paddingBottom: 60,
    gap: 20,
  },
  primaryButton: {
    backgroundColor: '#6C63FF',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
    width: '100%',
  },
  secondaryButton: {
    backgroundColor: '#2A2A40',
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
