import tkinter as tk
import random
import time
import threading
resultado_trivia = False
def generar_laberinto(n):
    laberinto = []
    for i in range(n):
        fila = []
        for j in range(n):
            fila.append(1)  
        laberinto.append(fila)
    laberinto[0][0] = 0  
    laberinto[n-1][n-1] = 2  
    i, j = 0, 0
    camino = [(0, 0)]
    while (i, j) != (n-1, n-1):
        laberinto[i][j] = 0
        if i < n-1 and j < n-1:
            if random.random() < 0.5:
                i += 1
            else:
                j += 1
        elif i < n-1:
            i += 1
        elif j < n-1:
            j += 1
        camino.append((i, j))  
    trivia_pos = random.choice(camino[:-1])  
    laberinto[trivia_pos[0]][trivia_pos[1]] = 6
    return laberinto
def trivia_ventana(text_widget):
    def verificar_respuesta():
        respuesta = int(entry_respuesta.get())
        if respuesta == 49:
            label_resultado.config(text="¡Correcto!")
            global resultado_trivia
            resultado_trivia = True
            top.destroy()
        else:
            label_resultado.config(text="Incorrecto. Intenta de nuevo.")
    top = tk.Toplevel()
    top.title("Pregunta Trivia")
    pregunta_label = tk.Label(top, text="¿Cuánto es 7x7?")
    pregunta_label.pack()
    entry_respuesta = tk.Entry(top)
    entry_respuesta.pack()
    boton_verificar = tk.Button(top, text="Verificar", command=verificar_respuesta)
    boton_verificar.pack()
    label_resultado = tk.Label(top, text="")
    label_resultado.pack()
    top.wait_window()  # Espera hasta que se cierre la ventana
def resolver_laberinto(laberinto, text_widget):
    n = len(laberinto)
    m = len(laberinto[0])
    dp = [[0 for j in range(m)] for i in range(n)]
    dp[0][0] = 1  
    for j in range(1, m):
        if laberinto[0][j] == 0:
            dp[0][j] = dp[0][j-1]
    for i in range(1, n):
        if laberinto[i][0] == 0:
            dp[i][0] = dp[i-1][0]
    for i in range(1, n):
        for j in range(1, m):
            if laberinto[i][j] in [0, 2, 6]:  
                if laberinto[i][j] == 6:
                    trivia_ventana(text_widget)
                    while not resultado_trivia:
                        time.sleep(0.1)
                    laberinto[i][j] = 0  
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])  
    return dp
def imprimir_camino(camino, laberinto, text_widget):
    n = len(laberinto)
    m = len(laberinto[0])
    for i in range(n):
        for j in range(m):
            if camino[i][j] > 0:  
                laberinto[i][j] = 9 
                update_output(laberinto, text_widget)
                time.sleep(0.5)  
def update_output(laberinto, text_widget):
    text_widget.delete('1.0', tk.END)
    for fila in laberinto:
        text_widget.insert(tk.END, f"{fila}\n")
def generar_laberinto_root(text_widget):
    global laberinto
    laberinto = generar_laberinto(10)
    update_output(laberinto, text_widget)
def resolver_laberinto_root(text_widget):
    global resultado_trivia
    resultado_trivia = False
    camino_dp = resolver_laberinto(laberinto, text_widget)
    imprimir_camino(camino_dp, laberinto, text_widget)
def resolver(text_widget):
    threading.Thread(target=resolver_laberinto_root, args=(text_widget,)).start()
def crear_ventana():
    root = tk.Tk()
    root.title("Actividad 5: Laberinto")
    text_output = tk.Text(root, height=10, width=30)
    text_output.pack()
    btn_generar = tk.Button(root, text="Generar Laberinto", command=lambda: generar_laberinto_root(text_output))
    btn_generar.pack()
    btn_resolver = tk.Button(root, text="Resolver Laberinto", command=lambda: resolver(text_output))
    btn_resolver.pack()
    root.mainloop()
crear_ventana()
