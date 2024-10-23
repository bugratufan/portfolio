import os
import markdown2
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from datetime import datetime
import re

def parse_markdown(md_text):
    # Metadata ve içerik arasında ayrım yapmak için regex kullanımı
    meta_regex = r'^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)'
    match = re.match(meta_regex, md_text, re.MULTILINE)
    
    if not match:
        return {
            'error': 'Metadata not found or improper format',
            'content': markdown2.markdown(md_text)  # Markdown içeriği hala döndürülür ama meta veri bulunamadı
        }
    
    meta_block, content = match.groups()
    
    meta_data = {}
    for line in meta_block.strip().split('\n'):
        key_value = line.split(':', 1)
        if len(key_value) == 2:
            key, value = key_value
            meta_data[key.strip().lower()] = value.strip()

    html_content = markdown2.markdown(content)
    
    return {
        'author': meta_data.get('author', 'No author specified'),
        'date': meta_data.get('date', 'No date specified'),
        'title': meta_data.get('title', 'No title specified'),
        'description': meta_data.get('description', 'No description specified'),
        'categories': meta_data.get('categories', 'No categories specified'),
        'header_img': 'markdowns/' + meta_data.get('header_img', 'No header image specified'),
        'content': html_content
    }

def list_blogs(request):
    category_filter = request.GET.get('category', None)  

    blog_directory = os.path.join(settings.BASE_DIR, 'static', 'markdowns')
    blogs = []

    for folder in os.listdir(blog_directory):
        files = os.listdir(os.path.join(blog_directory, folder))
        filename = next((f for f in files if f.endswith('.md')), None)
        if not filename:
            continue
        filepath = os.path.join(blog_directory, folder, filename)
        with open(filepath, 'r') as file:
            md_text = file.read()
            parsed_md = parse_markdown(md_text)
            blog_categories = [category.strip() for category in parsed_md['categories'].split(',')]
                
            if category_filter and category_filter not in blog_categories:
                continue  
            blogs.append({
                'filename': filename.replace('.md', ''),
                'title': parsed_md['title'],
                'description': parsed_md['description'],
                'author': parsed_md['author'],
                'content': parsed_md['content'],
                'creation_date': parsed_md['date'],
                'header_img': parsed_md['header_img'],
                'categories': [category.strip() for category in parsed_md['categories'].split(',')]
            })
    return render(request, 'list_blogs.html', {'blogs': blogs})

def blog_detail(request, filename):
    category_filter = request.GET.get('category', None)  
    blogs = get_blogs(category_filter)

    blog = next((blog for blog in blogs if blog['filename'] == filename), None)
    return render(request, 'blog_detail.html', {
        'content': blog['content'],
        'blog_list': blogs
    })

def get_blogs(category_filter):
    blog_directory = os.path.join(settings.BASE_DIR, 'static', 'markdowns')
    blogs = []
    for folder in os.listdir(blog_directory):
        print(folder)
        files = os.listdir(os.path.join(blog_directory, folder))
        filename = next((f for f in files if f.endswith('.md')), None)
        if not filename:
            continue
        filepath = os.path.join(blog_directory, folder, filename)
        with open(filepath, 'r') as file:
            md_text = file.read()
            parsed_md = parse_markdown(md_text)
            blog_categories = [category.strip() for category in parsed_md['categories'].split(',')]
            blogs.append({
                'filename': filename.replace('.md', ''),
                'title': parsed_md['title'],
                'description': parsed_md['description'],
                'author': parsed_md['author'],
                'content': parsed_md['content'],
                'creation_date': parsed_md['date'],
                'header_img': parsed_md['header_img'],
                'categories': [category.strip() for category in parsed_md['categories'].split(',')]
            })
    return blogs

def home(request):
    return render(request, 'home.html')


def projects(request):
    category = request.GET.get('category')  # Kategori parametresini alıyoruz

    projects = [
        # Örnek projeler
        {
            'title': 'Custom VHDL Module Development',
            'description': 'Developed custom VHDL modules tailored for specific functionalities.',
            'team_member': 'Bugra Tufan',
            'categories': ['Embedded', 'Hardware'],
        },
        {
            'title': 'Automated Driving Software Development',
            'description': 'Developed software for Level-4 automated buses.',
            'team_member': 'Orcun Can Deniz',
            'categories': ['Software', 'AI'],
        },
        {
            'title': 'High-Power Mainboard Design',
            'description': 'Designed high-power mainboards with a focus on EMI & EMC.',
            'team_member': 'Eyüp Erdem Erbil',
            'categories': ['Hardware', 'PCB'],
        },
        # Diğer projeler...
    ]

    # Eğer kategori parametresi varsa, projeleri filtreliyoruz
    if category:
        projects = [project for project in projects if category in project['categories']]

    return render(request, 'projects.html', {'projects': projects})

# portfolio_app/views.py

def services(request):
    services = [
        {
            'title': 'Embedded Systems Development',
            'description': 'Custom embedded systems solutions including FPGA development and microprocessor integration.',
            'category': 'Embedded',
            'team_member': 'Bugra Tufan',
            'email': 'bugra@example.com',
        },
        {
            'title': 'Software Development',
            'description': 'Advanced software solutions with expertise in machine learning, GPU programming, and autonomous systems.',
            'category': 'Software',
            'team_member': 'Orcun Can Deniz',
            'email': 'orcun@example.com',
        },
        {
            'title': 'PCB Design and Hardware Development',
            'description': 'High-quality PCB design, signal integrity analysis, and hardware development services.',
            'category': 'Hardware',
            'team_member': 'Eyüp Erdem Erbil',
            'email': 'eyup@example.com',
        },
        {
            'title': 'Consultancy Services',
            'description': 'Expert consultancy in hardware design, embedded systems, and software development.',
            'category': 'Consultancy',
            'team_member': 'All',
            'email': 'info@menger.de',
        },
    ]
    return render(request, 'services.html', {'services': services})


