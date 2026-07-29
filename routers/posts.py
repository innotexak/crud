from typing import Optional
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId

from database import post_collection
from schemas.post import PostModel, EditPostModel

router = APIRouter(
    prefix="/api/posts",
    tags=["Posts"]
)

# Helper function to validate MongoDB ObjectIds
def parse_object_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid MongoDB ObjectId format"
        )


@router.get("")
async def get_posts(skip: int = 0, limit: int = 10, published: Optional[bool] = None):
    query = {}
    if published is not None:
        query["published"] = published

    posts = await post_collection.find(query).skip(skip).limit(limit).to_list(length=limit)
    for post in posts:
        post["_id"] = str(post["_id"])
    return posts


@router.get("/{post_id}")
async def get_single_post(post_id: str):
    object_id = parse_object_id(post_id)
    post = await post_collection.find_one({"_id": object_id})
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
    post["_id"] = str(post["_id"])
    return post


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostModel):
    new_post = post.model_dump()
    result = await post_collection.insert_one(new_post)
    new_post["_id"] = str(result.inserted_id)
    return new_post


@router.patch("/{post_id}")
async def update_post(post_id: str, update: EditPostModel):
    object_id = parse_object_id(post_id)
    update_data = update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided to update")

    result = await post_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return {"message": "Post updated successfully", "modified_count": result.modified_count}


@router.delete("/{post_id}")
async def delete_post(post_id: str):
    object_id = parse_object_id(post_id)
    deleted_result = await post_collection.find_one_and_delete({"_id": object_id})
    
    if not deleted_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return {"message": f"Post with ID '{post_id}' deleted successfully"}