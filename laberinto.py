import random
import time
import os

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

def trivia():
    pregunta = "¿Cuánto es 7x7?"
    respuesta_correcta = 49

    while True:
        try:
            respuesta = int(input(f"Pregunta trivia: {pregunta} "))
            if respuesta == respuesta_correcta:
                print("¡Correcto!")
                return True
            else:
                print("Incorrecto. Intenta de nuevo.")
        except ValueError:
            print("Por favor, ingresa un número válido.")

def resolver_laberinto(laberinto):
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
                    print(f"Llegaste a una celda trivia en ({i}, {j})")
                    if trivia():
                        laberinto[i][j] = 0 
                if laberinto[i][j] == 0 or laberinto[i][j] == 2:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])  

    return dp

def imprimir_camino(camino, laberinto):
    n = len(laberinto)
    m = len(laberinto[0])
    for i in range(n):
        for j in range(m):
            if camino[i][j] > 0:  
                laberinto[i][j] = 9 
                os.system("cls")
                for fila in laberinto:
                    print(fila)
                time.sleep(0.5)  
    return laberinto


laberinto = generar_laberinto(10)
print("Laberinto generado:")
for fila in laberinto:
    print(fila)

camino_dp = resolver_laberinto(laberinto)
imprimir_camino(camino_dp, laberinto)
print("Laberinto resuelto")