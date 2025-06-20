# Portfólio Jurídico - Simone Persin Côrtes

Este é um portfólio profissional desenvolvido em Python Flask para a advogada Simone Persin Côrtes. O site inclui um sistema de gerenciamento de conteúdo fácil de usar, integração com WhatsApp, geolocalização e avaliações de clientes.

## Características

- **Design Profissional**: Interface moderna e responsiva
- **Integração WhatsApp**: Link direto para contato via WhatsApp
- **Geolocalização**: Mapa interativo com localização do escritório
- **Sistema de Avaliações**: Integração com Google Reviews + avaliações manuais
- **Painel Administrativo**: Interface fácil para gerenciar conteúdo
- **Idioma**: Completamente em português brasileiro
- **Responsivo**: Funciona perfeitamente em dispositivos móveis
- **Seguro**: Configuração via variáveis de ambiente

---

## INÍCIO RÁPIDO

### Método Mais Fácil (Recomendado):
```bash
./start.sh
```
*Este script faz tudo automaticamente: cria ambiente virtual, instala dependências e inicia o servidor*

### Método Manual:
```bash
# 1. Crie um ambiente virtual (primeira vez apenas)
python3 -m venv venv

# 2. Ative o ambiente virtual
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o projeto
python3 app.py
```

### Acessar o Site

Após executar, abra seu navegador e acesse:

- **Portfólio Principal**: http://localhost:5000
- **Painel Administrativo**: http://localhost:5000/admin

---

## CONFIGURAÇÃO INICIAL

### 1. Primeiro Uso

1. **Acesse o painel administrativo**: http://localhost:5000/admin

2. **Configure suas informações**:
   - Clique em "Editar" nas Informações Pessoais
   - Preencha seus dados profissionais
   - **IMPORTANTE**: Adicione as coordenadas do seu escritório para o mapa funcionar

3. **Adicione seus serviços**:
   - Vá em "Gerenciar" na seção Serviços
   - Adicione os serviços jurídicos que você oferece

4. **Adicione avaliações de clientes**:
   - Vá em "Gerenciar" na seção Avaliações
   - Adicione comentários de clientes satisfeitos

### 2. Configuração de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Google Maps API Configuration
GOOGLE_MAPS_API_KEY=sua_chave_do_google_maps_aqui
GOOGLE_PLACE_ID=seu_place_id_do_google_aqui

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta-super-segura-aqui

# Para produção, use:
# FLASK_ENV=production
```

### 3. Como Obter Coordenadas para o Mapa

1. Abra o Google Maps: https://maps.google.com
2. Pesquise pelo endereço do seu escritório
3. Clique com o botão direito no local exato
4. Copie as coordenadas que aparecem (formato: -23.5505, -46.6333)
5. Cole a primeira coordenada (Latitude) e a segunda (Longitude) no painel admin

### 4. WhatsApp Integration

O link do WhatsApp é gerado automaticamente baseado no seu número de telefone. Use o formato: **(11) 99999-9999**

---

## PERSONALIZAÇÃO

### Trocar sua foto
Substitua o arquivo `static/images/lawyer-hero.jpg` pela sua foto profissional.

### Alterar cores
Edite o arquivo `static/css/style.css` e modifique as variáveis CSS no início:

```css
:root {
    --primary-color: #1a365d;
    --secondary-color: #2c5282;
    --accent-color: #ed8936;
    /* ... outras cores */
}
```

### Configurando o Google Maps API
1. Obtenha uma chave da API do Google Maps em https://console.cloud.google.com/
2. Configure a variável `GOOGLE_MAPS_API_KEY` no arquivo `.env`
3. Configure restrições de domínio para segurança

---

## DEPLOY EM PRODUÇÃO

### Pré-requisitos
- Conta no GitHub
- Chave da API do Google Maps
- Conta no Vercel

### Deploy

#### Vercel (Recomendado)
1. Faça push do código para GitHub
2. Conecte sua conta Vercel ao GitHub
3. Importe o repositório
4. Configure as variáveis de ambiente:
   - `GOOGLE_MAPS_API_KEY`
   - `GOOGLE_PLACE_ID`
   - `SECRET_KEY`
   - `FLASK_ENV=production`
5. Deploy automático!

### Configurações de Produção

#### Variáveis de Ambiente (OBRIGATÓRIAS):
```env
GOOGLE_MAPS_API_KEY=sua_chave_aqui
GOOGLE_PLACE_ID=seu_place_id_aqui
SECRET_KEY=chave-super-secreta-aleatoria
FLASK_ENV=production
PORT=5000
```

#### Para Banco PostgreSQL (Recomendado para produção):
```env
DATABASE_URL=postgresql://user:password@host:port/database
```

### Segurança
- Mude a SECRET_KEY para algo aleatório
- Use HTTPS (automático na maioria das plataformas)
- Configure restrições da API do Google Maps para seu domínio
- O arquivo .env NÃO vai para o GitHub (está no .gitignore)

---

## ESTRUTURA DE ARQUIVOS

```
meus/
├── app.py                 # Aplicação principal Flask
├── database.py           # Configuração do banco de dados
├── google_reviews.py     # Integração com Google Reviews
├── sample_data.py        # Dados de exemplo
├── requirements.txt      # Dependências Python
├── runtime.txt          # Versão do Python para deploy
├── Procfile             # Configuração deploy
├── vercel.json          # Configuração Vercel
├── start.sh             # Script de inicialização
├── run.py               # Launcher alternativo
├── .env                 # Variáveis de ambiente (não commitado)
├── .gitignore           # Arquivos ignorados pelo Git
├── instance/
│   └── portfolio.db     # Banco de dados SQLite
├── static/
│   ├── css/
│   │   └── style.css    # Estilos CSS personalizados
│   ├── js/              # Arquivos JavaScript
│   └── images/
│       └── lawyer-hero.jpg # Imagem principal
└── templates/
    ├── base.html        # Template base
    ├── index.html       # Página principal
    ├── admin.html       # Painel administrativo
    ├── admin_lawyer.html # Edição de informações
    ├── admin_services.html # Gerenciamento de serviços
    ├── admin_about.html # Gerenciamento sobre nós
    └── admin_reviews.html # Gerenciamento de avaliações
```

---

## FUNCIONALIDADES TÉCNICAS

### Painel Administrativo
- **Informações Pessoais**: Edição completa dos dados do advogado
- **Gerenciar Serviços**: Adicionar/remover/editar serviços oferecidos
- **Gerenciar Sobre Nós**: Seções sobre missão, visão e valores  
- **Gerenciar Avaliações**: Sistema de avaliações manuais + integração Google Reviews
- **Reset de Dados**: Voltar aos dados de exemplo

### Integração Google Reviews
- Busca automática de avaliações do Google My Business
- Combinação com avaliações manuais
- Fallback gracioso quando API não está configurada

### Banco de Dados
- Utiliza SQLite para desenvolvimento
- Suporte a PostgreSQL para produção
- Criado automaticamente na primeira execução
- Sistema de migração simples

### Responsividade
- Design responsivo usando Bootstrap 5
- Funciona em desktop, tablet e mobile
- Navegação otimizada para dispositivos móveis

---

## SOLUÇÃO DE PROBLEMAS

### Erro: "ModuleNotFoundError"
```bash
pip3 install -r requirements.txt
```

### Porta já em uso
Se aparecer erro de porta, mude a porta no final do arquivo `app.py`:
```python
app.run(debug=True, port=5001)  # Mude para 5001 ou outra porta
```

### Problemas com o Banco de Dados
```bash
# Delete o arquivo portfolio.db e reinicie a aplicação
rm instance/portfolio.db
python app.py
```

### Erro: "Google Maps API key not configured"
1. Obtenha uma chave da API do Google Maps
2. Configure a variável `GOOGLE_MAPS_API_KEY` no arquivo `.env`

### Erro: "Google Place ID not configured"
1. Obtenha o Place ID do seu negócio
2. Configure a variável `GOOGLE_PLACE_ID` no arquivo `.env`

---

## REQUISITOS TÉCNICOS

### Requisitos Mínimos
- Python 3.7+
- pip (gerenciador de pacotes Python)
- 50MB de espaço em disco

### Dependências Python
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Flask-WTF 1.1.1
- WTForms 3.0.1
- python-dotenv 1.0.0
- requests 2.31.0

---

## RECURSOS ADICIONAIS

### Suporte
Para suporte técnico ou dúvidas sobre personalização:
1. Verifique este README
2. Consulte a documentação do Flask: https://flask.palletsprojects.com/
3. Documentação do Bootstrap: https://getbootstrap.com/

### Próximas Funcionalidades
- [ ] Sistema de blog
- [ ] Integração com redes sociais
- [ ] Sistema de agendamento online
- [ ] Múltiplos idiomas
- [ ] Analytics e métricas

---

## LICENÇA

Este projeto foi desenvolvido para uso pessoal/profissional da advogada Simone Persin Côrtes.

---

**Tudo pronto!** Seu portfólio profissional está funcionando!

**Importante**: Lembre-se de configurar as variáveis de ambiente antes de fazer deploy em produção! 