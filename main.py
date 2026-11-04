from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory='templates')

posts = {
    1: {"id": 1, "title": "10월 1째주 주간회의", "content": "회의록 보기"}, 
    2: {"id": 2, "title": "10월 2째주 주간회의", "content": "회의록 보기"},
}

@app.get("/posts")
def post_list(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='list.html',
        context={'posts' : list(posts.values())}
    )

@app.get('/posts/new')
def post_new(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='post.html',
    )

@app.get("/posts/{post_id}")
def post_detail(request: Request, post_id: int):
    post = posts[post_id]
    return templates.TemplateResponse(
        request=request,
        name='detail.html',
        context={'post':post}
    )

#사용자가 넘겨준 데이터를 저장
@app.post('/posts/create')
def post_create(title: str = Form(), content: str = Form()):
    new_id = max(posts.keys())+1
    posts[new_id] = {'id': new_id, 'title': title, 'content': content}

    return RedirectResponse(f'/posts/{new_id}', status_code=303)

@app.get('/posts/{post_id}/edit')
def post_edit(request: Request, post_id: int):
    post = posts[post_id]
    return templates.TemplateResponse(
        request=request,
        name='edit.html',
        context={'post':post}
    )

@app.post('/posts/{post_id}/update')
def post_update(post_id: int, title: str =Form(), content: str =Form()):
    old_post = posts[post_id]

    old_post['title']=title
    old_post['content']=content 

    new_post = old_post
    posts[post_id] = new_post
    return RedirectResponse(f'/posts/{post_id}', status_code=303)

@app.post('/posts/{post_id}/delete')
def post_delete(post_id: int):
    posts.pop(post_id)
    return RedirectResponse('/posts', status_code=303)