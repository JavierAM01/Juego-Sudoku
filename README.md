# Sudoku

<div style="text-align:center;">
  <image src="https://github.com/JavierAM01/Machine-Learnig-in-Games/blob/main/images/sudoku.gif" style="width:100%; height:12cm;">
</div>

Uso de la interfaz:
  
  1) Hacer click con el ratón en la casilla que quieras modificar. 
  2) Insertar idea: tocar el número que quieras introducir.
  3) Insertar número definitivo: hacer click en ```ENTER```. En caso de no ser un número válido, este no se introducirá.
  
## Algoritmo

El algoritmo de resolución de Sudoku utiliza la recursividad para resolver este desafiante rompecabezas. La idea principal es descomponer el problema en subproblemas más pequeños y resolverlos de forma recursiva. El algoritmo busca una casilla vacía en el tablero y prueba diferentes números del 1 al 9 para colocar en esa casilla, verificando si cumple con las reglas del Sudoku. Si se encuentra una solución válida, se avanza a la siguiente casilla vacía y se repite el proceso. Si no se encuentra una solución válida, se retrocede y se prueba con otro número. Este proceso continúa hasta llenar todas las casillas o hasta encontrar una solución completa. La recursividad permite explorar todas las combinaciones posibles de números de manera eficiente.

## Explicación
  
Para la creación del tablero creamos un objecto **Caja** la cual representa cada una de los 9x9 casillas del tablero. En ella guardamos 
el valor temporal que le queramos dar, así como si el valor es definitivo o no. Por último le añadimo una pequeña función para que grafique 
su número respectivo (distinto según si es temporal o definitivo).

Finalmente generamos el objeto **Sudoku** para el juego final. El él además creamos una función para la resolución del mismo. El algoritmo es simple,
pues se basa en buscar iterativamente la solución al problema. Para ello creamos una función recursiva.
  
```python
class Sudoku:
    
    (...)
    
    def resolver(self, Tablero):

        # find empty grid
        find = self.findEmpty(Tablero)
        if not find: return True
        x, y = find

        # fill valid
        for i in range(1,10):
            if self.es_valido(Tablero, i, x, y):
                Tablero[x][y] = i

                if self.resolver(Tablero): return True

                # undo
                Tablero[x][y] = 0

        return False
```
  
para saber si una posición es válida o no definimos una función que checkee la fila, columna y bloque respectivo a dicha posición y mire si dicho 
número ya existe en alguna de las tres.
  
```python
    def es_valido(self, Tablero, numero, x, y):

        # row
        for i in range(9):
            if Tablero[x][i] == numero and i != y: 
                return False

        # col
        for i in range(9):
            if Tablero[i][y] == numero and i != x: 
                return False

        # box
        bloque_x = x // 3
        bloque_y = y // 3
        for i in range(3*bloque_x, 3*bloque_x + 3):
            for j in range(3*bloque_y, 3*bloque_y + 3):
                if Tablero[i][j] == numero and (i,j) != (x,y): 
                    return False

        return True
```
