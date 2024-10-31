import random
import colorama

# Inicializar colorama
colorama.init(autoreset=True)

def leer_preguntas(nombre_archivo):
    matriz_preguntas = []

    with open(nombre_archivo, 'r', encoding='utf-8') as file:
        pregunta = []
        for line in file:
            line = line.strip()
            if not line:
                continue  # Ignorar líneas vacías
            elif line.startswith(("A.", "B.", "C.", "D.")):
                pregunta.append(line[3:].strip())  # Agregar opciones a la pregunta
            elif line.startswith("ANSWER:"):
                pregunta.append(line[7:].strip())  # Agregar la respuesta correcta
                matriz_preguntas.append(pregunta)
                pregunta = []  # Resetear para la siguiente pregunta
            else:
                pregunta = [line]  # Nueva pregunta

    return matriz_preguntas

def mostrar_pregunta(pregunta):
    print(pregunta[0])
    opciones = ['A', 'B', 'C', 'D']
    for i, opcion in enumerate(pregunta[1:5], start=1):
        print(f"{opciones[i-1]}. {opcion}")
    respuesta = input("Ingrese la respuesta: ").strip().upper()
    return respuesta

def validar_respuesta(respuesta_correcta, respuesta_usuario):
    return respuesta_correcta == respuesta_usuario

def generar_pregunta(preguntas):
    indice = random.randint(0, len(preguntas) - 1)
    pregunta = preguntas.pop(indice)  # Elimina la pregunta de la lista
    respuesta_usuario = mostrar_pregunta(pregunta)
    if validar_respuesta(pregunta[5], respuesta_usuario):
        print(colorama.Fore.GREEN + "Respuesta correcta")
        return True
    else:
        print(colorama.Fore.RED + f"Respuesta incorrecta. La respuesta correcta era: {pregunta[5]}")
        return False

def main():
    preguntas = leer_preguntas("preguntasT.txt")
    correctas = 0
    incorrectas = 0

    while preguntas:
        if generar_pregunta(preguntas):
            correctas += 1
        else:
            incorrectas += 1
        print(f"Respuestas correctas: {correctas}, Respuestas incorrectas: {incorrectas}")

if __name__ == "__main__":
    main()
