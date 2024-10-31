import numpy as np  # Importar la biblioteca NumPy para manipulación numérica
import math  # Importar el módulo de funciones matemáticas
import h5py  # Importar la biblioteca h5py para trabajar con archivos HDF5
import matplotlib.pyplot as plt  # Importar Matplotlib para visualización de datos
import os  # Importar el módulo os para funciones del sistema operativo
import tempfile  # Importar el módulo tempfile para crear archivos temporales
from Const import *


# Definir la clase Mapa
class Mapa:

    def __init__(self, filename):
        self.filename = filename  # Almacenar la ruta del archivo
        self.f = h5py.File(filename, 'r')  # Abrir el archivo HDF5 en modo de solo lectura
        

        # Obtener información del primer conjunto de datos
        dataset_name = list(self.f.keys())[0]
        dataset = self.f[dataset_name]

        # Atributos del mapa
        self.nodata_value = dataset.attrs["nodata_value"]
        self.size_cell = dataset.attrs['cellsize']
        self.up_left = (dataset.attrs['ysup'], dataset.attrs['xinf'])
        self.down_right = (dataset.attrs['yinf'], dataset.attrs['xsup'])
        self.dim = (dataset.shape[0], dataset.shape[1])

        # Inicializar listas para almacenar información de cada conjunto de datos
        self.up_left_list = []
        self.down_right_list = []
        self.dim_list = []

        # Iterar sobre todos los conjuntos de datos y recopilar información
        for dataset_name in self.f.keys():
            dataset = self.f[dataset_name]
            up_left = (dataset.attrs['ysup'], dataset.attrs['xinf'])
            down_right = (dataset.attrs['yinf'], dataset.attrs['xsup'])
            dim = (dataset.shape[0], dataset.shape[1])

            self.up_left_list.append(up_left)
            self.down_right_list.append(down_right)
            self.dim_list.append(dim)


    def umt_YX(self, y, x) -> float:
        # Iterar sobre los conjuntos de datos y buscar el que contiene las coordenadas
        for i, (up_left, down_right) in enumerate(zip(self.up_left_list, self.down_right_list), start=1):
            if down_right[0] <= y < up_left[0] and up_left[1] <= x < down_right[1]:
                dataset = self.f[list(self.f.keys())[i - 1]]
                data = dataset[()]

                # Calcular las coordenadas en las que insertar los datos del conjunto actual
                start_row = int((up_left[0] - y) / self.size_cell)
                start_col = int((x - up_left[1]) / self.size_cell)

                if 0 <= start_row < data.shape[0] and 0 <= start_col < data.shape[1]:
                    return data[start_row, start_col]
                else:
                    return self.nodata_value
                
                    
        # Devolver el valor nodata si las coordenadas no se encuentran en ningún conjunto
        return self.nodata_value
    
    def resize(self, factor, transform, new_name):
        #Abrimos el archivo LaGomera.hdf5 y creamos uno con el nombre proporcionado
        with h5py.File(new_name, 'w') as f_new, h5py.File(self.filename, 'r') as f:
            #Recorremos los 5 conjuntos de datos
            for ds_name in f.keys():
                # Obtener el conjunto de datos actual del archivo original
                old_data = f[ds_name]
                # Calcular las nuevas dimensiones del conjunto de datos después de la reducción de tamaño
                new_shape = (math.ceil(old_data.shape[0] / factor), math.ceil(old_data.shape[1] / factor))
                # Crear una nueva matriz llena de valores de nodata con las nuevas dimensiones
                new_data = np.full(new_shape,self.nodata_value,dtype=float)
                # Iterar sobre las filas de la nueva matriz
                for i in range(new_shape[0]):
                    for j in range(new_shape[1]):
                        # Calcular las coordenadas en el conjunto de datos original correspondientes a la nueva matriz
                        y_start=i*factor
                        x_start=j*factor
                        y_end=(i+1)*factor
                        x_end=(j+1)*factor

                        # Extraer la región del conjunto de datos original para la nueva matriz
                        subdataset = old_data[y_start:y_end, x_start:x_end]

                        # Convertir los valores nodata a NaN para facilitar el cálculo
                        subdataset[subdataset==self.nodata_value] = np.nan

                        # Verificar si todos los valores en la región son NaN
                        if np.all(np.isnan(subdataset)):
                            nuevo_valor = self.nodata_value   # Si son todos NaN, el nuevo valor sera no data value
                        else:
                            # Calcular el nuevo valor basado en la transformación especificada (mean o max)
                            nuevo_valor = transform(subdataset)
                        # Asignar el nuevo valor a la posición correspondiente en la nueva matriz
                        new_data[i,j]=nuevo_valor
                # Copiar atributos relevantes del conjunto de datos original al nuevo
                ds_new = f_new.create_dataset(ds_name, data=new_data)
                ds_new.attrs['nodata_value'] = old_data.attrs['nodata_value']
                ds_new.attrs['cellsize'] = old_data.attrs['cellsize'] * factor
                ds_new.attrs['xinf'] = old_data.attrs['xinf']
                ds_new.attrs['yinf'] = old_data.attrs['yinf']
                ds_new.attrs['xsup'] = old_data.attrs['xsup']
                ds_new.attrs['ysup'] = old_data.attrs['ysup']
        # Crear un nuevo objeto Mapa con el archivo HDF5 redimensionado
        return Mapa(new_name)
            
    def plot_all_datasets_subplots(self):
        num_datasets = len(self.f.keys())
        num_cols = 2  # Número de columnas en el subplot (puedes ajustar según sea necesario)
        num_rows = (num_datasets + num_cols - 1) // num_cols  # Número de filas

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 8))

        for i, (dataset_name, up_left, down_right, dim) in enumerate(
            zip(self.f.keys(), self.up_left_list, self.down_right_list, self.dim_list), start=1
        ):
            # Crear un array vacío para almacenar el conjunto actual
            data_combined = np.full((dim[0], dim[1]), self.nodata_value, dtype=float)

            dataset = self.f[dataset_name]
            data = dataset[()]  # Obtener todo el conjunto de datos

            # Calcular las coordenadas en las que insertar los datos del conjunto actual
            start_row = int((max(up_left[0], down_right[0]) - self.up_left[0]) / self.size_cell)
            start_col = int((min(up_left[1], down_right[1]) - self.up_left[1]) / self.size_cell)

            # Ajustar las dimensiones del conjunto de datos si es necesario
            adjusted_data = data[:min(data.shape[0], dim[0] - start_row), :min(data.shape[1], dim[1] - start_col)]

            # Insertar los datos del conjunto actual en el array del mapa completo
            data_combined[start_row:start_row + adjusted_data.shape[0], start_col:start_col + adjusted_data.shape[1]] = adjusted_data

            # Aplicar escala logarítmica a los datos, ignorando los valores negativos (agua)
            data_combined_log = np.log1p(np.maximum(data_combined, 0))

            # Utilizar una paleta de colores estilo mapa topográfico con escala logarítmica
            cmap = plt.get_cmap('terrain')

            # Calcular las coordenadas centrales del conjunto
            central_x = (up_left[1] + down_right[1]) / 2
            central_y = (up_left[0] + down_right[0]) / 2

            # Calcular las coordenadas del subplot actual
            row = i // num_cols
            col = i % num_cols

            # Visualizar el conjunto en el subplot
            axes[row, col].imshow(data_combined_log, cmap=cmap, extent=[up_left[1], down_right[1], down_right[0], up_left[0]])
            axes[row, col].set_title(f'Conjunto {i}')
            axes[row, col].set_xlabel('Coordenada X-UMT')
            axes[row, col].set_ylabel('Coordenada Y-UMT')

            # Imprimir las coordenadas centrales
            axes[row, col].text(central_x, central_y, f'({central_x:.2f}, {central_y:.2f})', color='red')

        # Ajustes finales para la presentación
        fig.tight_layout()
        plt.savefig("mapa.png")
        plt.show()

    def close(self):
        self.f.close()

def transformacion_media(celdas):
    return np.nanmean(celdas)
def transformacion_max(celdas):
    return np.nanmax(celdas)
 
if __name__ == "__main__":
    archivo_hdf5 = FileNameGlobal
    mi_mapa = Mapa(archivo_hdf5)

    
    #y_coord, x_coord = 3101029,282917			
    #altura = mi_mapa.umt_YX(y_coord, x_coord)
    #print(f"La altura en las coordenadas ({y_coord}, {x_coord}) es: {altura}")

    #Type: mean o max
    name_reszie_map=DirNameResize+"300.hdf5"
    nuevo_mapa = mi_mapa.resize(factor=300, transform=transformacion_media,new_name=name_reszie_map)
        # Ejemplo de uso de umt_YX
    y_coord, x_coord = 3101311,278997	
    altura = nuevo_mapa.umt_YX(y_coord, x_coord)
    print(type(altura))
    print(f"La altura en las coordenadas ({y_coord}, {x_coord}) es: {altura}")
    mi_mapa.close()
