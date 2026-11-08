import { requireOptionalNativeModule } from 'expo';
import { Platform, Text } from 'react-native';

export default function SdkVersion() {
  let label = 'SDK disponível no app Android';
  if (Platform.OS === 'android') {
    try {
      // Optional evita derrubar as telas no Expo Go, onde a ponte não existe.
      const pamia = requireOptionalNativeModule<{ obterVersao(): string }>('Pamia');
      label = pamia ? `PAMIA SDK ${pamia.obterVersao()}` : 'SDK não incluída nesta instalação';
    } catch (error) {
      console.error('Falha ao consultar a PAMIA SDK:', error);
      label = 'Não foi possível consultar a SDK';
    }
  }
  return <Text style={{ color: '#B8B8CC', fontSize: 12, marginTop: 16 }}>{label}</Text>;
}
