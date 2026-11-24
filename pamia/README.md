# PAMIA — App de demonstração

Aplicativo React Native com Expo SDK 56 para o projeto de prevenção ao assédio
contra mulheres (ODS 5 e 11). A integração atual consulta a versão da PAMIA SDK
na tela inicial. Detecção, processamento de IA e persistência ainda são planejados.

## Equipe

- Caio Rocha
- Guilherme Spinola
- João Barros
- Paulo Henrique

## Preparar o ambiente Android

Instale Node.js, JDK 17 e Android Studio. No Android Studio, abra **SDK Manager →
SDK Tools → Show Package Details** e instale os componentes usados pelo app:

- Android SDK Platform 36 (na aba SDK Platforms).
- Android SDK Build-Tools 36.0.0.
- NDK (Side by side) 27.1.12297006.
- CMake 3.22.1.
- Android SDK Platform-Tools.

Em **Device Manager**, inicie um emulador. Também é possível usar um celular com
depuração USB ativada e autorizada. Para abrir o projeto nativo no Android Studio,
selecione a pasta `android` dentro deste app, depois de ela ter sido gerada.

## Executar o app no Windows

Abra o terminal na pasta que contém este README e o `package.json`.
No Prompt de Comando (CMD):

```bat
set "JAVA_HOME=C:\Program Files\Java\jdk-17"
set "PATH=%JAVA_HOME%\bin;%PATH%"
set "ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk"
npm ci
npm run android
```

Se usar PowerShell, configure as variáveis assim antes dos mesmos comandos npm:

```powershell
$env:JAVA_HOME = 'C:/Program Files/Java/jdk-17'
$env:PATH = "$env:JAVA_HOME/bin;$env:PATH"
$env:ANDROID_HOME = "$env:LOCALAPPDATA/Android/Sdk"
```

Adapte os caminhos caso suas instalações estejam em outro local. Confirme com
`java -version` que está usando Java 17. Essas variáveis valem para o terminal atual.

`npm ci` instala as dependências JavaScript conforme o arquivo de lock e só precisa
ser repetido ao preparar o projeto ou atualizar essas dependências. `npm run android`
gera a pasta Android quando necessário, compila e instala o app no dispositivo e
inicia o servidor JavaScript. Mantenha o terminal aberto durante o teste.

**Use o aplicativo próprio, não o Expo Go:** nossa biblioteca Android não está
incluída no Expo Go. A primeira construção pode demorar para baixar ferramentas
e dependências. Depois, alterações apenas nas telas podem usar `npm start` com
o app próprio já instalado; mudanças nativas exigem `npm run android` novamente.

## Como a biblioteca é utilizada

O app utiliza **v0.1.0-alpha.2**, baixada do JitPack. Não precisa copiar um AAR,
clonar o repositório da SDK nem compilar a biblioteca separadamente.

A configuração está em `modules/pamia/android/build.gradle`:

```groovy
repositories {
    maven { url 'https://jitpack.io' }
}

dependencies {
    implementation("com.github.DevSpinola:pamia-sdk:v0.1.0-alpha.2")
}
```

O Gradle baixa a biblioteca compilada e seus metadados, guarda no cache local e
inclui seu código no APK. O celular não consulta o JitPack para executar a SDK.
O cache normalmente fica em `%USERPROFILE%\.gradle\caches`; se houver
`GRADLE_USER_HOME`, fica dentro desse diretório. Não edite o cache manualmente.

A tela inicial chama a ponte Expo, que chama `Pamia.obterVersao()` na SDK Java.
O texto `PAMIA SDK ...` mostra a resposta real da biblioteca, não um número fixo
no JavaScript. A versão retornada pode preservar o prefixo `v` da publicação.

## Atualizar a SDK

1. Publique uma nova tag da SDK e confirme a construção no JitPack.
2. Em `modules/pamia/android/build.gradle`, substitua somente a versão da
   dependência pela nova versão publicada, mantendo o nome exato, inclusive `v`.
3. Com Java 17 configurado e o emulador ou celular conectado, execute:

```bat
npm run android
```

4. Confira a versão na tela inicial do aplicativo reinstalado.

Só recarregar o JavaScript não atualiza a SDK. Publicar uma versão nova também
não atualiza automaticamente o app: ele continua usando a versão declarada.
Para voltar a uma versão anterior, altere a dependência e recompile. A versão
`0.1.0-alpha.1` não possui `obterVersao()` e não atende a esta integração.

## Arquivos da integração

- `modules/pamia/android/build.gradle`: endereço JitPack e versão da SDK.
- `modules/pamia/expo-module.config.json`: registra a ponte no Expo.
- `modules/pamia/android/src/main/java/br/com/pamia/bridge/PamiaModule.kt`:
  encaminha a chamada para a SDK Java, sem lógica de detecção.
- `src/components/sdk-version.tsx`: consulta e exibe a versão.
- `src/app/index.tsx`: inclui o componente na tela inicial.

Edite a integração em `modules/`, não nas pastas geradas. A configuração sobrevive
à regeneração do projeto Android. AARs, caches, `node_modules` e resultados de build
não devem ser versionados. O fluxo antigo de cópia de AAR local foi removido.

## Problemas comuns

- **SDK location not found:** confira `ANDROID_HOME` no terminal. Como alternativa,
  `android/local.properties` pode conter `sdk.dir=C:/Users/SEU_USUARIO/AppData/Local/Android/Sdk`.
  Esse arquivo é local, não deve ser versionado e precisa ser recriado se a pasta
  Android for apagada.
- **NDK sem source.properties:** reinstale a versão 27.1.12297006 no SDK Manager;
  instalar outra versão não substitui a exigida pelo projeto.
- **Erro de acesso restrito do Java:** confira Java 17; depois execute
  `android\gradlew.bat --stop` antes de tentar `npm run android` novamente.
- **Dependência não encontrada:** confirme o nome da tag, o sucesso no JitPack,
  a conexão e o acesso ao repositório. Não substitua por um AAR antigo.
- **SDK não incluída nesta instalação:** abra o app próprio `br.com.pamia.demo`
  e recompile; o Expo Go não contém a ponte.

## Organização da equipe

- Limite de WIP: quatro tarefas simultâneas na coluna Em Execução (uma por integrante).
- Daily Sync: alinhamento e resolução de impedimentos.
- Revisão por outro integrante antes de concluir uma tarefa.
- Testes futuros de IA poderão usar vídeos locais para reduzir a dependência
  da câmera e do desempenho do emulador.
