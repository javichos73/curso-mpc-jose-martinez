# Comparacion Spec a mano vs Spec Kit

## Pruebas ejecutadas

| Caso de prueba | Spec a mano (Bloque 3.A) | Spec Kit (Bloque 3.B) |
| --- | --- | --- |
| Normal (5 kg a lb) | Retorna 11.02 como numero float | Imprime 5.0 kg = 11.0231 lbs en consola |
| Caso borde (-10 kg) | Lanza un error ValueError en Python | Muestra un mensaje de error y termina con exit code 1 |
| No contemplado (10 toneladas) | Da error indicando que t no es una unidad valida | Muestra error de unidad no soportada en la CLI |

## Comparacion

| Pregunta | Spec a mano | Spec Kit |
| --- | --- | --- |
| ¿Cubrio los mismos casos borde? | Si, a traves de excepciones de Python | Si, con validaciones directas en la terminal |
| ¿Que creo que no le pedi? | Agrego soporte para onzas y alias de texto | Creo varias carpetas, un contrato CLI, salida JSON y tests |
| ¿Cual fue mas rapido para empezar? | Spec a mano, fue crear un archivo y listo | Spec Kit, tomo mas tiempo por los 4 comandos |
| ¿Cual da mas confianza? | Sirve para probar algo rapido | Spec Kit, porque deja todo mas ordenado y probado |

## Conclusion

La proxima vez que tenga un proyecto de tamaño mediano o grande, elegiria Spec Kit porque organiza mejor el codigo en carpetas; 
Tengo la duda que espero solventar en las siguientes clases, estos specs forman parte de mi codigo en el repositorio para que todos los
futuros desarrolladores lo tengan.. pero 
¿como los organizo para que no interrumpan la visualización limpia de mis archivos de código?
¿como se podran asociar en proyectos medianos un fragmento de codigo /clase /archivo a un spec/historia especifica entre tantos archivos?
