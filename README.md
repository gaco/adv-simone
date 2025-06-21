# Portfólio Profissional - Simone Persin Côrtes

Site profissional moderno e responsivo para advogados, com sistema de administração, integração com Google Reviews e mapa interativo.

## Características

-Design moderno e responsivo
-Painel administrativo protegido
-Integração com Google Reviews
-Mapa interativo do escritório
-Link direto para WhatsApp
-Gerenciamento de conteúdo
-SEO otimizado (Otimização para Mecanismos de Busca)

## Configuração Inicial

### 1. Preparação do Ambiente

```bash
# Clone o repositório
git clone [url-do-repositorio]
cd [nome-do-diretorio]

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

### 2. Configuração das Variáveis de Ambiente

Renomei o `.env.example` para `.env` e altere as configuracões de acordo


### 3. Configuração do Google Reviews

Para obter reviews reais do Google, siga estes passos:

1. **Obtenha uma Chave da API do Google Maps**:
   - Acesse o [Google Cloud Console](https://console.cloud.google.com)
   - Crie um novo projeto ou selecione um existente
   - Ative a API do Places
   - Crie uma chave de API em "Credenciais"
   - Copie a chave e adicione em `GOOGLE_MAPS_API_KEY` no `.env`

2. **Obtenha o Place ID do seu estabelecimento**:
   - Acesse o [Place ID Finder](https://developers.google.com/maps/documentation/javascript/examples/places-placeid-finder)
   - Pesquise pelo nome/endereço do seu estabelecimento
   - Copie o Place ID e adicione em `GOOGLE_PLACE_ID` no `.env`

3. **Restrições de Segurança**:
   - No Google Cloud Console, configure restrições de domínio para sua chave API
   - Recomendado: restrinja por domínio em produção
   - Para desenvolvimento: pode restringir por IP

### 4. Inicialização

```bash
# Inicie o servidor de desenvolvimento
python app.py
```

O site estará disponível em `http://localhost:3000`

## Uso do Sistema

### Acesso ao Painel Admin

1. Acesse `/admin` no seu navegador
2. Use as credenciais definidas em `.env`:
   - Username: `ADMIN_USERNAME`
   - Password: `ADMIN_PASSWORD`

### Gerenciamento de Conteúdo

No painel administrativo você pode:
- Atualizar informações do advogado
- Gerenciar serviços oferecidos
- Visualizar reviews do Google
- Adicionar reviews manuais
- Configurar textos da seção "Sobre"

## Deploy em Produção

### Vercel (Recomendado)

1. Push do código para o GitHub
2. Conecte ao Vercel
3. Configure as variáveis de ambiente:
   ```env
   FLASK_ENV=production
   GOOGLE_MAPS_API_KEY=sua_chave_aqui
   GOOGLE_PLACE_ID=seu_place_id_aqui
   SECRET_KEY=chave_secreta_producao
   ADMIN_USERNAME=usuario_admin
   ADMIN_PASSWORD=senha_admin
   ```

### Outros Provedores

Para outros provedores, certifique-se de:
1. Configurar todas as variáveis de ambiente
2. Usar um servidor WSGI (ex: Gunicorn)
3. Configurar HTTPS
4. Configurar domínio personalizado

## Manutenção

### Backups
- O banco SQLite está em `instance/portfolio.db`
- Faça backups regulares deste arquivo
- Em produção, considere migrar para PostgreSQL

### Atualizações
- Mantenha as dependências atualizadas
- Verifique regularmente as restrições da API do Google
- Monitore o uso da API do Google

## Suporte

Para suporte técnico:
1. Consulte esta documentação
2. Verifique as [Issues no GitHub](link-do-repositorio/issues)
3. Abra uma nova issue se necessário

## Licença

Este projeto foi desenvolvido para uso exclusivo da advogada Simone Persin Côrtes.
Todos os direitos reservados.
