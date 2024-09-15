from fastapi import FastAPI, status, Depends, APIRouter,HTTPException
from fastapi_app.app.database import Session,ENGINE
from fastapi_app.app.models import User,Post
from fastapi_app.app.schemas import PostCreateModel,PostUpdateModel
from fastapi.encoders import jsonable_encoder
session=Session(bind=ENGINE)

router = APIRouter(prefix="/posts",tags=["posts"])

@router.get("/")
async def posts_list():
    posts = session.query(Post).all()
    context = [
        {
            "id": post.id,
            "image_path": post.image_path,
            "caption": post.caption,
            "user_id": post.user_id,
        }
        for post in posts
    ]
    return jsonable_encoder(context)

@router.post('/create')
async def create(post: PostCreateModel):
    check_post = session.query(Post).filter(Post.id == post.id).first()
    if check_post:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bunday post already exists")

    new_post = Post(
        id=post.id,
        caption=post.caption,
        image_path=post.image_path,
    )
    session.add(new_post)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Success created")



@router.get("/{id}")
async def post_detail(id: int):
    post = session.query(Post).filter(Post.id == id).first()
    if post is None:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Post not found")

    data = {
        "caption": post.caption,
        "image_path": post.image_path,

    }
    return jsonable_encoder(data)


@router.put('/{id}')
async def update_post(id: int, data: PostUpdateModel):
    post = session.query(Post).filter(Post.id == id).first()
    if post:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(post, key, value)
        session.commit()
        data = {
            "code": 200,
            "message": "Update post",
            "object":{
                "post caption": post.caption,
                "image_path": post.image_path,
            }
        }
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post is not found")


@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete(id: int):
    post = session.query(Post).filter(Post.id == id).first()
    if post:
        session.delete(post)
        session.commit()
        data = {
            "code": 200,
            "message": f"Deleted with {id} post",
        }
        return jsonable_encoder(data)

    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post is not found")