# lógica del juego
# clases y funciones

import math
import random


class Pregunta:
    """Representa una pregunta con opciones, respuesta y pista."""

    def __init__(self, texto, opciones, correcta, pista):
        self.texto = texto
        self.opciones = opciones      
        self.correcta = correcta
        self.pista = pista

    def verificar(self, respuesta):
        """Retorna True si la respuesta es correcta."""
        return respuesta.strip().lower() == self.correcta.strip().lower()

    def opciones_mezcladas(self):
        """Retorna las opciones en orden aleatorio."""
        copia = self.opciones[:]
        random.shuffle(copia)
        return copia



class Monstruo:
    """Representa el monstruo de cada nivel."""

    def __init__(self, nombre, emoji, descripcion, nivel):
        self.nombre = nombre
        self.emoji = emoji
        self.descripcion = descripcion
        self.nivel = nivel



class Jugador:
    """Representa al jugador con nombre, vidas y puntaje."""

    VIDAS_INICIALES = 3

    def __init__(self, nombre):
        self.nombre = nombre
        self.vidas = Jugador.VIDAS_INICIALES
        self.puntaje = 0
        self.nivel_actual = 1
        self.escudos = 1      

    def perder_vida(self):
        self.vidas -= 1

    def ganar_puntos(self, cantidad):
        self.puntaje += cantidad

    def esta_vivo(self):
        return self.vidas > 0

    def subir_nivel(self):
        self.nivel_actual += 1
        self.escudos = 1       

    def usar_escudo(self):
        """Usa el escudo de agua (pista). Retorna True si pudo usarlo."""
        if self.escudos > 0:
            self.escudos -= 1
            return True
        return False

    def porcentaje_avance(self, total_niveles=10):
        """Calcula el porcentaje de avance usando math.floor."""
        return math.floor((self.nivel_actual / total_niveles) * 100)

    def rango(self):
        """Retorna el rango del jugador según su puntaje."""
        if self.puntaje >= 900:
            return "🔥 Maestro del Volcán"
        elif self.puntaje >= 600:
            return "⚔️ Guerrero de las Llamas"
        elif self.puntaje >= 300:
            return "🛡️ Aprendiz Valiente"
        else:
            return "🌱 Novato"



class Juego:
    """Controla el flujo completo del juego."""

    TOTAL_NIVELES = 10
    PREGUNTAS_POR_NIVEL = 3
    MINIMO_PARA_PASAR = 2        

    def __init__(self, jugador):
        self.jugador = jugador
        self.banco = BancoPreguntas()
        self.monstruos = self.banco.obtener_monstruos()
        self.preguntas_nivel = []
        self.indice_pregunta = 0
        self.correctas_nivel = 0
        self.cargar_nivel()

    def cargar_nivel(self):
        """Carga las preguntas y monstruo del nivel actual."""
        nivel = self.jugador.nivel_actual
        todas = self.banco.obtener_preguntas_nivel(nivel)
        random.shuffle(todas)
        self.preguntas_nivel = todas[:self.PREGUNTAS_POR_NIVEL]
        self.indice_pregunta = 0
        self.correctas_nivel = 0
        self.jugador.escudos = 1

    def pregunta_actual(self):
        if self.indice_pregunta < len(self.preguntas_nivel):
            return self.preguntas_nivel[self.indice_pregunta]
        return None

    def monstruo_actual(self):
        nivel = self.jugador.nivel_actual
        
        if nivel <= len(self.monstruos):
            return self.monstruos[nivel - 1]
        return self.monstruos[-1]

    def responder(self, opcion):
        """Procesa la respuesta. Retorna True si es correcta."""
        pregunta = self.pregunta_actual()
        if pregunta is None:
            return False
        es_correcta = pregunta.verificar(opcion)
        if es_correcta:
            self.correctas_nivel += 1
            
            bonus = math.ceil(self.jugador.nivel_actual * 1.5)
            self.jugador.ganar_puntos(10 + bonus)
        else:
            self.jugador.perder_vida()
        self.indice_pregunta += 1
        return es_correcta

    def nivel_superado(self):
        """Retorna True si el jugador pasó el nivel (mínimo 2/3)."""
        return self.correctas_nivel >= self.MINIMO_PARA_PASAR

    def avanzar_nivel(self):
        """Sube de nivel y carga nuevas preguntas."""
        self.jugador.subir_nivel()
        if not self.juego_ganado():
            self.cargar_nivel()

    def juego_ganado(self):
        return self.jugador.nivel_actual > self.TOTAL_NIVELES

    def juego_perdido(self):
        return not self.jugador.esta_vivo()

    def preguntas_restantes(self):
        return self.PREGUNTAS_POR_NIVEL - self.indice_pregunta

    def resumen(self):
        """Retorna diccionario con el resumen final."""
        return {
            "nombre":   self.jugador.nombre,
            "puntaje":  self.jugador.puntaje,
            "nivel":    self.jugador.nivel_actual,
            "vidas":    self.jugador.vidas,
            "rango":    self.jugador.rango(),
            "avance":   self.jugador.porcentaje_avance(),
        }



class BancoPreguntas:
    """Contiene todas las preguntas y monstruos del juego."""

    def __init__(self):
        # Diccionario: nivel → lista de preguntas
        self._preguntas = self._cargar_todas()
        self._monstruos = self._cargar_monstruos()

    def obtener_preguntas_nivel(self, nivel):
        return self._preguntas.get(nivel, [])

    def obtener_monstruos(self):
        return self._monstruos

    def _cargar_monstruos(self):
        """Lista de monstruos uno por nivel."""
        datos = [
            ("Elfo del Balón",       "🧌", "Un elfo obsesionado con el fútbol",          1),
            ("Fantasma Histórico",   "👻", "Un espíritu del pasado lleno de secretos",      2),
            ("Serpiente del Mapa",   "🐍", "Una serpiente que conoce cada rincón del mundo",3),
            ("Científico Mutante",   "🧪", "Una criatura nacida de un experimento fallido",  4),
            ("Titan Cultural",       "👺😴","Un titan dormido que conoce de cultura general", 5),
            ("Demonio Matemático",   "😈", "Un demonio que come números y ecuaciones",       6),
            ("Banshee Musical",      "🎵", "Un fantasma que llora canciones malditas",       7),
            ("Bestia Salvaje",       "🦁", "Una fiera guardiana de la naturaleza",           8),
            ("Profesor Coder",       "💻", "Un profesor que es muy exigente en Python básico",  9),
            ("Dragón del Código",    "🐲", "El dragón final, maestro supremo de Python",    10),
        ]
        
        lista = []
        for nombre, emoji, desc, nivel in datos:
            lista.append(Monstruo(nombre, emoji, desc, nivel))
        return lista

    def _cargar_todas(self):
        """
        Crea el diccionario completo de preguntas por nivel.
        Cada pregunta es un objeto Pregunta.
        """
        datos = {
            
            1: [
                Pregunta(
                    "¿Quién es el máximo goleador en la historia de los Mundiales?",
                    ["Ronaldo", "Miroslav Klose", "Pelé", "Messi"],
                    "Miroslav Klose",
                    "💧 Pista: Es un jugador alemán con 16 goles en mundiales."
                ),
                Pregunta(
                    "¿Qué selección ha ganado más Copas del Mundo?",
                    ["Alemania", "Argentina", "Brasil", "Italia"],
                    "Brasil",
                    "💧 Pista: Es un país de América del Sur conocido por el samba."
                ),
                Pregunta(
                    "¿En qué año se jugó el primer Mundial de Fútbol?",
                    ["1928", "1930", "1934", "1922"],
                    "1930",
                    "💧 Pista: Fue en Uruguay, en la década de los 30."
                ),
                Pregunta(
                    "¿Cuántos jugadores tiene un equipo de fútbol en el campo?",
                    ["10", "12", "11", "9"],
                    "11",
                    "💧 Pista: Es un número entre 10 y 12."
                ),
                Pregunta(
                    "¿Qué país ganó el Mundial de 2022 en Qatar?",
                    ["Francia", "Brasil", "Argentina", "Alemania"],
                    "Argentina",
                    "💧 Pista: Messi finalmente levantó la copa."
                ),
            ],
            
            2: [
                Pregunta(
                    "¿En qué año llegó Cristóbal Colón a América?",
                    ["1490", "1492", "1500", "1488"],
                    "1492",
                    "💧 Pista: Termina en 92, año muy famoso en la historia."
                ),
                Pregunta(
                    "¿Quién fue el primer presidente de Estados Unidos?",
                    ["Abraham Lincoln", "George Washington", "Thomas Jefferson", "John Adams"],
                    "George Washington",
                    "💧 Pista: Su cara aparece en el billete de un dólar."
                ),
                Pregunta(
                    "¿En qué país se construyeron las pirámides de Egipto?",
                    ["Irak", "Sudán", "Egipto", "Libia"],
                    "Egipto",
                    "💧 Pista: El río Nilo pasa por ese país."
                ),
                Pregunta(
                    "¿Cómo se llamaba el Imperio que dominó Europa por siglos desde Roma?",
                    ["Imperio Otomano", "Imperio Romano", "Imperio Griego", "Imperio Persa"],
                    "Imperio Romano",
                    "💧 Pista: Su capital era Roma y sus soldados se llamaban legionarios."
                ),
                Pregunta(
                    "¿En qué año cayó el Muro de Berlín?",
                    ["1985", "1991", "1989", "1987"],
                    "1989",
                    "💧 Pista: Fue en la década de los 80, casi llegando a los 90."
                ),
            ],
            
            3: [
                Pregunta(
                    "¿Cuál es el río más largo del mundo?",
                    ["Amazonas", "Nilo", "Yangtsé", "Misisipi"],
                    "Nilo",
                    "💧 Pista: Está en África y pasa por Egipto."
                ),
                Pregunta(
                    "¿Cuál es el país más grande del mundo?",
                    ["China", "Canadá", "Estados Unidos", "Rusia"],
                    "Rusia",
                    "💧 Pista: Está en Europa y Asia a la vez."
                ),
                Pregunta(
                    "¿Cuál es la capital de Francia?",
                    ["Lyon", "Marsella", "París", "Burdeos"],
                    "París",
                    "💧 Pista: Tiene una famosa torre de hierro."
                ),
                Pregunta(
                    "¿En qué continente está Brasil?",
                    ["África", "Europa", "América del Sur", "América del Norte"],
                    "América del Sur",
                    "💧 Pista: Es el continente debajo de América del Norte."
                ),
                Pregunta(
                    "¿Cuál es el océano más grande del mundo?",
                    ["Atlántico", "Índico", "Ártico", "Pacífico"],
                    "Pacífico",
                    "💧 Pista: Está entre Asia y América."
                ),
            ],
            
            4: [
                Pregunta(
                    "¿Cuántos planetas tiene el Sistema Solar?",
                    ["7", "8", "9", "10"],
                    "8",
                    "💧 Pista: Plutón ya no cuenta como planeta."
                ),
                Pregunta(
                    "¿Qué gas respiramos para vivir?",
                    ["Nitrógeno", "Dióxido de carbono", "Oxígeno", "Hidrógeno"],
                    "Oxígeno",
                    "💧 Pista: Las plantas lo producen durante la fotosíntesis."
                ),
                Pregunta(
                    "¿Cuál es el planeta más cercano al Sol?",
                    ["Venus", "Marte", "Mercurio", "Tierra"],
                    "Mercurio",
                    "💧 Pista: Es el más pequeño del Sistema Solar."
                ),
                Pregunta(
                    "¿Cuántos huesos tiene el cuerpo humano adulto?",
                    ["215", "198", "206", "220"],
                    "206",
                    "💧 Pista: Es un número entre 200 y 210."
                ),
                Pregunta(
                    "¿Qué animal es el más rápido del mundo?",
                    ["León", "Guepardo", "Águila", "Caballo"],
                    "Guepardo",
                    "💧 Pista: Es un felino manchado de África."
                ),
            ],
            
            5: [
                Pregunta(
                    "¿Cuántos colores tiene el arcoíris?",
                    ["5", "6", "7", "8"],
                    "7",
                    "💧 Pista: Rojo, naranja, amarillo... cuenta hasta llegar."
                ),
                Pregunta(
                    "¿Qué instrumento toca un pianista?",
                    ["Guitarra", "Violín", "Piano", "Flauta"],
                    "Piano",
                    "💧 Pista: Tiene teclas blancas y negras."
                ),
                Pregunta(
                    "¿Cuántos continentes hay en el mundo?",
                    ["5", "6", "7", "8"],
                    "7",
                    "💧 Pista: Incluye la Antártida."
                ),
                Pregunta(
                    "¿Quién pintó la Mona Lisa?",
                    ["Miguel Ángel", "Rafael", "Leonardo da Vinci", "Picasso"],
                    "Leonardo da Vinci",
                    "💧 Pista: También inventó máquinas y estudió anatomía."
                ),
                Pregunta(
                    "¿En qué país se inventó el papel?",
                    ["Japón", "India", "Egipto", "China"],
                    "China",
                    "💧 Pista: El país más poblado del mundo."
                ),
            ],
            
            6: [
                Pregunta(
                    "¿Cuánto es la raíz cuadrada de 81?",
                    ["7", "8", "9", "10"],
                    "9",
                    "💧 Pista: 9 x 9 = 81."
                ),
                Pregunta(
                    "¿Cuántos lados tiene un octágono?",
                    ["6", "7", "8", "9"],
                    "8",
                    "💧 Pista: La señal de STOP tiene esa forma."
                ),
                Pregunta(
                    "¿Cuánto es 15% de 200?",
                    ["25", "30", "35", "20"],
                    "30",
                    "💧 Pista: 10% de 200 es 20, más la mitad de eso."
                ),
                Pregunta(
                    "¿Cuántos grados tiene un triángulo en total?",
                    ["90", "180", "270", "360"],
                    "180",
                    "💧 Pista: La mitad de 360."
                ),
                Pregunta(
                    "¿Cuál es el número primo más pequeño?",
                    ["0", "1", "2", "3"],
                    "2",
                    "💧 Pista: Es el único número primo par."
                ),
            ],
            
            7: [
                Pregunta(
                    "¿Cuántas notas musicales hay?",
                    ["5", "6", "7", "8"],
                    "7",
                    "💧 Pista: Do, Re, Mi... cuenta hasta llegar."
                ),
                Pregunta(
                    "¿De qué país es el reggaetón?",
                    ["Colombia", "México", "Puerto Rico", "Cuba"],
                    "Puerto Rico",
                    "💧 Pista: Es una isla del Caribe."
                ),
                Pregunta(
                    "¿Cómo se llama el instrumento de cuerda más grande de la orquesta?",
                    ["Violín", "Viola", "Chelo", "Contrabajo"],
                    "Contrabajo",
                    "💧 Pista: Es tan grande que se toca de pie."
                ),
                Pregunta(
                    "¿Quién es conocido como el Rey del Pop?",
                    ["Elvis Presley", "Michael Jackson", "Prince", "David Bowie"],
                    "Michael Jackson",
                    "💧 Pista: Famoso por el moonwalk."
                ),
                Pregunta(
                    "¿Cuántas cuerdas tiene una guitarra estándar?",
                    ["4", "5", "6", "7"],
                    "6",
                    "💧 Pista: Número entre 5 y 7."
                ),
            ],
            
            8: [
                Pregunta(
                    "¿Cuál es el animal terrestre más grande del mundo?",
                    ["Hipopótamo", "Rinoceronte", "Elefante africano", "Jirafa"],
                    "Elefante africano",
                    "💧 Pista: Tiene trompa y colmillos de marfil."
                ),
                Pregunta(
                    "¿Qué proceso usan las plantas para alimentarse con luz solar?",
                    ["Respiración", "Fotosíntesis", "Digestión", "Oxidación"],
                    "Fotosíntesis",
                    "💧 Pista: Foto = luz, síntesis = crear."
                ),
                Pregunta(
                    "¿Cuántas patas tiene una araña?",
                    ["6", "8", "10", "12"],
                    "8",
                    "💧 Pista: Los insectos tienen 6, las arañas tienen más."
                ),
                Pregunta(
                    "¿Cuál es el árbol más alto del mundo?",
                    ["Baobab", "Ceiba", "Secuoya", "Pino"],
                    "Secuoya",
                    "💧 Pista: Crece en California, EE.UU."
                ),
                Pregunta(
                    "¿Qué tipo de animal es la ballena?",
                    ["Pez", "Reptil", "Mamífero", "Anfibio"],
                    "Mamífero",
                    "💧 Pista: Amamanta a sus crías y respira aire."
                ),
            ],
            
            9: [
                Pregunta(
                    "¿Cómo se define una función en Python?",
                    ["function miFuncion():", "def miFuncion():", "fun miFuncion():", "define miFuncion():"],
                    "def miFuncion():",
                    "💧 Pista: Usa una palabra clave de 3 letras."
                ),
                Pregunta(
                    "¿Qué tipo de dato es esto en Python: {'nombre': 'Ana', 'edad': 20}?",
                    ["Lista", "Tupla", "Diccionario", "Conjunto"],
                    "Diccionario",
                    "💧 Pista: Usa llaves {} y pares clave:valor."
                ),
                Pregunta(
                    "¿Cuál es la salida de: print(type([1, 2, 3]))?",
                    ["<class 'tuple'>", "<class 'dict'>", "<class 'list'>", "<class 'set'>"],
                    "<class 'list'>",
                    "💧 Pista: Los corchetes [] definen este tipo de dato."
                ),
                Pregunta(
                    "¿Qué palabra clave se usa para crear una clase en Python?",
                    ["object", "class", "def", "type"],
                    "class",
                    "💧 Pista: Es la misma palabra en inglés."
                ),
                Pregunta(
                    "¿Cómo se accede al valor 'Bogotá' en: d = {'ciudad': 'Bogotá'}?",
                    ["d.ciudad", "d['ciudad']", "d->ciudad", "d(ciudad)"],
                    "d['ciudad']",
                    "💧 Pista: Se usan corchetes con la clave entre comillas."
                ),
            ],
            
            10: [
                Pregunta(
                    "¿Qué método especial se llama al crear un objeto de una clase?",
                    ["__start__", "__create__", "__init__", "__new__"],
                    "__init__",
                    "💧 Pista: Es el inicializador, empieza y termina con doble guión bajo."
                ),
                Pregunta(
                    "¿Qué hace 'self' dentro de una clase en Python?",
                    ["Llama a la clase padre", "Hace referencia a la instancia actual", "Define un método estático", "Importa un módulo"],
                    "Hace referencia a la instancia actual",
                    "💧 Pista: Es el primer parámetro de los métodos de instancia."
                ),
                Pregunta(
                    "¿Cuál es la salida de: [x**2 for x in range(3)]?",
                    ["[1, 4, 9]", "[0, 1, 4]", "[0, 2, 4]", "[1, 2, 3]"],
                    "[0, 1, 4]",
                    "💧 Pista: range(3) genera 0, 1, 2. Cada uno se eleva al cuadrado."
                ),
                Pregunta(
                    "¿Qué librería de Python se usa para operaciones matemáticas avanzadas?",
                    ["os", "sys", "math", "random"],
                    "math",
                    "💧 Pista: Tiene funciones como floor(), ceil() y sqrt()."
                ),
                Pregunta(
                    "¿Qué hace math.floor(4.9)?",
                    ["5", "4", "4.9", "Error"],
                    "4",
                    "💧 Pista: Floor = piso, redondea hacia abajo."
                ),
            ],
        }
        return datos



def formatear_puntaje(puntaje):
    """Muestra el puntaje con ceros a la izquierda."""
    return str(puntaje).zfill(5)

def corazones(vidas, maximo=3):
    return f"{vidas}/{maximo} ♥"

def estrellas_nivel(nivel, total=10):
    """Retorna barra de progreso visual usando math."""
    llenas = math.floor((nivel / total) * 10)
    return "🔥" * llenas + "⬛" * (10 - llenas)