# Globanttest

## Se crea en la cuenta de AWS 667783558859 lo siguiente:

### Cargar los archivos en la pagina:http://globant-host-web.s3-website-us-east-1.amazonaws.com/ 
  Esta pagina esta creada para tomar todos los archivos que agreguen y ejecutar el api gateway para transferir estos archivos a un bucket s3: globant-files

### Api Gateway
  Se utiliza para transferir los archivos desde la pagina web hasta un bucket s3 en aws

### Buckets en s3: 
   ##### * globant-files: se usa para recibir los archivos que envia la api.
   ##### * globant-files-error: se usa para guardar los insert que generen error y se pueda ver que informacion quedo sin ingestar en la base de datos.
   ##### * globant-files-post-stage: se usa para guardar los archivos que se fueron ingestando correctamente.
   ##### * globant-host-web: para hospedar los archivos (HTML,CSS, JQUERY) y poder tener una pagina web.

### RDS configurado con Mysql:
  Se configura para insertar los datos.

### Lambda:
  Se utiliza para que una vez se agregue los archivos .csv al bucket de s3, el lambda detecte este evento y pueda pasar los archivos .csv a la base de datos y a los buckets correspondientes (si genero error algun insert en: 
  globant-files-error y los que corrieron bien en globant-files-post-stage).

### Python:
  Se agrega el codigo python usado en el lambda para la ejecucion e insert de los archivos.

### Archivos sql Ejercicio2 :
  Se encuentra las consultas para resolver los enunciados:

    ![image](https://github.com/AlejandroGuedez/Globanttest/assets/69370624/fa5f5443-4567-489b-b33f-3f74daef45fe)

Puntos a mejorar: en el lambda lo mejor seria obtener los datos de la base de datos extraidos por otra funcion y haseada y/o codificada para que no sea de facil  acceso a los datos.

Adicional se crea un crawler para que una vez los archivos esten en globant-files-post-stage se pueda cargar en athena, sin embargo,no se configura eventos para que se dispare automanticamente.
