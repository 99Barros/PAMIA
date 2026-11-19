import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, SafeAreaView, StatusBar, ScrollView, Image } from 'react-native';
import { useRouter } from 'expo-router';

type RidesDashboardProps = {
  title: string;
};

export function RidesDashboard({ title }: RidesDashboardProps) {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#131422" />

      <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
        <Text style={styles.backArrow}>‹</Text>
        <Text style={styles.backText}>Voltar</Text>
      </TouchableOpacity>

      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>{title}</Text>

        <View style={styles.card}>
          <Image
            source={require('../../assets/images/cv-inspiration-cabin.png')}
            style={styles.inspirationImage}
            resizeMode="cover"
          />
          <View style={styles.badge}>
            <Text style={styles.badgeText}>Em breve</Text>
          </View>
          <Text style={styles.caption}>
            Em breve: análise de visão computacional, identificando movimentos e
            situações de risco em tempo real durante a corrida.
          </Text>
        </View>
      </ScrollView>
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
  content: {
    paddingTop: 20,
    paddingBottom: 30,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 20,
  },
  card: {
    backgroundColor: '#1E1E30',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#2A2A40',
    overflow: 'hidden',
  },
  inspirationImage: {
    width: '100%',
    height: 220,
  },
  badge: {
    position: 'absolute',
    top: 12,
    right: 12,
    backgroundColor: 'rgba(108, 99, 255, 0.9)',
    borderRadius: 6,
    paddingHorizontal: 8,
    paddingVertical: 4,
  },
  badgeText: {
    color: '#FFFFFF',
    fontSize: 11,
    fontWeight: 'bold',
    letterSpacing: 0.5,
  },
  caption: {
    padding: 16,
    fontSize: 14,
    color: '#8A8A9E',
    lineHeight: 20,
  },
});
