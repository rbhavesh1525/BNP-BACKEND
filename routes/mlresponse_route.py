from fastapi import APIRouter
from schemas.ml_response import MLResponseSchema
from Services.save_ml_response import save_model_response

router = APIRouter()

@router.post("/save-response")
def save_response(data: MLResponseSchema):
    data_dict = data.dict()
    response = save_model_response(data_dict)
    return {"status": "success", "data": response.data}
