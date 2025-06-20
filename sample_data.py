# sample_data.py
# Sample data for the lawyer portfolio application

import os

# Lawyer information (single record - there will always be only one)
LAWYER_DATA = {
    "name": "Simone Persin Côrtes",
    "title": "Advogada Especialista em Direito Civil e Empresarial",
    "description": "Com mais de 10 anos de experiência, Simone Persin Côrtes é uma advogada dedicada e comprometida em oferecer soluções jurídicas eficazes para seus clientes. Especializada em Direito Civil e Empresarial, atua com foco na resolução de conflitos e na prevenção de litígios.",
    "phone": "(16) 99999-9999",
    "email": "simone.cortes@advocacia.com",
    "address": "R. Treze de Maio, 1845 - sala 4 - Jardim São Carlos, São Carlos - SP, 13561-207",
    "lat": -22.018446353844716,
    "lng": -47.89211584565878,
    "profile_image": "lawyer-hero.jpg",
}

# Google Maps Place ID for reviews integration - Load from environment variable
GOOGLE_PLACE_ID = os.getenv("GOOGLE_PLACE_ID")

# Services offered (multiple records)
SERVICES_DATA = [
    {
        "title": "Direito Civil",
        "description": "Contratos, responsabilidade civil, direito de família e sucessões. Assessoria completa em questões civis.",
        "icon": "fas fa-home",
    },
    {
        "title": "Direito Empresarial",
        "description": "Constituição de empresas, contratos comerciais e consultoria empresarial. Suporte jurídico para seu negócio.",
        "icon": "fas fa-briefcase",
    },
    {
        "title": "Direito do Consumidor",
        "description": "Defesa dos direitos do consumidor, resolução de conflitos e reparação de danos. Proteção aos seus interesses.",
        "icon": "fas fa-shopping-cart",
    },
    {
        "title": "Direito Trabalhista",
        "description": "Assessoria em relações trabalhistas, rescisões e direitos do trabalhador. Expertise em legislação trabalhista.",
        "icon": "fas fa-users",
    },
]

# About Us items (multiple records)
ABOUT_DATA = [
    {
        "title": "Nossa Missão",
        "description": "Oferecer soluções jurídicas eficazes e personalizadas, sempre priorizando a transparência, ética e o melhor interesse de nossos clientes.",
        "icon": "fas fa-bullseye",
    },
    {
        "title": "Nossa Visão",
        "description": "Ser reconhecido como um escritório de advocacia de referência, construindo relacionamentos duradouros baseados na confiança e excelência.",
        "icon": "fas fa-eye",
    },
    {
        "title": "Nossos Valores",
        "description": "Comprometimento, integridade, responsabilidade e dedicação em cada caso, sempre buscando a justiça e a defesa dos direitos de nossos clientes.",
        "icon": "fas fa-heart",
    },
]
