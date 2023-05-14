# Sudoku

<div style="text-align:center;">
  <image src="https://github.com/JavierAM01/Machine-Learnig-in-Games/blob/main/images/sudoku.gif" style="width:100%; height:12cm;">
</div>
  
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
