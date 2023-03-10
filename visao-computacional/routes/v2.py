import json
from utils.functions import validate_image_info, get_faces_response, get_image_creation_date

def v2_vision(event, context):
    
    # Recebe o objeto enviado pelo cliente
    try:
        image_info = json.loads(event['body'])
        bucket, image_name = validate_image_info(image_info)
    except ValueError as e:
        error_message = str(e)
        return {"statusCode": 500, "body": json.dumps({"error": error_message})}

    # Detecta as faces da imagem
    try:
        response_faces = get_faces_response(bucket, image_name)
    except ValueError as e:
        error_message = str(e)
        return {"statusCode": 500, "body": json.dumps({"error": error_message})}
    
    # Cria a lista de faces detectadas
    position_faces = []
    if len(response_faces['FaceDetails']) > 0:
        for face in response_faces['FaceDetails']:
            position_faces.append({
                'Left': face['BoundingBox']['Left'],
                'Top': face['BoundingBox']['Top'],
                'Width': face['BoundingBox']['Width'],
                'Height': face['BoundingBox']['Height']
            })
        have_faces = True
    else:
        have_faces = False

    # Cria a resposta com as informações solicitadas
    response_data = {
        'url_to_image': f"https://{bucket}.s3.amazonaws.com/{image_name}",
        'created_image': get_image_creation_date(bucket, image_name),
        'have_faces': have_faces,
        'position_faces': position_faces if have_faces else None,
    }

    # Mostra a resposta no CloudWatch:
    print("RETURN:", json.dumps(response_data))

    # Retorna a resposta com o código HTTP 200
    return {
        "statusCode": 200,
        "body": json.dumps(response_data)
    }