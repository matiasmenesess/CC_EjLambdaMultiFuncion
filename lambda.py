import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event['tenant_id']
    action = event['action']
    
    # Inicializar DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    if action == 'listar':
        # Listar alumnos
        response = table.query(
            KeyConditionExpression=Key('tenant_id').eq(tenant_id)
        )
        items = response['Items']
        num_reg = response['Count']
        return {
            'statusCode': 200,
            'tenant_id': tenant_id,
            'num_reg': num_reg,
            'alumnos': items
        }

    elif action == 'crear':
        # Crear alumno
        alumno_id = event['alumno_id']
        alumno_datos = event['alumno_datos']
        alumno = {
            'tenant_id': tenant_id,
            'alumno_id': alumno_id,
            'alumno_datos': alumno_datos
        }
        response = table.put_item(Item=alumno)
        return {
            'statusCode': 200,
            'response': response
        }

    elif action == 'modificar':
        # Modificar alumno
        alumno_id = event['alumno_id']
        alumno_datos = event['alumno_datos']
        response = table.update_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            },
            UpdateExpression="set alumno_datos=:alumno_datos",
            ExpressionAttributeValues={
                ':alumno_datos': alumno_datos
            },
            ReturnValues="UPDATED_NEW"
        )
        return {
            'statusCode': 200,
            'response': response
        }

    elif action == 'eliminar':
        # Eliminar alumno
        alumno_id = event['alumno_id']
        response = table.delete_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            }
        )
        return {
            'statusCode': 200,
            'response': response
        }

    elif action == 'buscar':
        # Buscar alumno
        alumno_id = event['alumno_id']
        response = table.get_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            }
        )
        return {
            'statusCode': 200,
            'response': response
        }

    else:
        return {
            'statusCode': 400,
            'error': 'Acción no válida'
        }
