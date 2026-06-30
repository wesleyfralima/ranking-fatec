from dataclasses import dataclass
from enum import StrEnum

# Gabarito oficial completo de 60 questões
# (Questões 1 a 60, alternativas A-E)
GABARITO: dict[int, str] = {
    1: "D",
    2: "C",
    3: "B",
    4: "E",
    5: "E",
    6: "C",
    7: "D",
    8: "B",
    9: "D",
    10: "A",
    11: "E",
    12: "B",
    13: "B",
    14: "A",
    15: "D",
    16: "E",
    17: "B",
    18: "D",
    19: "C",
    20: "A",
    21: "D",
    22: "D",
    23: "B",
    24: "B",
    25: "C",
    26: "B",
    27: "C",
    28: "B",
    29: "C",
    30: "D",
    31: "D",
    32: "E",
    33: "A",
    34: "C",
    35: "E",
    36: "A",
    37: "D",
    38: "C",
    39: "B",
    40: "D",
    41: "E",
    42: "B",
    43: "C",
    44: "D",
    45: "A",
    46: "D",
    47: "D",
    48: "B",
    49: "C",
    50: "A",
    51: "E",
    52: "E",
    53: "A",
    54: "C",
    55: "A",
    56: "C",
    57: "B",
    58: "C",
    59: "B",
    60: "D",
}


class PeriodoEnum(StrEnum):
    MANHA = "Manhã"
    TARDE = "Tarde"
    NOITE = "Noite"
    EAD = "EaD"


@dataclass(frozen=True, slots=True)
class OfertaDTO:
    curso: str
    vagas: int
    nota_corte: float | None
    candidatos_por_vaga: float | None


OfertasEstruturadas = dict[str, dict[PeriodoEnum, list[OfertaDTO]]]

OFERTAS_ESTRUTURADAS: OfertasEstruturadas = {
    "FATEC Adamantina": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Ciência de Dados", 33, None, 1.27),
            OfertaDTO("Gestão Comercial", 30, None, 1.40),
        ]
    },
    "FATEC Americana": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 33, None, 2.85),
            OfertaDTO("Design de Moda", 36, None, 1.22),
            OfertaDTO("Gestão Empresarial", 38, None, 1.08),
            OfertaDTO("Logística", 38, None, 1.18),
            OfertaDTO("Segurança da Informação", 33, None, 1.67),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 33, None, 1.76),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão Empresarial", 31, None, 2.77),
            OfertaDTO("Jogos Digitais", 31, None, 2.10),
            OfertaDTO("Logística", 33, None, 1.55),
            OfertaDTO("Produção Têxtil", 37, None, 1.24),
            OfertaDTO("Segurança da Informação", 30, None, 4.63),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 35, None, 3.66),
        ],
    },
    "FATEC Araçatuba": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 36, None, 1.47),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Biocombustíveis", 37, None, 1.14),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 34, None, 1.53),
        ],
    },
    "FATEC Araraquara": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 30, 74.800, 2.8),
            OfertaDTO("Gestão Empresarial", 34, 52.800, 0.74),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão Comercial", 36, 55.746, 1.17),
            OfertaDTO("Gestão da Produção Industrial", 33, 57.680, 1.52),
            OfertaDTO("Segurança da Informação", 32, 66.294, 3.03),
        ],
    },
    "FATEC Araras": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 34, None, 1.71),
            OfertaDTO("Gestão Empresarial", 32, None, 1.94),
        ]
    },
    "FATEC Assis": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão Comercial", 32, None, 1.56),
            OfertaDTO("Gestão da Tecnologia da Informação", 34, None, 2.29),
        ]
    },
    "FATEC Atibaia": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 32, None, 1.69),
        ]
    },
    "FATEC Baixada Santista": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 32, 76.266, 3.56),
            OfertaDTO("Ciência de Dados", 31, 71.134, 2.0),
            OfertaDTO("Gestão Portuária", 33, 56.500, 1.79),
            OfertaDTO("Logística", 33, 54.000, 1.85),
            OfertaDTO("Sistemas para Internet", 36, 59.514, 1.75),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 30, 78.667, 8.5),
            OfertaDTO("Gestão de Recursos Humanos", 33, 60.866, 2.67),
            OfertaDTO("Gestão Empresarial", 32, 58.666, 1.84),
            OfertaDTO("Gestão Portuária", 31, 66.294, 5.84),
            OfertaDTO("Logística", 31, 64.786, 6.03),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 32, 65.266, 2.88),
        ],
    },
    "FATEC Barretos": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão Hospitalar", 37, None, 1.3),
        ]
    },
    "FATEC Barueri": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Gestão da Tecnologia da Informação", 32, 66.734, 3.25),
            OfertaDTO("Gestão de Eventos", 32, 48.000, 1.19),
            OfertaDTO("Gestão de Negócios e Pessoas", 31, 51.334, 1.58),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Comércio Exterior", 33, 35.406, 1.18),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Comércio Exterior", 32, 69.306, 4.78),
            OfertaDTO("Design de Mídias Digitais", 32, 68.554, 4.75),
            OfertaDTO("Gestão de Comércio Eletrônico", 38, 20.600, 0.92),
            OfertaDTO("Gestão de Recursos Humanos", 33, 65.266, 5.33),
            OfertaDTO("Transporte Terrestre", 40, 47.666, 0.85),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 32, 69.306, 5.31),
        ],
    },
    "FATEC Bauru": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Gestão Hospitalar", 37, None, 1.46),
            OfertaDTO("Redes de Computadores", 31, None, 1.68),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Automação Industrial", 33, None, 2.45),
            OfertaDTO("Banco de Dados", 31, None, 3.35),
            OfertaDTO("Sistemas Biomédicos", 35, None, 1.63),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 33, None, 3.85),
        ],
    },
    "FATEC Bebedouro": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Logística", 32, None, 1.13),
        ]
    },
    "FATEC Botucatu": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 35, None, 1.66),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Agronegócio", 35, None, 1.31),
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 37, None, 3.49),
            OfertaDTO("Logística", 32, None, 1.31),
            OfertaDTO("Produção Industrial", 37, None, 1.92),
            OfertaDTO("Radiologia", 36, None, 1.83),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 34, None, 3.41),
        ],
    },
    "FATEC Bragança Paulista": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 33, None, 1.55),
            OfertaDTO("Gestão Empresarial", 35, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão da Tecnologia da Informação", 38, None, 1.42),
            OfertaDTO("Gestão Financeira", 37, None, 1.27),
            OfertaDTO("Logística", 36, None, 0.86),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 30, None, 2.30),
        ],
    },
    "FATEC Campinas": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 31, None, 4.61),
            OfertaDTO("Gestão Empresarial", 32, None, 1.19),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 31, None, 2.13),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão da Tecnologia da Informação", 31, None, 3.42),
            OfertaDTO("Logística", 31, None, 2.48),
            OfertaDTO("Processos Químicos", 31, None, 2.74),
        ],
    },
    "FATEC Capão Bonito": {
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 32, None, 2.13),
        ]
    },
    "FATEC Carapicuíba": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 31, 70.814, 4.13),
            OfertaDTO("Design de Mídias Digitais", 34, 57.333, 1.35),
            OfertaDTO("Jogos Digitais", 30, 56.466, 0.87),
            OfertaDTO("Logística", 34, None, 1.41),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 31, 73.473, 11.68),
            OfertaDTO("Jogos Digitais", 33, 56.466, 1.33),
            OfertaDTO("Logística", 32, 53.534, 2.72),
            OfertaDTO("Secretariado", 30, 39.600, 1.37),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 31, 62.334, 4.84),
        ],
    },
    "FATEC Catanduva": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Gestão Empresarial", 38, None, 1.32),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Automação Industrial", 31, None, 1.97),
            OfertaDTO("Gestão da Tecnologia da Informação", 31, None, 2.42),
            OfertaDTO("Gestão Empresarial", 32, None, 2.03),
        ],
    },
    "FATEC Cotia": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Comércio Exterior", 32, None, 1.69),
            OfertaDTO(
                "Design de Produto com Ênfase em Processos de Produção e Indust.",
                32,
                30.0,
                0.44,
            ),
            OfertaDTO("Gestão da Produção Industrial", 35, None, 0.69),
            OfertaDTO("Gestão Empresarial", 34, None, 1.26),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Ciência de Dados", 30, None, 4.63),
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 31, None, 3.74),
            OfertaDTO("Gestão da Produção Industrial", 33, None, 1.45),
            OfertaDTO("Gestão Empresarial", 31, None, 3.26),
        ],
    },
    "FATEC Cruzeiro": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 32, None, 2.91),
            OfertaDTO("Gestão Hospitalar", 38, None, 1.32),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão da Produção Industrial", 32, None, 1.91),
            OfertaDTO("Gestão de Eventos", 38, None, 0.84),
        ],
    },
    #
    # Continuar daqui
    #
    "FATEC Diadema": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Cosméticos", 31, None, None),
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 31, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Cosméticos", 33, None, None),
            OfertaDTO("Gestão da Produção Industrial", 31, None, None),
        ],
    },
    "FATEC Ferraz de Vasconcelos": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 30, 72.320, 3.7),
            OfertaDTO("Gestão Empresarial", 35, 44.000, 0.66),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão da Produção Industrial", 36, 42.534, 1.17),
        ],
    },
    "FATEC Franca": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 38, None, None),
            OfertaDTO("Gestão da Produção Industrial", 35, None, None),
            OfertaDTO("Gestão de Recursos Humanos", 36, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 33, None, None),
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 33, None, None),
            OfertaDTO("Gestão da Produção Industrial", 38, None, None),
            OfertaDTO("Gestão de Recursos Humanos", 32, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 35, None, None),
        ],
    },
    "FATEC Franco da Rocha": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 30, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão da Tecnologia da Informação", 31, None, None),
            OfertaDTO("Gestão de Energia e Eficiência Energética", 38, None, None),
        ],
    },
    "FATEC Garça": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 39, None, None),
            OfertaDTO("Gestão Empresarial", 40, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 39, None, None),
            OfertaDTO("Gestão Empresarial", 40, None, None),
            OfertaDTO("Mecatrônica Industrial", 40, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 40, None, None),
        ],
    },
    "FATEC Guaratinguetá": {
        PeriodoEnum.TARDE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 33, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão da Produção Industrial", 33, None, None),
            OfertaDTO("Gestão da Tecnologia da Informação", 32, None, None),
            OfertaDTO("Gestão Empresarial", 31, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 33, None, None),
        ],
    },
    "FATEC Guarulhos": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Comércio Exterior", 33, None, None),
            OfertaDTO("Logística Aeroportuária", 31, None, None),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 30, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão da Produção Industrial", 32, None, None),
            OfertaDTO("Logística", 31, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 30, None, None),
        ],
    },
    "FATEC Ilha Solteira": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 36, None, None),
        ],
    },
    "FATEC Indaiatuba": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 35, 65.266, 1.66),
            OfertaDTO("Gestão de Serviços", 38, 44.734, 1.42),
            OfertaDTO("Logística Aeroportuária", 34, 46.200, 1.53),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Gestão Empresarial", 39, 46.200, 1.44),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 31, 77.333, 6.71),
            OfertaDTO("Comércio Exterior", 33, 70.400, 2.27),
            OfertaDTO("Gestão Empresarial", 31, 46.200, 4.06),
        ],
    },
    "FATEC Itapetininga": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 35, None, None),
            OfertaDTO("Comércio Exterior", 33, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Agronegócio", 35, None, None),
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 36, None, None),
            OfertaDTO("Comércio Exterior", 35, None, None),
            OfertaDTO("Gestão Ambiental", 33, None, None),
            OfertaDTO("Gestão da Produção Industrial", 34, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 36, None, None),
        ],
    },
    "FATEC Itapira": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 35, None, None),
            OfertaDTO("Gestão da Produção Industrial", 37, None, None),
            OfertaDTO("Gestão Empresarial", 38, None, None),
        ],
    },
    "FATEC Itaquaquecetuba": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Gestão Comercial", 34, 52.000, 0.44),
            OfertaDTO("Gestão da Tecnologia da Informação", 32, 58.666, 2.22),
            OfertaDTO("Secretariado", 30, 30.066, 0.33),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Gestão de Comércio Eletrônico", 38, 33.900, 0.08),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão Comercial", 33, 31.640, 1.88),
            OfertaDTO("Secretariado", 31, 21.846, 0.84),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 31, 62.526, 3.9),
        ],
    },
    "FATEC Itatiba": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 36, None, None),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 39, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão da Produção Industrial", 39, None, None),
        ],
    },
    "FATEC Itu": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 37, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão da Tecnologia da Informação", 33, None, None),
            OfertaDTO("Gestão Empresarial", 35, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 40, None, None),
        ],
    },
    "FATEC Jaboticabal": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Biocombustíveis", 39, None, None),
            OfertaDTO("Marketing", 35, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Biocombustíveis", 37, None, None),
            OfertaDTO("Gestão Ambiental", 38, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 35, None, None),
        ],
    },
    "FATEC Jacareí": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 32, None, None),
            OfertaDTO("Geoprocessamento", 37, None, None),
            OfertaDTO("Meio Ambiente e Recursos Hídricos", 40, None, None),
        ]
    },
    "FATEC Jales": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 36, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Agronegócio", 37, None, None),
            OfertaDTO("Gestão Empresarial", 39, None, None),
            OfertaDTO("Sistemas para Internet", 37, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 35, None, None),
        ],
    },
    "FATEC Jahu": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Construção Naval", 37, None, None),
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 33, None, None),
            OfertaDTO("Sistemas de Navegação Fluvial", 40, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão da Produção Industrial", 37, None, None),
            OfertaDTO("Gestão da Tecnologia da Informação", 35, None, None),
            OfertaDTO("Logística", 35, None, None),
            OfertaDTO("Meio Ambiente e Recursos Hídricos", 37, None, None),
        ],
    },
    "FATEC Jundiaí": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Gestão de Eventos", 34, None, None),
            OfertaDTO("Gestão de Logística Integrada", 34, None, None),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 32, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Ciência de Dados", 31, None, None),
            OfertaDTO("Defesa Cibernética", 32, None, None),
            OfertaDTO("Gestão Ambiental", 31, None, None),
            OfertaDTO("Gestão da Tecnologia da Informação", 34, None, None),
            OfertaDTO("Gestão de Logística Integrada", 34, None, None),
            OfertaDTO("Sistemas Embarcados", 38, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 30, None, None),
        ],
    },
    "FATEC Lins": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 36, None, None),
            OfertaDTO("Gestão da Qualidade", 40, None, None),
            OfertaDTO("Logística", 39, None, None),
        ]
    },
    "FATEC Marília": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Alimentos", 39, None, None),
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 37, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Alimentos", 40, None, None),
            OfertaDTO("Gestão Comercial", 39, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 39, None, None),
        ],
    },
    "FATEC Matão": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 37, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise de Processos Agroindustriais", 32, None, None),
        ],
    },
    "FATEC Mauá": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Fabricação Mecânica", 36, None, None),
            OfertaDTO("Informática para Negócios", 37, None, None),
            OfertaDTO("Logística", 35, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 32, None, None),
            OfertaDTO("Fabricação Mecânica", 38, None, None),
            OfertaDTO("Informática para Negócios", 33, None, None),
            OfertaDTO("Logística", 32, None, None),
            OfertaDTO("Polímeros", 36, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 32, None, None),
        ],
    },
    "FATEC Mococa": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Agronegócio", 39, None, None),
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 37, None, None),
            OfertaDTO("Gestão de Recursos Humanos", 39, None, None),
            OfertaDTO("Gestão Empresarial", 36, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 39, None, None),
        ],
    },
    "FATEC Mogi das Cruzes": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Gestão de Recursos Humanos", 34, 55.000, 1.76),
            OfertaDTO("Logística", 35, 53.486, 1.57),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Agronegócio", 35, 40.680, 0.14),
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 33, 76.086, 3.09),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Agronegócio", 36, 55.000, 1.94),
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 31, 80.666, 9.77),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 31, 66.000, 5.06),
        ],
    },
    "FATEC Mogi Mirim": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 31, 65.333, 1.71),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 32, 74.066, 5.16),
            OfertaDTO("Projetos Mecânicos", 38, 49.866, 2.13),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 34, 61.600, 3.59),
        ],
    },
    "FATEC Olímpia": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 35, None, None),
            OfertaDTO("Gestão de Turismo", 38, None, None),
        ]
    },
    "FATEC Osasco": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Automação Industrial", 32, None, None),
            OfertaDTO("Manutenção Industrial", 39, None, None),
            OfertaDTO("Sistemas Biomédicos", 34, None, None),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Gestão Financeira", 34, None, None),
            OfertaDTO("Redes de Computadores", 35, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Automação Industrial", 31, None, None),
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 30, None, None),
            OfertaDTO("Gestão Financeira", 32, None, None),
            OfertaDTO("Manutenção Industrial", 33, None, None),
            OfertaDTO("Redes de Computadores", 32, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 30, None, None),
        ],
    },
    "FATEC Ourinhos": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Agronegócio", 38, None, None),
            OfertaDTO("Jogos Digitais", 40, None, None),
            OfertaDTO("Segurança da Informação", 38, None, None),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 38, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Agronegócio", 37, None, None),
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 35, None, None),
            OfertaDTO("Ciência de Dados", 37, None, None),
            OfertaDTO("Segurança da Informação", 37, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 35, None, None),
        ],
    },
    "FATEC Pindamonhangaba": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Manutenção Industrial", 37, None, None),
            OfertaDTO("Processos Metalúrgicos", 39, None, None),
            OfertaDTO("Projetos Mecânicos", 35, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 31, None, None),
        ],
    },
    "FATEC Piracicaba": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Alimentos", 36, None, None),
            OfertaDTO("Gestão Empresarial", 32, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Biocombustíveis", 34, None, None),
            OfertaDTO("Gestão Empresarial", 31, None, None),
        ],
    },
    "FATEC Pompéia": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Mecanização em Agricultura de Precisão", 38, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Mecanização em Agricultura de Precisão", 38, None, None),
            OfertaDTO("Sistemas Inteligentes", 36, None, None),
        ],
    },
    "FATEC Porto Ferreira": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 37, None, None),
        ]
    },
    "FATEC Praia Grande": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Comércio Exterior", 31, 59.333, 2.23),
            OfertaDTO("Gestão Empresarial", 33, 48.966, 1.00),
            OfertaDTO("Processos Químicos", 37, 48.000, 1.08),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 32, 64.786, 3),
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 32, 64.034, 1.66),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 31, 75.534, 8.61),
            OfertaDTO("Comércio Exterior", 32, 64.534, 4.38),
            OfertaDTO("Gestão Empresarial", 33, 52.800, 1.76),
            OfertaDTO("Processos Químicos", 38, 48.966, 1.32),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 31, 63.800, 4.42),
        ],
    },
    "FATEC Presidente Prudente": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 32, None, None),
            OfertaDTO("Marketing", 36, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 34, None, None),
            OfertaDTO("Gestão Empresarial", 35, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 33, None, None),
        ],
    },
    "FATEC Registro": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 25, None, None),
            OfertaDTO("Gestão Empresarial", 25, None, None),
        ]
    },
    "FATEC Ribeirão Preto": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 32, None, None),
            OfertaDTO("Gestão de Recursos Humanos", 35, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 31, None, None),
            OfertaDTO("Gestão de Negócios e Inovação", 34, None, None),
            OfertaDTO("Sistemas Biomédicos", 34, None, None),
        ],
    },
    "FATEC Rio Claro": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Inteligência Artificial", 28, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO(
                "Gestão da Sustentabilidade Ambiental, Social e Governança Corporativa",
                28,
                30.0,
                1.0,
            ),
        ],
    },
    "FATEC Santana de Parnaíba": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 33, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Ciência de Dados", 31, None, None),
            OfertaDTO("Gestão Comercial", 36, None, None),
            OfertaDTO("Segurança da Informação", 31, None, None),
        ],
    },
    "FATEC Santo André": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Mecânica Automobilística", 33, 52.734, 1.36),
            OfertaDTO("Mecatrônica Industrial", 34, 66.000, 2.18),
            OfertaDTO("Sistemas Embarcados", 35, 46.706, 0.83),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Eletrônica Automotiva", 30, 61.333, 3.37),
            OfertaDTO("Mecânica Automobilística", 32, 65.333, 4.5),
        ],
    },
    "FATEC São Bernardo do Campo": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Automação Industrial", 31, None, None),
            OfertaDTO("Informática para Negócios", 30, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Automação Industrial", 32, None, None),
            OfertaDTO("Informática para Negócios", 32, None, None),
            OfertaDTO("Manufatura Avançada", 33, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 34, None, None),
        ],
    },
    "FATEC São Caetano do Sul": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 31, 78.466, 4.77),
            OfertaDTO("Segurança da Informação", 31, 68.934, 1.87),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 31, 68.000, 1.9),
            OfertaDTO("Comércio Exterior", 33, 61.333, 1.06),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Jogos Digitais", 31, 69.333, 2.35),
            OfertaDTO("Segurança da Informação", 31, 72.667, 5.61),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 33, 63.066, 2.88),
        ],
    },
    "FATEC São Carlos": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Big Data para Indústria", 34, None, None),
            OfertaDTO("Gestão da Produção Industrial", 33, None, None),
            OfertaDTO("Gestão de Recursos Humanos", 34, None, None),
            OfertaDTO("Gestão Empresarial", 33, None, None),
        ],
    },
    "FATEC São José do Rio Preto": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Agronegócio", 32, 44.446, 1.00),
            OfertaDTO("Informática para Negócios", 31, 56.000, 1.35),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 34, 81.713, 3.68),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Agronegócio", 34, 47.666, 1.41),
            OfertaDTO("Gestão de Negócios e Inovação", 31, None, 1.84),
            OfertaDTO("Informática para Negócios", 31, 69.666, 3.03),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 32, 68.000, 4.22),
        ],
    },
    "FATEC São José dos Campos": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 35, 79.934, 5.06),
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 30, 73.473, 2.4),
            OfertaDTO("Logística", 31, 56.466, 1.58),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Banco de Dados", 30, 74.847, 4.40),
            OfertaDTO("Gestão da Produção Industrial", 32, 60.866, 1.91),
            OfertaDTO("Logística", 33, 59.514, 2.12),
            OfertaDTO("Manutenção de Aeronaves", 34, 71.566, 2.91),
            OfertaDTO("Projetos de Estruturas Aeronáuticas", 31, 65.266, 2.23),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 35, 68.200, 3.94),
        ],
    },
    "FATEC Ipiranga": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Big Data para Negócios", 38, 66.000, 1.05),
            OfertaDTO("Gestão Comercial", 36, 33.146, 0.39),
            OfertaDTO("Gestão de Eventos", 35, 48.067, 0.57),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 33, 66.734, 1.73),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 33, 74.800, 7.48),
            OfertaDTO("Gestão Comercial", 34, 60.134, 1.74),
            OfertaDTO("Gestão de Recursos Humanos", 35, 61.600, 2.8),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 35, 63.280, 3.09),
        ],
    },
    "FATEC Itaquera": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Manutenção Industrial", 35, None, None),
            OfertaDTO("Refrigeração, Ventilação e Ar Condicionado", 38, None, None),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Automação Industrial", 32, None, None),
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 30, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Automação Industrial", 32, None, None),
            OfertaDTO("Fabricação Mecânica", 35, None, None),
            OfertaDTO("Mecânica - Processos de Soldagem", 38, None, None),
            OfertaDTO("Refrigeração, Ventilação e Ar Condicionado", 38, None, None),
        ],
    },
    #
    # Feito
    #
    "FATEC São Paulo": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 34, 84.000, 10.0),
            OfertaDTO("Construção Civil - Edifícios", 35, 60.134, 1.86),
            OfertaDTO("Gestão da Produção Industrial", 33, 55.000, 1.76),
            OfertaDTO("Gestão de Turismo", 35, 59.514, 1.14),
            OfertaDTO("Instalações Elétricas", 30, 58.000, 2.60),
            OfertaDTO("Materiais", 40, None, 0.68),
            OfertaDTO("Microeletrônica", 36, 63.800, 1.64),
            OfertaDTO("Produção Cultural", 31, 71.134, 4.65),
            OfertaDTO("Projetos Mecânicos", 38, 49.333, 1.08),
            OfertaDTO("Refrigeração e Climatização", 37, 47.460, 0.78),
            OfertaDTO("Secretariado e Assessoria Internacional", 34, 67.333, 2.03),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 31, 75.333, 3.74),
            OfertaDTO("Gestão de Empreendimentos Gastronômicos", 37, 33.000, 1.14),
            OfertaDTO("Gestão de Turismo", 33, 27.333, 1.12),
            OfertaDTO("Paisagismo e Jardinagem", 35, 53.486, 1.66),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 70, 80.606, 13.81),
            OfertaDTO("Construção Civil - Edifícios", 52, 55.333, 3.94),
            OfertaDTO("Eletrônica Industrial", 32, 71.866, 4.84),
            OfertaDTO("Estradas", 40, 55.333, 0.98),
            OfertaDTO("Fabricação Mecânica", 31, 58.006, 1.87),
            OfertaDTO("Gestão da Qualidade", 32, 64.786, 3.88),
            OfertaDTO("Hidráulica e Saneamento Ambiental", 37, 55.333, 1.95),
            OfertaDTO("Projetos Mecânicos", 37, 65.333, 2.89),
            OfertaDTO("Secretariado e Assessoria Internacional", 30, 65.540, 4.03),
            OfertaDTO("Soldagem", 36, 59.400, 2.0),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 30, 73.826, 10.33),
        ],
    },
    "FATEC Sebrae": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Gestão de Negócios e Inovação", 26, 58.006, 1.54),
            OfertaDTO("Marketing", 26, 69.306, 4.15),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Ciência de Dados para Negócios", 26, 70.667, 2.31),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão de Negócios e Inovação", 26, 65.540, 3.65),
            OfertaDTO("Marketing", 26, 73.826, 8.73),
        ],
    },
    "FATEC Tatuapé": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Controle de Obras", 36, None, None),
            OfertaDTO(
                "Design de Produto com Ênfase em Processos de Produção e Indust.",
                30,
                30.0,
                1.0,
            ),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Construção de Edifícios", 35, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Construção de Edifícios", 34, None, None),
            OfertaDTO("Controle de Obras", 36, None, None),
            OfertaDTO("Transporte Terrestre", 39, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 30, None, None),
        ],
    },
    "FATEC Zona Leste": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Comércio Exterior", 33, 64.000, 1.45),
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 30, 72.600, 2.27),
            OfertaDTO("Gestão de Recursos Humanos", 33, 60.667, 2.0),
            OfertaDTO("Gestão Empresarial", 31, 63.066, 1.39),
            OfertaDTO("Logística", 31, 50.474, 1.32),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 31, 72.000, 2.74),
            OfertaDTO("Comércio Exterior", 34, 53.333, 1.15),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 30, 79.934, 14.13),
            OfertaDTO("Logística", 30, 62.334, 3.47),
            OfertaDTO("Polímeros", 39, 42.186, 1.18),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 33, 65.920, 4.85),
        ],
    },
    "FATEC Zona Sul": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 32, None, None),
            OfertaDTO("Gestão Empresarial", 37, None, None),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 31, None, None),
            OfertaDTO("Gestão Empresarial", 35, None, None),
            OfertaDTO("Logística", 38, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 30, None, None),
            OfertaDTO("Logística", 32, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 32, None, None),
        ],
    },
    "FATEC São Roque": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Gestão de Empreendimentos Gastronômicos", 27, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão Comercial", 24, None, None),
            OfertaDTO("Gestão de Turismo", 25, None, None),
            OfertaDTO("Sistemas para Internet", 23, None, None),
        ],
    },
    "FATEC São Sebastião": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 34, None, None),
            OfertaDTO("Gestão Empresarial", 37, None, None),
            OfertaDTO("Marketing", 34, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 34, None, None),
        ],
    },
    "FATEC Sertãozinho": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Gestão Empresarial", 33, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão da Produção Industrial", 33, None, None),
            OfertaDTO("Gestão Empresarial", 33, None, None),
            OfertaDTO("Manutenção Industrial", 36, None, None),
            OfertaDTO("Mecânica - Processos de Soldagem", 40, None, None),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 32, None, None),
        ],
    },
    "FATEC Sorocaba": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 33, 77.333, 3.73),
            OfertaDTO("Fabricação Mecânica", 34, 38.866, 0.88),
            OfertaDTO("Gestão da Qualidade", 33, 54.933, 1.24),
            OfertaDTO("Manutenção de Aeronaves", 32, 65.266, 1.84),
            OfertaDTO("Processos Metalúrgicos", 39, 42.534, 1.15),
            OfertaDTO("Projetos Mecânicos", 39, 46.706, 0.74),
            OfertaDTO("Sistemas Biomédicos", 36, 57.254, 0.81),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Logística", 34, 50.474, 0.74),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 32, 77.734, 7.84),
            OfertaDTO("Eletrônica Automotiva", 33, 63.066, 2.09),
            OfertaDTO("Fabricação Mecânica", 77, 52.800, 1.61),
            OfertaDTO("Polímeros", 36, 47.460, 0.86),
            OfertaDTO("Projetos Mecânicos", 37, 70.400, 2.62),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 33, 70.060, 5.21),
        ],
    },
    "FATEC Sumaré": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Gestão de Logística Integrada", 31, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão de Negócios e Inovação", 30, None, None),
            OfertaDTO("Gestão de Recursos Humanos", 34, None, None),
        ],
    },
    "FATEC Suzano": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Gestão da Produção Industrial", 34, 60.866, 2.85),
            OfertaDTO("Redes de Computadores", 32, 66.000, 3.03),
        ],
    },
    "FATEC Taquaritinga": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Gestão da Produção Industrial", 39, 34.667, 1.41),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Agronegócio", 39, 28.600, 1.36),
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 39, 54.240, 1.46),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Agronegócio", 36, 49.134, 1.47),
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 30, 71.866, 4.2),
            OfertaDTO("Gestão da Produção Industrial", 38, 43.266, 1.34),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 39, 53.534, 1.72),
        ],
    },
    "FATEC Tatuí": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Automação Industrial", 39, None, None),
            OfertaDTO("Gestão da Tecnologia da Informação", 36, None, None),
            OfertaDTO("Manutenção Industrial", 39, None, None),
        ],
        PeriodoEnum.TARDE: [
            OfertaDTO("Gestão Empresarial", 39, None, None),
            OfertaDTO("Produção Fonográfica", 38, None, None),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Automação Industrial", 36, None, None),
            OfertaDTO("Gestão da Tecnologia da Informação", 38, None, None),
            OfertaDTO("Gestão Empresarial", 31, None, None),
            OfertaDTO("Manutenção Industrial", 39, None, None),
        ],
    },
    "FATEC Taubaté": {
        PeriodoEnum.MANHA: [
            OfertaDTO("Gestão de Recursos Humanos", 32, 48.400, 1.59),
        ],
        PeriodoEnum.NOITE: [
            OfertaDTO("Análise e Desenvolvimento de Sistemas (ADS)", 32, 74.800, 4.88),
            OfertaDTO("Eletrônica Automotiva", 34, 58.000, 1.68),
        ],
        PeriodoEnum.EAD: [
            OfertaDTO("Gestão Empresarial", 31, 65.266, 2.94),
        ],
    },
    "FATEC Votorantim": {
        PeriodoEnum.NOITE: [
            OfertaDTO("Ciência de Dados para Negócios", 33, None, None),
            OfertaDTO("Controle de Obras", 33, None, None),
            OfertaDTO("Desenvolvimento de Software Multiplataforma", 29, None, None),
        ],
    },
}


# Inicializa a lista plana esperada pelo backend para persistência de dados
DADOS_OFERTAS_INICIAIS: list[tuple[str, PeriodoEnum, str, int, float, float]] = []

for campus, periodos in OFERTAS_ESTRUTURADAS.items():
    for periodo, ofertas in periodos.items():
        for dto in ofertas:
            curso = dto.curso
            vagas = dto.vagas
            corte = dto.nota_corte
            cv = dto.candidatos_por_vaga
            DADOS_OFERTAS_INICIAIS.append((campus, periodo, curso, vagas, corte, cv))
