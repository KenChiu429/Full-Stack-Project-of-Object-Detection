from typing import Union
from fastapi import FastAPI, File, HTTPException, UploadFile
import uvicorn
from pydantic import BaseModel
from process_img_tag.process import process_image
from service.crud import delete_file, update_tag
from service.image import upload_image
from service.search import query, query_by_image


app = FastAPI()


class SearchModel(BaseModel):
    tags: Union[list, None] = None
    url: Union[str, None] = None


class UpdateModel(BaseModel):
    type: Union[int, None] = None
    tags: Union[list, None] = None
    url: Union[str, None] = None


class AuthModel(BaseModel):
    username: str
    password: str
    email: str


@app.post("/api/image")
async def upload_file(file: UploadFile):
    suffix = file.filename.split('.')[-1]
    if suffix not in ['jpg', 'png', 'jpeg']:
        raise HTTPException(status_code=400, detail="Please upload pictures.")

    res = upload_image(file.file, suffix)
    if res['isSuccess']:
        return {"message": "Success"}

    raise HTTPException(status_code=400, detail="Upload failed.")


@app.delete("/api/image")
async def delete_image(url: str):
    delete_file(url)
    res = delete_file(url)
    if res:
        return {"message": "Success"}
    raise HTTPException(status_code=400, detail="Delete failed.")


@app.patch("/api/tag")
async def update_tag(model: UpdateModel):
    res = update_tag(model)
    if res:
        return {"message": "Success"}
    raise HTTPException(status_code=400, detail="Update failed.")


@app.post("/api/search/file")
async def upload_file(file: UploadFile):
    tags = await process_image(file)
    print('tags',tags)
    model = SearchModel(tags=list(tags))
    res = query(model)
    return {"message": "Success", "data": res}


@app.post("/api/search")
async def search_tag(model: SearchModel):
    print(model)
    res = query(model)
    return {"message": "Success", "data": res}


if __name__ == "__main__":
    uvicorn.run(app='main:app', host='127.0.0.1', port=9000, reload=True)
