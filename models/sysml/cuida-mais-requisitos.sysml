package CuidaMais_Sprint1 {
  // Requisitos funcionais associados às 12 funcionalidades.
  requirement RF01 {
    doc /* F01: O sistema deve permitir registar e atualizar a conta do idoso com dados pessoais e clínicos válidos. */
  }
  requirement RF02 {
    doc /* F02: O sistema deve permitir adicionar contactos familiares e definir a prioridade de notificação. */
  }
  requirement RF03 {
    doc /* F03: O sistema deve detetar uma queda provável, criar um alerta e notificar os contactos por prioridade. */
  }
  requirement RF04 {
    doc /* F04: O sistema deve registar sistólica, diastólica e pulso, classificar e conservar o histórico. */
  }
  requirement RF05 {
    doc /* F05: O sistema deve controlar horários, libertação e omissão de doses de medicação. */
  }
  requirement RF06 {
    doc /* F06: O sistema deve detetar risco doméstico e comandar o corte seguro de gás ou energia. */
  }
  requirement RF07 {
    doc /* F07: O sistema deve ajustar iluminação e temperatura segundo presença, horário e condições ambientais. */
  }
  requirement RF08 {
    doc /* F08: O sistema deve receber sinais vitais do wearable, identificar anomalias e atualizar o painel clínico. */
  }
  requirement RF09 {
    doc /* F09: O sistema deve analisar pressão e imobilidade e acionar a redistribuição de pressão do colchão. */
  }
  requirement RF10 {
    doc /* F10: O sistema deve localizar a pulseira, detetar saída do perímetro e alertar a equipa. */
  }
  requirement RF11 {
    doc /* F11: O sistema deve comunicar emergências e contexto clínico a um serviço externo e guardar a referência. */
  }
  requirement RF12 {
    doc /* F12: O sistema deve consultar o stock do dispensador e solicitar reposição ao serviço da farmácia. */
  }
  requirement RNF01 {
    doc /* Segurança e privacidade: Cifragem, controlo de acesso, consentimento e minimização de dados. */
  }
  requirement RNF04 {
    doc /* Desempenho em tempo real: Alerta local em ≤ 2 s no percentil 95; registo de medições em ≤ 1 s. */
  }
  requirement RNF03 {
    doc /* Usabilidade e acessibilidade: Interface responsiva, contraste, foco visível e controlos de grande dimensão. */
  }
  requirement RNF02 {
    doc /* Disponibilidade e recuperação: Serviço local de alertas disponível 99,5% e recuperação automática. */
  }
  // Relações: RNF01 «conflict» RNF03 e RNF04; RNF04 «contribute» RNF02 e RNF03.
}