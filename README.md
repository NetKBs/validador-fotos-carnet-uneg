
# Validador De Fotos Para Carnets

Este proyecto, desarrollado en el marco de la asignatura “Innovación De Desarrollo”, tiene como objetivo principal la creación de un algoritmo basado en inteligencia artificial. Este algoritmo se diseñó con la intención de automatizar y optimizar el proceso de actualización de los carnets de los estudiantes de la Universidad Nacional Experimental de Guayana (UNEG).

## Resumen Del Proyecto
El algoritmo funciona a través de un proceso de validación de fotos. En primer lugar, se recibe una foto del estudiante junto con su identificación. El algoritmo verifica que la foto cumpla con los criterios establecidos para ser considerada válida. Una vez que la foto ha sido validada, el algoritmo procede a comparar el rostro que aparece en la foto del estudiante con el rostro que aparece en su identificación. Esta comparación se realiza mediante técnicas de reconocimiento facial, permitiendo determinar si las dos imágenes corresponden a la misma persona.

Este proceso de validación y comparación garantiza que la foto del carnet sea una representación precisa y actualizada del estudiante, lo que contribuye a la seguridad y la integridad del sistema de identificación de la UNEG. Además, al automatizar este proceso, se reduce la carga de trabajo del personal administrativo y se agiliza la emisión de los carnets de estudiante.


## Dependencias

Para la ejecución del proyecto se necesitan las siguientes dependencias
- facenet_pytorch
- numpy
- matplotlib `opcional` `requerido en la demo`
- pillow
- scipy



    
## Lista de tareas (módulos a desarrollar)

- [ ] Modulo para cargar las fotos con su par cédula

- [ ] Modulo para redimensionar y recortar la foto de la persona y cédulas.

- [ ] Modulo para extraer y verificar número de cédula

- [ ] Modulo para verificar si la persona tiene gorra/sombrero/etc

- [ ] Modulo para verificar el fondo blanco. 

- [x] Modulo para extraer rostros

- [ ] Modulo verificar el rostro de la persona y cédula (sean humanos)

- [ ] Modulo para para comparar la cédula y la persona

- [ ] Modulo para el manejo de errores.


