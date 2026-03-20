import requests

def fetch_maze_data():
    url = "https://77c1-2803-1800-4202-201-d89c-e9f9-d163-b844.ngrok-free.app/maze"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción si hay un error HTTP
        data = response.json()  # Convierte la respuesta JSON a un diccionario
        return data  # Devuelve la lista de listas
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Ejemplo de uso
maze_data = fetch_maze_data()
if maze_data:
    print("Maze Data:", maze_data)