from django.shortcuts import render, redirect
from blogtool.forms import AddBlogPostForm,GitHubAccessTokenForm,EditBlogPostForm
from .models import Ghat,BlogPost
import pybase64
from PIL import Image
import requests 
import json
import re
import base64
import cv2
# funcs
def add_blog_post(post_title, post_text, card_title, card_caption, post_image = None, card_image = None):
    obj = Ghat.objects.all().first()
    github_access_token = obj.ghat
    post_img_path = ""
    card_img_path = ""
    # func for uploading image
    def upload_img(github_access_token, image, title):
        print(image)
        encoded_img = pybase64.b64encode(image.read())
        image = encoded_img.decode("utf-8")
        
        headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {github_access_token}',
    'X-GitHub-Api-Version': '2022-11-28',
    'Content-Type': 'application/x-www-form-urlencoded',
}

        data = {"message":f"Uploaded blog post image for {title}","content":f'{image}'}
        data = json.dumps(data)
        request = requests.put(f'https://api.github.com/repos/parkit-smith/parkit/contents/assets/imgs/{title}.png', headers=headers,data=data)
        print(request.text)
        return
    # func for uploading html file
    def upload_html(github_access_token, html_text, title, blog, research):
        html_file = pybase64.b64encode(html_text.encode("ascii"))
        html_file = html_file.decode("utf-8")
    
        headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {github_access_token}',
    'X-GitHub-Api-Version': '2022-11-28',
    'Content-Type': 'application/x-www-form-urlencoded',
}

        if blog:
            data = {"message":f"Uploaded blog post html for {title} blog post","content":f'{html_file}'}
            data = json.dumps(data)
            request = requests.put(f'https://api.github.com/repos/parkit-smith/parkit/contents/blog_posts/{title}.html', headers=headers,data=data)
            print(request.text)
            return
        elif research:
            # delete current research.html
            headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {github_access_token}',
    'X-GitHub-Api-Version': '2022-11-28',
}
            response = requests.get('https://api.github.com/repos/parkit-smith/parkit/contents/research.html', headers=headers)
            sha = response.json()['sha']
            # replace with new
            data = {"message":f"Updated research.html for {title} blog card","content":f'{html_file}',"sha":f'{sha}'}
            data = json.dumps(data)
            request = requests.put(f'https://api.github.com/repos/parkit-smith/parkit/contents/research.html', headers=headers,data=data)
            print(request.text)
            return
    # func for uploading new card
    def create_card_html(github_access_token, title, caption, post_title, image_path=""):
        headers = {
    'Accept': 'application/vnd.github.raw',
    'Authorization': f'Bearer {github_access_token}',
    'X-GitHub-Api-Version': '2022-11-28',
}
        new_card = '''\
                <div class="col-md-4">
                    <div class="card blog-post my-4 my-sm-5 my-md-0">
            <!-- ADD BLOG POST IMAGE IN LINE BELOW-->
                        <img src="{image_path}">
                        <div class="card-body">
            <!-- ADD BLOG POST TITLE IN LINE BELOW -->
                            <h5 class="card-title">{title}</h5>
                <!-- ADD BLOG POST DESCRIPTION IN LINE BELOW -->
                            <p>{caption}</p>
                            <a href="blog_posts/{post_title}.html" style="color:#000000 !important;">Read More...</a>
                        </div>
                    </div>
                </div>
'''.format(image_path=image_path,title=title,caption=caption, post_title=post_title)
        request = requests.get("https://api.github.com/repos/parkit-smith/parkit/contents/research.html", headers=headers)
        request_text = request.text
        start_index = re.search("<!-- ADD NEW POST HERE -->", request_text).start()
        updated_html = request_text[:start_index-6] + new_card + request_text[start_index-6:]
        return updated_html


    # check to see if there are images and upload to assets folder
    if post_image:
        upload_img(github_access_token,post_image,post_title)
        post_img_path = f"assets/imgs/{post_title}.png"
    if card_image:
        upload_img(github_access_token,card_image,card_title)
    
    
    
    blog_post_html = '''\
<!DOCTYPE html>
<html lang="en">
<head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
    <script src="assets/vendors/jquery/my-js.js"></script>
	<meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="Start your development with Creative Studio landing page.">
    <meta name="author" content="Devcrud">
    <title>ParKit@Smith</title>

    <!-- font icons -->
    <link rel="stylesheet" href="assets/vendors/themify-icons/css/themify-icons.css">

    <!-- Bootstrap + Creative Studio + Fonts main styles -->
	<link rel="stylesheet" href="assets/css/website.css">
    <style> @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=block');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800&display=block');
    </style>
</head>
<body data-spy="scroll" data-target=".navbar" data-offset="40" id="home">
    
    <!-- Page Navigation -->
    <nav class="navbar custom-navbar navbar-expand-lg navbar-dark" data-spy="affix" data-offset-top="20">
        <div class="container">
            <a class="navbar-brand" href="#">
                <img src="assets/imgs/logo_parkit.png" alt="Download free bootstrap 4 landing page, free boootstrap 4 templates, Download free bootstrap 4.1 landing page, free boootstrap 4.1.1 templates, Creative studio Landing page">
            </a>
            <div class="logo" id="logo">ParKit@Smith</div>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="index.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <div class="dropdown">
                            <a class="nav-link" href="#">About</a>
                            <div class="dropdown-content">
                                <a href="our-project.html">Our Project</a>
                                <a href="our-team.html">Our Team</a>
                                <a href="instructables.html">Our Instructables</a>
                            </div>
                        </div>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="research.html">Research</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="gallery.html">Gallery</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="events.html">Events</a>
                    </li>          
                    <li class="nav-item">
                        <a class="nav-link btn btn-primary btn-sm ml-lg-3" href="Contact.html">Contact Us</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <!-- End Of Page Navigation -->

    <!-- Page Header -->
    <header class="page-header">
        <div class="page-overlay">
            <!-- ADD YOUR BLOG POST TITLE IN THE LINE BELOW -->
            <h1 class="page-title" style="text-align: center;">{post_title}</h1>         
        </div>      
    </header>
    <!-- End Of Page Header -->


    <!-- Blog Post Section -->
    <section id="about">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-7 col-lg-8">
                    <!-- ADD YOUR TEXT BELOW -->
                    {post_text}
                </div>
                <div class="col-md-5 col-lg-4">
                    <!-- ADD AN IMAGE IN THE LINE BELOW. REMEMBER TO UPLOAD IT TO OUR IMAGES FOLDER FIRST! GO TO ASSETS > IMGS AND THEN UPLOAD IMAGE -->
                    <img src="{post_img_path}" alt="Download free bootstrap 4 landing page, free boootstrap 4 templates, Download free bootstrap 4.1 landing page, free boootstrap 4.1.1 templates, Creative studio Landing page" class="w-100 img-thumbnail mb-3">
                </div>
            </div>
        </div>
    </section>
    <!-- End of Blog Post Section -->

    <!-- Footer Section -->
    <section class="has-bg-img py-0">
        <div class="container">
            <div class="footer">
                <div class="footer-lists">
                    <ul class="list">
                        <li class="list-head">
                            <h6 class="font-weight-bold">ABOUT US</h6>
                        </li>
                        <li class="list-body">
                            <a href="#" class="logo">
                                <img src="assets/imgs/logo_parkit.png" alt="Download free bootstrap 4 landing page, free boootstrap 4 templates, Download free bootstrap 4.1 landing page, free boootstrap 4.1.1 templates, Creative studio Landing page">
                                <h6>PARKIT@SMITH</h6>
                            </a>
                            <p>A bike-towed, park-making kit that makes small, temporary parks mobile. Designed and maintained by Professor Reid Bertone-Johnson and his research team at Smith College.</p> 
                            <p class="mt-3">
                                Copyright <script>document.write(new Date().getFullYear())</script> &copy; <a class="d-inline text-primary" href="mailto:lledwards@smith.edu" style="color:#A3C14A !important;">Laura Edwards</a>
                            </p>                   
                        </li>
                    </ul>
                    <ul class="list">
                        <li class="list-head">
                            <h6 class="font-weight-bold">USEFUL LINKS</h6>
                        </li>
                        <li class="list-body">
                            <div class="row">
                                <div class="col" style="background-color:#2a2e32;">
                                    <a href="project.html">Our Project</a>
                                    <a href="team.html">Our Team</a>
                                    <a href="instructables.html">Our Instructables</a>
                                    <a href="research.html">Our Research</a>
                                </div>
                                <div class="col" style="background-color:#2a2e32;">
                                    <a href="gallery.html">Our Gallery</a>
                                    <a href="events.html">Our Events</a>                 
                                </div>
                            </div>
                        </li>
                    </ul>
                    <ul class="list">
                        <li class="list-head">
                            <h6 class="font-weight-bold">CONTACT INFO</h6>
                        </li>
                        <li class="list-body">
                            <p>Contact us and we'll get back to you within 3 business days.</p>
                            <p><i class="ti-location-pin"></i> Smith College, Northampton, MA, 01063</p>
                            <p><i class="ti-email"></i> parkit@smith.edu </p>
                            <div class="social-links">
                                <a href="javascript:void(0)" class="link"><i class="ti-facebook"></i></a>
                                <a href="javascript:void(0)" class="link"><i class="ti-twitter-alt"></i></a>
                                <a href="javascript:void(0)" class="link"><i class="ti-google"></i></a>
                                <a href="javascript:void(0)" class="link"><i class="ti-pinterest-alt"></i></a>
                                <a href="javascript:void(0)" class="link"><i class="ti-instagram"></i></a>
                                <a href="javascript:void(0)" class="link"><i class="ti-rss"></i></a>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>    
        </div>
    </section>

    <!-- core  -->
    <script src="assets/vendors/jquery/jquery-3.4.1.js"></script>
    <script src="assets/vendors/bootstrap/bootstrap.bundle.js"></script>

    <!-- bootstrap affix -->
    <script src="assets/vendors/bootstrap/bootstrap.affix.js"></script>

    <!-- Creative Studio js -->
    <script src="assets/js/creative-studio.js"></script>

</body>
</html>
'''.format(post_title=post_title,post_img_path=post_img_path,post_text=post_text)
    upload_html(github_access_token=github_access_token, html_text = blog_post_html, title = post_title,blog=True,research=False)
    updated_research_html = create_card_html(github_access_token=github_access_token,title=card_title,caption=card_caption,post_title=post_title)
    upload_html(github_access_token=github_access_token, html_text = updated_research_html, title = card_title,blog=False,research=True)
    return

def edit_blog_post(post_title, post_text, card_title, card_caption, old_post_title, old_card_title, old_card_caption, blog_post_image_read = "", blog_card_image_read="", old_card_image = None, post_image = None, card_image = None):
    obj = Ghat.objects.all().first()
    github_access_token = obj.ghat
    post_img_path=""
    card_img_path=""
    if old_card_image:
        old_card_image_path = f"assets/imgs/{old_card_title}.png"
    else:
        old_card_image_path = ""
    # func to delete current files
    def get_sha(github_access_token,path):
        headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {github_access_token}',
    'X-GitHub-Api-Version': '2022-11-28',
}
        response = requests.get(f'https://api.github.com/repos/parkit-smith/parkit/contents/{path}', headers=headers)
        try:
            sha = response.json()['sha']
            return sha
        except:
            return False
    # func for uploading image
    def edit_upload_img(github_access_token, image_read, title):
        path = f"assets/imgs/{title}.png"
        # returns sha or False
        sha_status = get_sha(github_access_token=github_access_token,path=path)
        encoded_img = pybase64.b64encode(image_read)
        image = encoded_img.decode("utf-8")
        print(image)
        
        headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {github_access_token}',
    'X-GitHub-Api-Version': '2022-11-28',
    'Content-Type': 'application/x-www-form-urlencoded',
}

        if sha_status:
            data = {"message":f"Uploaded blog post image for {title}","content":f'{image}', 'sha': f'{sha_status}'}
            data = json.dumps(data)
            request = requests.put(f'https://api.github.com/repos/parkit-smith/parkit/contents/assets/imgs/{title}.png', headers=headers,data=data)
            print(request.text)
            return
        if not sha_status:
            data = {"message":f"Uploaded blog post image for {title}","content":f'{image}'}
            data = json.dumps(data)
            request = requests.put(f'https://api.github.com/repos/parkit-smith/parkit/contents/assets/imgs/{title}.png', headers=headers,data=data)
            print(request.text)
            return
    # func for uploading html file
    def edit_upload_html(github_access_token, html_text, title, blog, research):
        html_file = pybase64.b64encode(html_text.encode("ascii"))
        html_file = html_file.decode("utf-8")
    
        headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {github_access_token}',
    'X-GitHub-Api-Version': '2022-11-28',
    'Content-Type': 'application/x-www-form-urlencoded',
}

        if blog:
            path = f"blog_posts/{title}.html"
            sha = get_sha(github_access_token=github_access_token,path=path)
            data = {"message":f"Uploaded blog post html for {title} blog post","content":f'{html_file}', 'sha': f'{sha}'}
            data = json.dumps(data)
            request = requests.put(f'https://api.github.com/repos/parkit-smith/parkit/contents/blog_posts/{title}.html', headers=headers,data=data)
            print(request.text)
            return
        elif research:
            path = "research.html"
            sha = get_sha(github_access_token=github_access_token,path=path)
            data = {"message":f"Updated research.html for {title} blog card","content":f'{html_file}',"sha":f'{sha}'}
            data = json.dumps(data)
            request = requests.put(f'https://api.github.com/repos/parkit-smith/parkit/contents/research.html', headers=headers,data=data)
            print(request.text)
            return
     # check to see if there are images and upload to assets folder
    if post_image:
        edit_upload_img(github_access_token,blog_post_image_read,post_title)
        post_img_path = f"assets/imgs/{post_title}.png"
    if card_image:
        edit_upload_img(github_access_token,blog_card_image_read,card_title)
        card_img_path = f"assets/imgs/{card_title}.png"

    # func for uploading new card
    def edit_create_card_html(github_access_token, title, caption, post_title, old_post_title=old_post_title, old_title=old_card_title, old_caption=old_card_caption, old_image_path="", image_path=""):
        headers = {
    'Accept': 'application/vnd.github.raw',
    'Authorization': f'Bearer {github_access_token}',
    'X-GitHub-Api-Version': '2022-11-28',
}
        old_card = """                <div class="col-md-4">
                    <div class="card blog-post my-4 my-sm-5 my-md-0">
            <!-- ADD BLOG POST IMAGE IN LINE BELOW-->
                        <img src="{old_image_path}">
                        <div class="card-body">
            <!-- ADD BLOG POST TITLE IN LINE BELOW -->
                            <h5 class="card-title">{old_title}<\/h5>
                <!-- ADD BLOG POST DESCRIPTION IN LINE BELOW -->
                            <p>{old_caption}<\/p>
                            <a href="blog_posts\/{old_post_title}.html" style="color:#000000 !important;">Read More...<\/a>
                        <\/div>
                    <\/div>
                <\/div>""".format(old_image_path=old_image_path,old_title=old_title,old_caption=old_caption, old_post_title=old_post_title)
        new_card = '''\
                <div class="col-md-4">
                    <div class="card blog-post my-4 my-sm-5 my-md-0">
            <!-- ADD BLOG POST IMAGE IN LINE BELOW-->
                        <img src="{image_path}">
                        <div class="card-body">
            <!-- ADD BLOG POST TITLE IN LINE BELOW -->
                            <h5 class="card-title">{title}</h5>
                <!-- ADD BLOG POST DESCRIPTION IN LINE BELOW -->
                            <p>{caption}</p>
                            <a href="blog_posts/{post_title}.html" style="color:#000000 !important;">Read More...</a>
                        </div>
                    </div>
                </div>
'''.format(image_path=image_path,title=title,caption=caption, post_title=post_title)
        response = requests.get('https://api.github.com/repos/parkit-smith/parkit/contents/research.html', headers=headers)
        start = re.search(old_card, response.text).start()
        end = re.search(old_card, response.text).end()
        response_text_new = response.text[:start+1] + response.text[end+1:]
        start_index = re.search("<!-- ADD NEW POST HERE -->", response_text_new).start()
        updated_html = response_text_new[:start_index-6] + new_card + response_text_new[start_index-6:]
        return updated_html

    
    
    
    blog_post_html = '''\
<!DOCTYPE html>
<html lang="en">
<head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
    <script src="assets/vendors/jquery/my-js.js"></script>
	<meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="Start your development with Creative Studio landing page.">
    <meta name="author" content="Devcrud">
    <title>ParKit@Smith</title>

    <!-- font icons -->
    <link rel="stylesheet" href="assets/vendors/themify-icons/css/themify-icons.css">

    <!-- Bootstrap + Creative Studio + Fonts main styles -->
	<link rel="stylesheet" href="assets/css/website.css">
    <style> @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=block');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800&display=block');
    </style>
</head>
<body data-spy="scroll" data-target=".navbar" data-offset="40" id="home">
    
    <!-- Page Navigation -->
    <nav class="navbar custom-navbar navbar-expand-lg navbar-dark" data-spy="affix" data-offset-top="20">
        <div class="container">
            <a class="navbar-brand" href="#">
                <img src="assets/imgs/logo_parkit.png" alt="Download free bootstrap 4 landing page, free boootstrap 4 templates, Download free bootstrap 4.1 landing page, free boootstrap 4.1.1 templates, Creative studio Landing page">
            </a>
            <div class="logo" id="logo">ParKit@Smith</div>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="index.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <div class="dropdown">
                            <a class="nav-link" href="#">About</a>
                            <div class="dropdown-content">
                                <a href="our-project.html">Our Project</a>
                                <a href="our-team.html">Our Team</a>
                                <a href="instructables.html">Our Instructables</a>
                            </div>
                        </div>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="research.html">Research</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="gallery.html">Gallery</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="events.html">Events</a>
                    </li>          
                    <li class="nav-item">
                        <a class="nav-link btn btn-primary btn-sm ml-lg-3" href="Contact.html">Contact Us</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <!-- End Of Page Navigation -->

    <!-- Page Header -->
    <header class="page-header">
        <div class="page-overlay">
            <!-- ADD YOUR BLOG POST TITLE IN THE LINE BELOW -->
            <h1 class="page-title" style="text-align: center;">{post_title}</h1>         
        </div>      
    </header>
    <!-- End Of Page Header -->


    <!-- Blog Post Section -->
    <section id="about">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-7 col-lg-8">
                    <!-- ADD YOUR TEXT BELOW -->
                    {post_text}
                </div>
                <div class="col-md-5 col-lg-4">
                    <!-- ADD AN IMAGE IN THE LINE BELOW. REMEMBER TO UPLOAD IT TO OUR IMAGES FOLDER FIRST! GO TO ASSETS > IMGS AND THEN UPLOAD IMAGE -->
                    <img src="{post_img_path}" alt="Download free bootstrap 4 landing page, free boootstrap 4 templates, Download free bootstrap 4.1 landing page, free boootstrap 4.1.1 templates, Creative studio Landing page" class="w-100 img-thumbnail mb-3">
                </div>
            </div>
        </div>
    </section>
    <!-- End of Blog Post Section -->

    <!-- Footer Section -->
    <section class="has-bg-img py-0">
        <div class="container">
            <div class="footer">
                <div class="footer-lists">
                    <ul class="list">
                        <li class="list-head">
                            <h6 class="font-weight-bold">ABOUT US</h6>
                        </li>
                        <li class="list-body">
                            <a href="#" class="logo">
                                <img src="assets/imgs/logo_parkit.png" alt="Download free bootstrap 4 landing page, free boootstrap 4 templates, Download free bootstrap 4.1 landing page, free boootstrap 4.1.1 templates, Creative studio Landing page">
                                <h6>PARKIT@SMITH</h6>
                            </a>
                            <p>A bike-towed, park-making kit that makes small, temporary parks mobile. Designed and maintained by Professor Reid Bertone-Johnson and his research team at Smith College.</p> 
                            <p class="mt-3">
                                Copyright <script>document.write(new Date().getFullYear())</script> &copy; <a class="d-inline text-primary" href="mailto:lledwards@smith.edu" style="color:#A3C14A !important;">Laura Edwards</a>
                            </p>                   
                        </li>
                    </ul>
                    <ul class="list">
                        <li class="list-head">
                            <h6 class="font-weight-bold">USEFUL LINKS</h6>
                        </li>
                        <li class="list-body">
                            <div class="row">
                                <div class="col" style="background-color:#2a2e32;">
                                    <a href="project.html">Our Project</a>
                                    <a href="team.html">Our Team</a>
                                    <a href="instructables.html">Our Instructables</a>
                                    <a href="research.html">Our Research</a>
                                </div>
                                <div class="col" style="background-color:#2a2e32;">
                                    <a href="gallery.html">Our Gallery</a>
                                    <a href="events.html">Our Events</a>                 
                                </div>
                            </div>
                        </li>
                    </ul>
                    <ul class="list">
                        <li class="list-head">
                            <h6 class="font-weight-bold">CONTACT INFO</h6>
                        </li>
                        <li class="list-body">
                            <p>Contact us and we'll get back to you within 3 business days.</p>
                            <p><i class="ti-location-pin"></i> Smith College, Northampton, MA, 01063</p>
                            <p><i class="ti-email"></i> parkit@smith.edu </p>
                            <div class="social-links">
                                <a href="javascript:void(0)" class="link"><i class="ti-facebook"></i></a>
                                <a href="javascript:void(0)" class="link"><i class="ti-twitter-alt"></i></a>
                                <a href="javascript:void(0)" class="link"><i class="ti-google"></i></a>
                                <a href="javascript:void(0)" class="link"><i class="ti-pinterest-alt"></i></a>
                                <a href="javascript:void(0)" class="link"><i class="ti-instagram"></i></a>
                                <a href="javascript:void(0)" class="link"><i class="ti-rss"></i></a>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>    
        </div>
    </section>

    <!-- core  -->
    <script src="assets/vendors/jquery/jquery-3.4.1.js"></script>
    <script src="assets/vendors/bootstrap/bootstrap.bundle.js"></script>

    <!-- bootstrap affix -->
    <script src="assets/vendors/bootstrap/bootstrap.affix.js"></script>

    <!-- Creative Studio js -->
    <script src="assets/js/creative-studio.js"></script>

</body>
</html>
'''.format(post_title=post_title,post_img_path=post_img_path,post_text=post_text)
    edit_upload_html(github_access_token=github_access_token, html_text = blog_post_html, title = post_title,blog=True,research=False)
    updated_research_html = edit_create_card_html(github_access_token=github_access_token,title=card_title,caption=card_caption,post_title=post_title,old_image_path=old_card_image_path,image_path=card_img_path)
    edit_upload_html(github_access_token=github_access_token, html_text = updated_research_html, title = card_title,blog=False,research=True)
    return
    

# Create your views here.
def add(request):
    form = AddBlogPostForm()
    context = {
            'form': form
        }
    if request.method == "POST":
        print("method is post!")
        form = AddBlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            print("form is valid!")
            print(form.cleaned_data)
            blog_post_title = form.cleaned_data['blog_post_title']
            blog_post_date = form.cleaned_data['blog_post_date']
            blog_post_image = form.cleaned_data.get('blog_post_image')
            if not blog_post_image:
                blog_post_image = None
            blog_post_text = form.cleaned_data['blog_post_text']
            blog_card_title = form.cleaned_data['blog_card_title']
            blog_card_caption = form.cleaned_data['blog_card_caption']
            blog_card_image = form.cleaned_data.get('blog_card_image')
            if not blog_card_image:
                blog_card_image = None
            add_blog_post(post_title=blog_post_title,post_text=blog_post_text,card_title=blog_card_title,
                        card_caption=blog_card_caption,post_image=blog_post_image,card_image=blog_card_image)
            form.save()
            return redirect('https://parkit-smith.github.io/parkit/')
        else:
            print(form.errors)
    else:
        ghat_form = GitHubAccessTokenForm()
        form = AddBlogPostForm()
        context = {
            'form': form
        }
    return render(request, 'add.html', context)

def edit(request):
    obj = Ghat.objects.all().first()
    github_access_token = obj.ghat
    form = EditBlogPostForm()
    context = {
        'form': form
    }
    if request.method == "POST":
        form = EditBlogPostForm(request.POST)
        if form.is_valid():
            selected_obj = form.cleaned_data['blog_post']
            request.session['blog_post_title_to_edit'] = selected_obj.blog_post_title
            print()
            context = {
                'form':form
            }
            return redirect('blogpost:submit_edit')
        else:
            print(form.errors, "not valid")
    return render(request, 'edit.html', context)

def submit_edit(request):
    blog_post_obj = BlogPost.objects.get(blog_post_title=request.session['blog_post_title_to_edit'])
    form = AddBlogPostForm(instance=blog_post_obj)
    if request.method == "POST":
        form = AddBlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            # get old data
            old_card_caption = blog_post_obj.blog_card_caption
            old_card_title = blog_post_obj.blog_card_title
            old_post_title = blog_post_obj.blog_post_title
            old_card_image = blog_post_obj.blog_card_image
            if not old_card_image:
                old_card_image = None
            submitted_edit = form.save(commit=False)
            # get new data
            blog_post_title = form.cleaned_data['blog_post_title']
            blog_post_date = form.cleaned_data['blog_post_date']
            blog_post_image = form.cleaned_data.get('blog_post_image')
            if blog_post_image:
                blog_post_image_read = blog_post_image.read()
            if not blog_post_image:
                print("no new blog post image!")
                blog_post_image = None
                blog_post_image_read=""
            blog_post_text = form.cleaned_data['blog_post_text']
            blog_card_title = form.cleaned_data['blog_card_title']
            blog_card_caption = form.cleaned_data['blog_card_caption']
            blog_card_image = form.cleaned_data.get('blog_card_image')
            if blog_card_image:
                blog_card_image_read = blog_card_image.read()
            if not blog_card_image:
                print("no new blog card image!")
                blog_card_image = None
                blog_card_image_read=""
            # keep old images if they have been unchanged
            if not form.cleaned_data.get('blog_post_image') and blog_post_obj.blog_post_image:
                blog_post_image = blog_post_obj.blog_post_image
                submitted_edit.blog_post_image = blog_post_image
            if not form.cleaned_data.get('blog_card_image') and blog_post_obj.blog_card_image:
                blog_card_image = blog_post_obj.blog_card_image
                submitted_edit.blog_card_image = blog_card_image
            # delete old instance
            BlogPost.objects.get(blog_post_title=old_post_title).delete()
            submitted_edit.save()
            # do the actual GitHub updating
            edit_blog_post(post_title=blog_post_title,post_text=blog_post_text,
                           card_title=blog_card_title,card_caption=blog_card_caption,
                           old_post_title=old_post_title,old_card_title=old_card_title,
                           old_card_caption=old_card_caption,old_card_image=old_card_image,
                           post_image=blog_post_image,card_image=blog_card_image,blog_post_image_read=blog_post_image_read,
                           blog_card_image_read=blog_card_image_read)
            print("edit_blog_post done!")
            return redirect('https://parkit-smith.github.io/parkit/')
        else:
            form = AddBlogPostForm(instance=blog_post_obj)
    return render(request, 'submit_edit.html', context = {'form':form})