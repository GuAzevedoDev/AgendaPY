// Perguntas da Ficha de Anamnese — Estética Facial (Mali Azevedo Studio de Beleza).
// SECOES_CLIENTE: respondidas pelo cliente no formulario publico (anamnese_form.js).
// SECOES_PROFISSIONAL: preenchidas so pela equipe, no modal do dashboard (anamnese_ui.js).
// SECOES_ANAMNESE: as duas juntas, usada no modal para exibir/editar a ficha completa.

export const SECOES_CLIENTE = [
  {
    id: "dados_pessoais",
    titulo: "Dados pessoais",
    perguntas: [
      { id: "ocupacao", label: "Ocupação", tipo: "texto", obrigatorio: true },
      { id: "data_nascimento", label: "Data de nascimento (DD/MM/AAAA)", tipo: "texto", obrigatorio: true },
      { id: "endereco", label: "Endereço", tipo: "texto", obrigatorio: true },
      { id: "rg", label: "RG", tipo: "texto", obrigatorio: true },
      { id: "cpf", label: "CPF", tipo: "texto", obrigatorio: true },
    ],
  },
  {
    id: "historico_saude",
    titulo: "Histórico de saúde",
    perguntas: [
      { id: "lentes_contato", label: "Utiliza lentes de contato?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "tabagismo", label: "Tabagismo?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "epilepsia_convulsoes", label: "Tem epilepsia / convulsões?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "alteracoes_cardiacas", label: "Possui alterações cardíacas?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "intestino_regular", label: "Funcionamento intestinal regular?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "marcapasso", label: "É portador de marcapasso?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "tratamento_facial_anterior", label: "Já fez tratamento facial anteriormente?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "tratamento_facial_especifique", label: "Se sim, especifique", tipo: "texto", dependeDe: "tratamento_facial_anterior", obrigatorio: true },
      { id: "ja_fez_botox", label: "Já fez botox?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "ja_fez_botox_tempo", label: "Se sim, ha quanto tempo?", tipo: "texto",dependeDe: "ja_fez_botox", obrigatorio: true },
      { id: "gestante", label: "Está gestante?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "gestante_semanas", label: "Se sim, quantas semanas?", tipo: "texto", dependeDe: "gestante", obrigatorio: true },
      { id: "alergia", label: "Possui algum tipo de alergia?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "alergia_especifique", label: "Se sim, especifique a alergia", tipo: "texto", dependeDe: "alergia", obrigatorio: true },
      { id: "problema_saude", label: "Possui algum problema de saúde?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "problema_saude_qual", label: "Qual?", tipo: "texto", dependeDe: "problema_saude", obrigatorio: true },
      { id: "protese", label: "Possui prótese corporal/facial?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "protese_especifique", label: "Se sim, especifique", tipo: "texto", dependeDe: "protese", obrigatorio: true },
      { id: "problemas_pele", label: "Possui problemas de pele?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "problemas_pele_especifique", label: "Se sim, relate", tipo: "texto", dependeDe: "problemas_pele", obrigatorio: true },
    ],
  },
  {
    id: "habitos_rotina",
    titulo: "Hábitos e rotina",
    perguntas: [
      { id: "agua_frequencia", label: "Ingere água com frequência?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "agua_especifique", label: "Especifique (quantidade aproximada)", tipo: "texto", dependeDe: "agua_frequencia", obrigatorio: true },
      { id: "cremes_locoes_facial", label: "Usa cremes ou loções faciais?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "cremes_especifique", label: "Quais?", tipo: "texto", dependeDe: "cremes_locoes_facial", obrigatorio: true },
      { id: "bebida_alcoolica", label: "Ingere bebida alcoólica?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "alcool_especifique", label: "Com que frequência?", tipo: "texto", dependeDe: "bebida_alcoolica", obrigatorio: true },
      { id: "atividade_fisica", label: "Pratica atividade física?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "atividade_especifique", label: "Qual e com que frequência?", tipo: "texto", dependeDe: "atividade_fisica", obrigatorio: true },
      { id: "exposicao_sol", label: "Tem exposição ao sol?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "exposicao_frequencia", label: "Com que frequência?", tipo: "texto", dependeDe: "exposicao_sol", obrigatorio: true },
      { id: "usa_filtro_solar", label: "Usa protetor solar?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "filtro_solar_qual", label: "Qual e qual fator?", tipo: "texto", dependeDe: "usa_filtro_solar", obrigatorio: true },
      { id: "anticoncepcional", label: "Utiliza anticoncepcional?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "anticoncepcional_qual", label: "Qual?", tipo: "texto", dependeDe: "anticoncepcional", obrigatorio: true },
      { id: "periodo_menstrual", label: "Está no período menstrual?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "data_menstruacao", label: "Data da última menstruação", tipo: "texto", dependeDe: "periodo_menstrual", obrigatorio: true },
      { id: "boa_qualidade_sono", label: "Tem boa qualidade de sono?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "horas_sono", label: "Quantas horas por noite?", tipo: "texto", dependeDe: "boa_qualidade_sono", obrigatorio: true },
      { id: "boa_alimentacao", label: "Possui uma boa alimentação?", tipo: "radio", opcoes: ["Sim", "Não"], obrigatorio: true },
      { id: "alimentacao_especifique", label: "Especifique", tipo: "texto", dependeDe: "boa_alimentacao", obrigatorio: true },
    ],
  },
  {
    id: "declaracao",
    titulo: "Declaração",
    perguntas: [
      {
        id: "declaracao_veracidade",
        label:
          "Declaro que as informações acima são verdadeiras, não cabendo à profissional quaisquer responsabilidades por informações omitidas nessa avaliação.",
        tipo: "confirmacao",
        obrigatorio: true,
      },
    ],
  },
];

export const SECOES_PROFISSIONAL = [
  {
    id: "avaliacao_clinica_pele",
    titulo: "Avaliação clínica da pele",
    perguntas: [
      { id: "oleosidade", label: "Oleosidade", tipo: "radio", opcoes: ["Alípica", "Lipídica", "Normal", "Seborreica"] },
      { id: "acne_grau", label: "Grau de acne", tipo: "radio", opcoes: ["I", "II", "III", "IV"] },
      { id: "espessura", label: "Espessura", tipo: "radio", opcoes: ["Espessa", "Fina", "Muito Fina"] },
      { id: "hidratacao", label: "Hidratação", tipo: "radio", opcoes: ["Desidratada", "Normal"] },
      { id: "fototipo", label: "Fototipo", tipo: "radio", opcoes: ["I", "II", "III", "IV", "V", "VI"] },
      { id: "outros", label: "Outros", tipo: "texto" },
      {
        id: "caracteristicas_pele",
        label: "Características observadas",
        tipo: "checkbox",
        opcoes: [
          "Millium", "Hipertricose", "Foliculite", "Quelóide", "Papiloma", "Nódulos",
          "Comedão", "Ptose", "Queratose", "Tumor", "Efélides", "Víbices",
          "Pápula", "Rugas", "Cicatriz", "Nevo Vascular", "Bolhas", "Telangiectasia",
          "Pústula", "Acromia", "Atrofia", "Nevo Melanócito", "Abcessos", "Hipocromia",
          "Cistos", "Hipercromia", "Xantelasma", "Verruga Plana", "Hirsutismo",
        ],
      },
    ],
  },
  {
    id: "plano_tratamento",
    titulo: "Plano de tratamento",
    perguntas: [{ id: "plano", label: "Plano de tratamento", tipo: "textarea" }],
  },
];

export const SECOES_ANAMNESE = [...SECOES_CLIENTE, ...SECOES_PROFISSIONAL];
