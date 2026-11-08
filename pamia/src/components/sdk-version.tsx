import { requireOptionalNativeModule } from 'expo';
import { Platform, Text } from 'react-native';

export default function SdkVersion() {
  let label = 'SDK disponível no app Android';
  let olaMundo = '';
  if (Platform.OS === 'android') {
    try {
      // Optional evita derrubar as telas no Expo Go, onde a ponte não existe.
      const pamia = requireOptionalNativeModule('Pamia');
      label = pamia ? `PAMIA SDK ${pamia.obterVersao()}` : 'SDK não incluída nesta instalação';
      olaMundo =  pamia ? pamia.olaMundo() : 'Função Nao encontrada'
    } catch (error) {
      console.error('Falha ao consultar a PAMIA SDK:', error);
      label = 'Não foi possível consultar a SDK';
    }
  }
  return <>
    <Text style={{ color: '#B8B8CC', fontSize: 12, marginTop: 16 }}>{label}</Text>
    <Text style={{ color: '#B8B8CC', fontSize: 12, marginTop: 16 }}>{olaMundo}</Text>
  </>;
}
