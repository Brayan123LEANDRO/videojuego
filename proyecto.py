# interfaz del juego
# usa tkinter

import tkinter as tk
from libreria import (
    Jugador, Juego,
    formatear_puntaje, corazones, estrellas_nivel
)



C = {
    "fondo":      "#1C1919",
    "panel":      "#1a0a00",
    "fuego1":     "#ff4500",
    "fuego2":     "#ff8c00",
    "fuego3":     "#ffd700",
    "lava":       "#8b0000",
    "agua":       "#00bfff",
    "correcto":   "#00e676",
    "incorrecto": "#ff1744",
    "texto":      "#fff3e0",
    "gris":       "#a0785a",
    "boton":      "#2d1000",
    "boton2":     "#3d1a00",
}



class App:
    def __init__(self, root):
        self.root = root
        self.root.title("🌋 El Desafío del Conocimiento")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.root.configure(bg=C["fondo"])

        self.nombre_var = tk.StringVar()
        self.juego = None
        self.respondido = False
        self.frame_actual = None

        self._ir_login()

    def _limpiar(self):
        if self.frame_actual:
            self.frame_actual.destroy()

    
    def _ir_login(self):
        self._limpiar()
        f = tk.Frame(self.root, bg=C["fondo"])
        f.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frame_actual = f

        tk.Label(f, text="🌋", font=("Segoe UI Emoji", 70),
                 bg=C["fondo"], fg=C["fuego1"]).pack(pady=(30, 0))

        tk.Label(f, text="EL DESAFÍO DEL CONOCIMIENTO",
                 font=("Courier New", 20, "bold"),
                 bg=C["fondo"], fg=C["fuego2"]).pack()

        tk.Label(f, text="Derrota a 10 monstruos y conviértete en Maestro del Volcán",
                 font=("Courier New", 10),
                 bg=C["fondo"], fg=C["gris"]).pack(pady=(4, 30))

        panel = tk.Frame(f, bg=C["panel"], padx=50, pady=35)
        panel.pack(padx=100, fill="x")

        tk.Label(panel, text="⚔️  Crea tu perfil de aventurero",
                 font=("Courier New", 13, "bold"),
                 bg=C["panel"], fg=C["fuego3"]).pack(pady=(0, 15))

        tk.Label(panel, text="Ingresa tu nombre:",
                 font=("Courier New", 11),
                 bg=C["panel"], fg=C["texto"]).pack()

        self.entrada = tk.Entry(
            panel, textvariable=self.nombre_var,
            font=("Courier New", 14),
            bg=C["boton2"], fg=C["fuego2"],
            insertbackground=C["fuego2"],
            relief="flat", width=22, justify="center"
        )
        self.entrada.pack(ipady=10, pady=8)
        self.entrada.focus()

        self.lbl_error = tk.Label(panel, text="",
                                   font=("Courier New", 10),
                                   bg=C["panel"], fg=C["incorrecto"])
        self.lbl_error.pack()

        tk.Button(
            panel, text="🔥  ENTRAR AL VOLCÁN",
            font=("Courier New", 12, "bold"),
            bg=C["fuego1"], fg=C["fondo"],
            activebackground=C["lava"],
            relief="flat", cursor="hand2",
            padx=20, pady=10,
            command=self._iniciar
        ).pack(pady=(15, 0))

        tk.Label(f, text="🛡️ 3 vidas · 3 preguntas por monstruo · Pasa con 2/3 · 💧 1 pista por nivel",
                 font=("Courier New", 9),
                 bg=C["fondo"], fg=C["gris"]).pack(pady=(20, 0))

        self.root.bind("<Return>", lambda e: self._iniciar())


    def _ir_monstruo(self):
        self._limpiar()
        f = tk.Frame(self.root, bg=C["fondo"])
        f.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frame_actual = f

        monstruo = self.juego.monstruo_actual()
        jugador = self.juego.jugador

        tk.Label(f, text=estrellas_nivel(jugador.nivel_actual),
                 font=("Segoe UI Emoji", 14),
                 bg=C["fondo"], fg=C["fuego1"]).pack(pady=(20, 0))

        tk.Label(f, text=f"NIVEL {jugador.nivel_actual} DE 10",
                 font=("Courier New", 12, "bold"),
                 bg=C["fondo"], fg=C["fuego3"]).pack()

        tk.Label(f, text=monstruo.emoji,
                 font=("Segoe UI Emoji", 90),
                 bg=C["fondo"]).pack(pady=(20, 5))

        tk.Label(f, text=monstruo.nombre,
                 font=("Courier New", 22, "bold"),
                 bg=C["fondo"], fg=C["fuego1"]).pack()

        tk.Label(f, text=monstruo.descripcion,
                 font=("Courier New", 11),
                 bg=C["fondo"], fg=C["gris"]).pack(pady=(5, 20))

        info = tk.Frame(f, bg=C["panel"], padx=30, pady=12)
        info.pack(padx=80, fill="x")

        tk.Label(info, text=corazones(jugador.vidas),
         font=("Arial", 16, "bold"),
         bg=C["panel"], fg="#ff3b3b").pack(side="left", expand=True)

        tk.Label(info, text=f"🏆 {formatear_puntaje(jugador.puntaje)}",
                 font=("Courier New", 13, "bold"),
                 bg=C["panel"], fg=C["fuego3"]).pack(side="left", expand=True)

        tk.Label(info, text=f"👤 {jugador.nombre}",
                 font=("Courier New", 11),
                 bg=C["panel"], fg=C["texto"]).pack(side="left", expand=True)

        tk.Button(
            f, text="⚔️  ¡ENFRENTAR AL MONSTRUO!",
            font=("Courier New", 13, "bold"),
            bg=C["fuego1"], fg=C["fondo"],
            activebackground=C["lava"],
            relief="flat", cursor="hand2",
            padx=20, pady=12,
            command=self._ir_pregunta
        ).pack(pady=30)


    def _ir_pregunta(self):
        self._limpiar()
        self.respondido = False

        f = tk.Frame(self.root, bg=C["fondo"])
        f.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frame_actual = f

        jugador = self.juego.jugador
        pregunta = self.juego.pregunta_actual()
        num = self.juego.indice_pregunta + 1

        
        hud = tk.Frame(f, bg=C["panel"], pady=8)
        hud.pack(fill="x", padx=15, pady=(15, 8))

        tk.Label(hud, text=f"👤 {jugador.nombre}",
                 font=("Courier New", 10, "bold"),
                 bg=C["panel"], fg=C["fuego3"]).grid(row=0, column=0, padx=12)

        tk.Label(hud, text=f"🏆 {formatear_puntaje(jugador.puntaje)}",
                 font=("Courier New", 10, "bold"),
                 bg=C["panel"], fg=C["fuego2"]).grid(row=0, column=1, padx=12)

        self.lbl_vidas_hud = tk.Label(hud, text=corazones(jugador.vidas),
                                       font=("Segoe UI Emoji", 11),
                                       bg=C["panel"])
        self.lbl_vidas_hud.grid(row=0, column=2, padx=12)

        tk.Label(hud, text=f"Nivel {jugador.nivel_actual} · Pregunta {num}/3",
                 font=("Courier New", 10),
                 bg=C["panel"], fg=C["gris"]).grid(row=0, column=3, padx=12)

        hud.columnconfigure((0,1,2,3), weight=1)

        m = self.juego.monstruo_actual()
        tk.Label(f, text=f"{m.emoji} vs {jugador.nombre}",
                 font=("Courier New", 11),
                 bg=C["fondo"], fg=C["gris"]).pack(pady=(2, 5))

        # Pregunta
        panel_p = tk.Frame(f, bg=C["panel"])
        panel_p.pack(fill="x", padx=25, pady=4)

        tk.Label(panel_p, text=pregunta.texto,
                 font=("Courier New", 13, "bold"),
                 bg=C["panel"], fg=C["texto"],
                 wraplength=600, justify="center",
                 pady=18, padx=15).pack(fill="x")

        
        self.lbl_pista = tk.Label(f, text="",
                                   font=("Courier New", 10, "italic"),
                                   bg=C["fondo"], fg=C["agua"],
                                   wraplength=600)
        self.lbl_pista.pack(pady=(4, 2))

        
        self.botones = []
        fb = tk.Frame(f, bg=C["fondo"])
        fb.pack(padx=25, fill="x", pady=4)

        opciones = pregunta.opciones_mezcladas()
        for i in range(4):
            op = opciones[i]
            btn = tk.Button(
                fb, text=op,
                font=("Courier New", 11),
                bg=C["boton"], fg=C["texto"],
                activebackground=C["boton2"],
                relief="flat", cursor="hand2",
                wraplength=290, justify="center",
                pady=10,
                command=lambda o=op: self._responder(o)
            )
            btn.grid(row=i//2, column=i%2, padx=8, pady=5, sticky="ew")
            self.botones.append(btn)

        fb.columnconfigure(0, weight=1)
        fb.columnconfigure(1, weight=1)

        # Fila inferior
        fila_inf = tk.Frame(f, bg=C["fondo"])
        fila_inf.pack(fill="x", padx=25, pady=8)

        escudo_ok = jugador.escudos > 0
        self.btn_escudo = tk.Button(
            fila_inf,
            text=f"💧 Escudo de agua {'✅' if escudo_ok else '❌'}",
            font=("Courier New", 10),
            bg=C["agua"] if escudo_ok else C["boton"],
            fg=C["fondo"] if escudo_ok else C["gris"],
            relief="flat", cursor="hand2",
            padx=12, pady=6,
            command=self._usar_escudo,
            state="normal" if escudo_ok else "disabled"
        )
        self.btn_escudo.pack(side="left")

        self.btn_siguiente = tk.Button(
            fila_inf, text="Siguiente →",
            font=("Courier New", 11, "bold"),
            bg=C["fuego2"], fg=C["fondo"],
            activebackground=C["fuego1"],
            relief="flat", cursor="hand2",
            padx=16, pady=6,
            command=self._siguiente,
            state="disabled"
        )
        self.btn_siguiente.pack(side="right")

    
    def _ir_resultado_nivel(self, superado):
        self._limpiar()
        f = tk.Frame(self.root, bg=C["fondo"])
        f.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frame_actual = f

        jugador = self.juego.jugador
        m = self.juego.monstruo_actual()

        if superado:
            emoji, titulo, color = "🎉", f"¡Derrotaste a {m.nombre}!", C["correcto"]
            sub = f"Correctas: {self.juego.correctas_nivel}/3 · ¡Subes al nivel {jugador.nivel_actual}!"
        else:
            emoji, titulo, color = "💀", f"¡{m.nombre} te venció!", C["incorrecto"]
            sub = f"Solo respondiste {self.juego.correctas_nivel}/3"

        tk.Label(f, text=emoji, font=("Segoe UI Emoji", 70),
                 bg=C["fondo"]).pack(pady=(50, 5))
        tk.Label(f, text=titulo, font=("Courier New", 20, "bold"),
                 bg=C["fondo"], fg=color).pack()
        tk.Label(f, text=sub, font=("Courier New", 11),
                 bg=C["fondo"], fg=C["gris"]).pack(pady=(5, 20))
        tk.Label(f, text=corazones(jugador.vidas),
                 font=("Segoe UI Emoji", 20), bg=C["fondo"]).pack()
        tk.Label(f, text=f"🏆 Puntaje: {formatear_puntaje(jugador.puntaje)}",
                 font=("Courier New", 13, "bold"),
                 bg=C["fondo"], fg=C["fuego3"]).pack(pady=8)

        if superado:
            tk.Button(f, text="➡️  Siguiente nivel",
                      font=("Courier New", 12, "bold"),
                      bg=C["correcto"], fg=C["fondo"],
                      relief="flat", cursor="hand2",
                      padx=20, pady=10,
                      command=self._continuar_nivel).pack(pady=20)
        elif self.juego.juego_perdido():
            tk.Button(f, text="💀  VER GAME OVER",
                      font=("Courier New", 12, "bold"),
                      bg=C["incorrecto"], fg=C["texto"],
                      relief="flat", cursor="hand2",
                      padx=20, pady=10,
                      command=self._ir_game_over).pack(pady=20)
        else:
            tk.Button(f, text="🔄  Reintentar nivel",
                      font=("Courier New", 12, "bold"),
                      bg=C["fuego1"], fg=C["fondo"],
                      relief="flat", cursor="hand2",
                      padx=20, pady=10,
                      command=self._reintentar_nivel).pack(pady=20)

    
    def _ir_game_over(self):
        self._limpiar()
        f = tk.Frame(self.root, bg=C["fondo"])
        f.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frame_actual = f

        jugador = self.juego.jugador

        tk.Label(f, text="💀", font=("Segoe UI Emoji", 80),
                 bg=C["fondo"]).pack(pady=(40, 5))
        tk.Label(f, text="GAME OVER",
                 font=("Courier New", 36, "bold"),
                 bg=C["fondo"], fg=C["incorrecto"]).pack()
        tk.Label(f, text=f"El volcán te consumió, {jugador.nombre}...",
                 font=("Courier New", 12),
                 bg=C["fondo"], fg=C["gris"]).pack(pady=(5, 25))

        panel = tk.Frame(f, bg=C["panel"], padx=40, pady=20)
        panel.pack(padx=100, fill="x")

        for icono, etiqueta, valor in [
            ("🌋", "Llegaste al nivel", str(jugador.nivel_actual)),
            ("🏆", "Puntaje obtenido",  formatear_puntaje(jugador.puntaje)),
            ("⚔️",  "Rango alcanzado",   jugador.rango()),
        ]:
            fila = tk.Frame(panel, bg=C["panel"])
            fila.pack(fill="x", pady=4)
            tk.Label(fila, text=f"{icono}  {etiqueta}:",
                     font=("Courier New", 12), bg=C["panel"],
                     fg=C["gris"], width=22, anchor="w").pack(side="left")
            tk.Label(fila, text=valor,
                     font=("Courier New", 12, "bold"),
                     bg=C["panel"], fg=C["fuego2"]).pack(side="left")

        tk.Button(f, text="🔄  VOLVER AL INICIO",
                  font=("Courier New", 12, "bold"),
                  bg=C["fuego1"], fg=C["fondo"],
                  activebackground=C["lava"],
                  relief="flat", cursor="hand2",
                  padx=20, pady=10,
                  command=self._ir_login).pack(pady=25)

    
    def _ir_victoria(self):
        self._limpiar()
        f = tk.Frame(self.root, bg=C["fondo"])
        f.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frame_actual = f

        jugador = self.juego.jugador
        resumen = self.juego.resumen()

        tk.Label(f, text="🏆", font=("Segoe UI Emoji", 80),
                 bg=C["fondo"]).pack(pady=(30, 5))
        tk.Label(f, text="¡MAESTRO DEL VOLCÁN!",
                 font=("Courier New", 24, "bold"),
                 bg=C["fondo"], fg=C["fuego3"]).pack()
        tk.Label(f, text=f"¡Lo lograste, {jugador.nombre}! Derrotaste los 10 monstruos",
                 font=("Courier New", 11),
                 bg=C["fondo"], fg=C["gris"]).pack(pady=(5, 20))

        panel = tk.Frame(f, bg=C["panel"], padx=40, pady=20)
        panel.pack(padx=80, fill="x")

        for icono, etiqueta, valor, color in [
            ("🏆", "Puntaje final",   formatear_puntaje(resumen["puntaje"]), C["fuego3"]),
            ("❤️",  "Vidas restantes", corazones(resumen["vidas"]),            C["correcto"]),
            ("⚔️",  "Rango obtenido",  resumen["rango"],                       C["fuego2"]),
            ("📊", "Avance",          f"{resumen['avance']}%",                C["fuego1"]),
        ]:
            fila = tk.Frame(panel, bg=C["panel"])
            fila.pack(fill="x", pady=4)
            tk.Label(fila, text=f"{icono}  {etiqueta}:",
                     font=("Courier New", 12), bg=C["panel"],
                     fg=C["gris"], width=22, anchor="w").pack(side="left")
            tk.Label(fila, text=valor,
                     font=("Courier New", 12, "bold"),
                     bg=C["panel"], fg=color).pack(side="left")

        tk.Button(f, text="🔄  JUGAR DE NUEVO",
                  font=("Courier New", 12, "bold"),
                  bg=C["fuego3"], fg=C["fondo"],
                  activebackground=C["fuego2"],
                  relief="flat", cursor="hand2",
                  padx=20, pady=10,
                  command=self._ir_login).pack(pady=20)


    def _iniciar(self):
        nombre = self.nombre_var.get().strip()
        if not nombre:
            self.lbl_error.config(text="⚠️ Debes ingresar un nombre para entrar al volcán")
            self.entrada.focus()
            return
        jugador = Jugador(nombre)
        self.juego = Juego(jugador)
        self._ir_monstruo()

    def _usar_escudo(self):
        if self.respondido:
            return
        if self.juego.jugador.usar_escudo():
            pregunta = self.juego.pregunta_actual()
            self.lbl_pista.config(text=pregunta.pista)
            self.btn_escudo.config(
                text="💧 Escudo usado ✅",
                bg=C["boton"], fg=C["gris"],
                state="disabled"
            )

    def _responder(self, opcion):
        if self.respondido:
            return
        self.respondido = True

        pregunta = self.juego.pregunta_actual()
        es_correcta = self.juego.responder(opcion)

        for btn in self.botones:
            t = btn.cget("text")
            if pregunta.verificar(t):
                btn.config(bg=C["correcto"], fg=C["fondo"])
            elif t == opcion and not es_correcta:
                btn.config(bg=C["incorrecto"], fg=C["texto"])
            btn.config(state="disabled")

        self.lbl_vidas_hud.config(text=corazones(self.juego.jugador.vidas))
        self.btn_siguiente.config(state="normal")
        self.btn_escudo.config(state="disabled")

    def _siguiente(self):
        if self.juego.juego_perdido():
            self._ir_game_over()
            return
        if self.juego.indice_pregunta < self.juego.PREGUNTAS_POR_NIVEL:
            self._ir_pregunta()
        else:
            superado = self.juego.nivel_superado()  
            self._ir_resultado_nivel(superado)

    def _continuar_nivel(self):
        self.juego.avanzar_nivel()

        if self.juego.juego_ganado():
           self._ir_victoria()
        else:
           self._ir_monstruo()

    def _reintentar_nivel(self):
        self.juego.cargar_nivel()
        self._ir_monstruo()


if __name__ == "__main__":
    ventana = tk.Tk()
    App(ventana)
    ventana.mainloop()
    