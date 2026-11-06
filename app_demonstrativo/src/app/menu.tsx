import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  StatusBar,
  ScrollView,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';

const MENU_PASSAGEIRO = [
  { label: 'Minhas Viagens', icon: '🗺️' },
  { label: 'Reportar Incidente', icon: '⚠️' },
  { label: 'Configurações', icon: '⚙️' },
];

const MENU_MOTORISTA = [
  { label: 'Minhas Corridas', icon: '🚗' },
  { label: 'Histórico', icon: '📋' },
  { label: 'Configurações', icon: '⚙️' },
];

export default function MenuPrincipal() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const userType = (params.userType as string) ?? 'passageiro';
  const isMotorista = userType === 'motorista';

  const menuItems = isMotorista ? MENU_MOTORISTA : MENU_PASSAGEIRO;

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#131422" />

      <TouchableOpacity style={styles.backButton} onPress={() => router.replace('/' as any)}>
        <Text style={styles.backArrow}>‹</Text>
        <Text style={styles.backText}>Início</Text>
      </TouchableOpacity>

      <View style={styles.header}>
        <Text style={styles.welcomeText}>Bem-vindo,</Text>
        <Text style={styles.userTypeText}>{isMotorista ? 'Motorista' : 'Passageiro'}</Text>
      </View>

      <ScrollView contentContainerStyle={styles.menuContainer}>
        {menuItems.map((item, index) => (
          <TouchableOpacity key={index} style={styles.menuCard}>
            <Text style={styles.menuIcon}>{item.icon}</Text>
            <Text style={styles.menuLabel}>{item.label}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <TouchableOpacity style={styles.logoutButton} onPress={() => router.replace('/' as any)}>
        <Text style={styles.logoutText}>Sair</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#131422',
    paddingHorizontal: 20,
  },
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
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
  header: {
    paddingVertical: 30,
  },
  welcomeText: {
    fontSize: 16,
    color: '#8A8A9E',
  },
  userTypeText: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#FFFFFF',
    textTransform: 'capitalize',
  },
  menuContainer: {
    paddingBottom: 20,
    gap: 12,
  },
  menuCard: {
    backgroundColor: '#1E1E30',
    borderRadius: 12,
    padding: 20,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 15,
    borderWidth: 1,
    borderColor: '#2A2A40',
  },
  menuIcon: {
    fontSize: 24,
  },
  menuLabel: {
    fontSize: 16,
    color: '#FFFFFF',
    fontWeight: '500',
  },
  logoutButton: {
    marginBottom: 30,
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#2A2A40',
  },
  logoutText: {
    color: '#8A8A9E',
    fontSize: 16,
  },
});
