import os
import boto3
import csv
import pymysql

# Configuración de AWS
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

# Configuración de la base de datos MySQL
db_host = 'globant-instances-db.cqq8rjza2a46.us-east-1.rds.amazonaws.com'
db_user = 'admin'
db_password = 'Alex203011'
db_name = 'globanttest'

def is_numeric(value):
    return value.isdigit()

def get_column_data_types(cursor, table_name):
    # Obtener los tipos de datos de las columnas de la tabla
    column_data_types = {}
    query = f"DESCRIBE `{table_name}`;"
    cursor.execute(query)
    for column_info in cursor.fetchall():
        column_name = column_info[0]
        data_type = column_info[1]
        column_data_types[column_name] = data_type
    return column_data_types

def lambda_handler(event, context):
    # Obtener la lista de objetos en el bucket S3 y carpeta "globant-files"
    bucket_name = 'globant-files'
    # Almacenar los valores no insertados
    valores_no_insertados = []
    
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    

    if 'Contents' in response:
        for file_info in response['Contents']:
            file_key = file_info['Key']
            file_name = os.path.basename(file_key)

            # Verificar si es un archivo CSV
            if file_name.endswith('.csv'):
                
                folder_name = file_name[:-4]  # Eliminar la extensión ".csv" para obtener el nombre de la subcarpeta
                # Asegurarse de que el nombre de la tabla sea válido (solo caracteres alfanuméricos y guiones bajos)
                table_name = folder_name.replace('-', '')
                
                # Obtener el contenido del archivo CSV
                csv_content = s3_client.get_object(Bucket=bucket_name, Key=file_key)['Body'].read().decode('utf-8')

                # Procesar el archivo CSV y cargar los registros en la base de datos
                try:
                    
                    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
                    cursor = connection.cursor()

                    csv_reader = csv.reader(csv_content.splitlines())
                    column_names = next(csv_reader)  # Saltar la primera fila si contiene encabezados

                    # Obtener los tipos de datos de las columnas de la tabla
                    column_data_types = get_column_data_types(cursor, table_name)

                    for fila in csv_reader:
                        valores = []
                        for valor in fila:
                            valor = valor.strip()
                            if valor.isdigit():
                                valores.append(valor)
                            else:
                                valores.append(f"'{valor}'")
                        # Construir la sentencia INSERT
                        sentencia_insert = f"INSERT INTO {table_name} VALUES ({', '.join(valores)});"
                        print(sentencia_insert)  # Opcional, para ver las sentencias generadas
                        try:
                            # Ejecutar la sentencia INSERT en la base de datos
                            cursor.execute(sentencia_insert)
                        except pymysql.Error as e:
                            valores_no_insertados.append(fila)

                    
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    
                    # Almacenar los valores no insertados en un nuevo archivo CSV en S3
                    if len(valores_no_insertados) > 0:
                        csv_content_failed = "\n".join([",".join(fila) for fila in valores_no_insertados])
                        failed_data_key = f"{file_name[:-4]}_failed.csv"
                        s3_client.put_object(Bucket='globant-files-error', Key=failed_data_key, Body=csv_content_failed)


                    # Mover el archivo a la carpeta "globant-files-post-stage"
                    target_bucket_name = 'globant-files-post-stage'
                    target_key = f'{folder_name}/{file_name}'
                    s3_resource.Object(target_bucket_name, target_key).copy_from(CopySource={'Bucket': bucket_name, 'Key': file_key})
                    s3_resource.Object(bucket_name, file_key).delete()
                    
                except Exception as e:
                    print(f"Error: {e}")
                    # Puedes implementar un manejo de errores más detallado si es necesario

    return {
        'statusCode': 200,
        'body': 'Proceso completado exitosamente.'
    }
