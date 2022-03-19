import json
from multiprocessing import context
from app import models, schemas

def test_get_all_posts(authorized_client,test_posts):
    res=authorized_client.get('/posts/')
    def validate(post):
        return schemas.PostsOut(**post)

    post_map=map(validate,res.json())
    post_list=list(post_map)
    assert len(res.json())==len(test_posts)
    assert res.status_code==200

def test_unautherized_get_all_posts(client,test_posts):
    res=client.get('/posts/')
    assert res.status_code==401

def test_unautherized_user_get_all_posts(client,test_posts):
    res=client.get(f'/posts/{test_posts[2].id}')
    assert res.status_code==401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404

def test_get_one_post(authorized_client,test_posts):
    res=authorized_client.get(f'/posts/{test_posts[3].id}')
    post=schemas.PostsOut(**res.json())
    assert post.Posts.id==test_posts[3].id
    assert post.Posts.content==test_posts[3].content
    assert post.Posts.title==test_posts[3].title

def test_create_post(authorized_client,test_user,test_posts):
    res= authorized_client.post('/posts/',json={
        'title':'test case title', 'content':'test content'
    })
    created_post=schemas.Posts(**res.json())
    assert res.status_code == 201
    assert created_post.title == "test case title"
    assert created_post.content == "test content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client,test_user,test_posts):
    res= client.post('/posts/',json={
        'title':'test case title', 'content':'test content'
    })
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client,test_user,test_posts):
    res= client.delete(f'/posts/{test_posts[2].id}')
    assert res.status_code == 401

def test_delete_post_success(authorized_client,test_user,test_posts):
    res= authorized_client.delete(f'/posts/{test_posts[2].id}')
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client,test_user,test_posts):
    res= authorized_client.delete('/posts/80989')
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client,test_user,test_posts):
    res= authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert res.status_code == 403

def test_update_post(authorized_client,test_user,test_posts):
    data= {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id
    }
    res=authorized_client.put(f'/posts/{test_posts[0].id}',json=data)
    updated_post=schemas.Posts(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(
        f"/posts/8000000", json=data)

    assert res.status_code == 404