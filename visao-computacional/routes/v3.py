import json
from utils.functions import validate_image_info, get_faces_response, get_image_creation_date

def v3_vision(event, context):

    # Recebe o objeto enviado pelo cliente e valida as informações
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
    
    # Cria a lista de rostos detectados com as emoções classificadas
    faces = []
    if not response_faces['FaceDetails']:
        # Adiciona um objeto de rosto vazio com valores nulos
        faces.append({
            "position": {
                "Height": None,
                "Left": None,
                "Top": None,
                "Width": None
            },
            "classified_emotion": None,
            "classified_emotion_confidence": None
        })
    else:
        for face in response_faces['FaceDetails']:
            highest_emotion = max(face['Emotions'], key=lambda e: e['Confidence'])
            faces.append({
                "position": {
                    "Height": face['BoundingBox']['Height'],
                    "Left": face['BoundingBox']['Left'],
                    "Top": face['BoundingBox']['Top'],
                    "Width": face['BoundingBox']['Width']
                },
                "classified_emotion": highest_emotion['Type'],
                "classified_emotion_confidence": highest_emotion['Confidence']
            })

    # Cria o objeto de resposta
    response_data = {
        "url_to_image": f"https://{bucket}.s3.amazonaws.com/{image_name}",
        "created_image": get_image_creation_date(bucket, image_name),
        "faces": faces
    }

    # Mostra a resposta no CloudWatch:
    print("RETURN:", json.dumps(response_data))

    # Retorna resposta com sucesso
    return {
        "statusCode": 200,
        "body": json.dumps(response_data)
    }