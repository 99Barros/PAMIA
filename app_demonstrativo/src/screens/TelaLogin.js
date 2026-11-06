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
  StatusBar
} from 'react-native';

export default function TelaLogin({ navigation, route }) {
  // Recebe o parâmetro da tela anterior (se é 'passageiro' ou 'motorista')
  // Usamos um fallback caso não venha nada, para evitar quebras no app
  const { userType } = route.params || { userType: 'Passageiro' };
  
  // Gerenciamento de Estado para os inputs
  const [cpf, setCpf] = useState('');
  const [senha, setSenha] = useState('');

  const handleLogin = () => {
    // No futuro, conectaremos isso à validação no SQLite local.
    // Por hora, simulamos a entrada guiando o usuário para o Menu Principal.
    navigation.navigate('MenuPrincipal');
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#131422" />
      
      {/* KeyboardAvoidingView evita que o teclado cubra os inputs na tela do celular */}
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardContainer}
      >
        <Text style={styles.titleText}>Login</Text>
        
        {/* Feedback visual sutil de qual fluxo o usuário escolheu */}
        <Text style={styles.userTypeText}>Modo: {userType}</Text>

        <View style={styles.formContainer}>
          <TextInput
            style={styles.input}
            placeholder="CPF"
            placeholderTextColor="#666"
            keyboardType="numeric" // Facilita mostrando apenas números no celular
            value={cpf}
            onChangeText={setCpf}
          />
          
          <TextInput
            style={styles.input}
            placeholder="Senha"
            placeholderTextColor="#666"
            secureTextEntry={true} // Esconde a senha com "pontinhos"
            value={senha}
            onChangeText={setSenha}
          />

          <TouchableOpacity 
            style={styles.primaryButton}
            onPress={handleLogin}
          >
            <Text style={styles.buttonText}>Entrar</Text>
          </TouchableOpacity>

          {/* Botão de redirecionamento estratégico para o Cadastro */}
          <TouchableOpacity 
            style={styles.linkButton}
            onPress={() => navigation.navigate('Cadastro')}
          >
            <Text style={styles.linkText}>Cadastre-se</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

// Folha de Estilos
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#131422',
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
    backgroundColor: '#1E1E30', // Levemente mais claro que o fundo para destacar
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