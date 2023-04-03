from sudoku import Sudoku


def main():
    s = Sudoku()
    print("Elige nivel de juego:")
    print(" 1) Nivel Facil")
    print(" 2) Nivel Medio")
    print(" 3) Nivel Dificil")
    try:
        nivel = int(input(" > "))
    except:
        nivel = 3
    s.jugar(nivel-1)

if __name__ == "__main__":
    main()

