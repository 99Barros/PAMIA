import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  KeyboardAvoidingView,
  Platform,
  StatusBar,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';

export default function TelaLogin() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const userType = (params.userType as string) ?? 'passageiro';

  const [cpf, setCpf] = useState('');
  const [senha, setSenha] = useState('');

  const formatCpf = (value: string) => {
    const digits = value.replace(/\D/g, '').slice(0, 11);
    return digits
      .replace(/(\d{3})(\d)/, '$1.$2')
      .replace(/(\d{3})(\d)/, '$1.$2')
      .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
  };

  const handleLogin = () => {
    router.push({ pathname: '/menu', params: { userType } } as any);
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#131422" />

      <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
        <Text style={styles.backArrow}>‹</Text>
        <Text style={styles.backText}>Voltar</Text>
      </TouchableOpacity>

      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardContainer}
      >
        <Text style={styles.titleText}>Login</Text>
        <Text style={styles.userTypeText}>Modo: {userType}</Text>

        <View style={styles.formContainer}>
          <TextInput
            style={styles.input}
            placeholder="CPF (xxx.xxx.xxx-xx)"
            placeholderTextColor="#666"
            keyboardType="numeric"
            maxLength={14}
            value={cpf}
            onChangeText={(text) => setCpf(formatCpf(text))}
          />

          <TextInput
            style={styles.input}
            placeholder="Senha"
            placeholderTextColor="#666"
            secureTextEntry
            value={senha}
            onChangeText={setSenha}
          />

          <TouchableOpacity style={styles.primaryButton} onPress={handleLogin}>
            <Text style={styles.buttonText}>Entrar</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.linkButton}
            onPress={() => router.push('/cadastro' as any)}
          >
            <Text style={styles.linkText}>Cadastre-se</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#131422',
  },
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 10,
    paddingBottom: 5,
    gap: 4,
  },
  backArrow: {
    fontSize: 28,
    color: '#6C63FF',
    lineHeight: 30,
  },
  backText: {
    fontSize: 16,
    color: '#6C63FF',
    fontWeight: '500',
  },
  keyboardContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 30,
  },
  titleText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 5,
  },
  userTypeText: {
    fontSize: 14,
    color: '#6C63FF',
    marginBottom: 40,
    textTransform: 'capitalize',
  },
  formContainer: {
    width: '100%',
    gap: 15,
  },
  input: {
    backgroundColor: '#1E1E30',
    color: '#FFFFFF',
    borderRadius: 8,
    paddingHorizontal: 15,
    paddingVertical: 15,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#2A2A40',
  },
  primaryButton: {
    backgroundColor: '#6C63FF',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
  linkButton: {
    marginTop: 15,
    alignItems: 'center',
    padding: 10,
  },
  linkText: {
    color: '#8A8A9E',
    fontSize: 14,
    fontWeight: '500',
  },
});
