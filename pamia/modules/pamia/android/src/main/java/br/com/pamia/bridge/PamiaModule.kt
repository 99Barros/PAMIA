package br.com.pamia.bridge

import br.com.pamia.sdk.Pamia
import expo.modules.kotlin.modules.Module
import expo.modules.kotlin.modules.ModuleDefinition

// Esta ponte apenas expõe a função Java da SDK para o JavaScript do app.
class PamiaModule : Module() {
    override fun definition() = ModuleDefinition {
        Name("Pamia")
        Function("obterVersao") { Pamia.obterVersao() }
        Function("olaMundo") { Pamia.olaMundo() }
    }
}
