# AI-Powered FAQ System with Administration

This project implements a smart FAQ system powered by AI with a comprehensive administration interface.

## Features
- AI-generated FAQ content from PDF documents
- FAQ management with manual editing
- User administration system
- Visit statistics and predictions
- PDF document management
- AI model configuration

## Technologies
- **Backend**: Python Flask, PostgreSQL, Ollama
- **Frontend**: React TypeScript, Tailwind CSS
- **AI**: RAG model with Ollama
- **Deployment**: Docker, Docker Compose

## System Requirements
- Docker 20.10+
- Docker Compose 2.20+
- 8GB RAM minimum (16GB recommended for AI)
- 50GB disk space

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/valentinkt/faq-ai-project.git
   cd faq-ai-project
   ```

2. **Download AI model**
   ```bash
   docker compose run ollama ollama pull llama3
   ```

3. **Start services**
   ```bash
   docker compose up --build -d
   ```

4. **Initialize database**
   ```bash
   docker compose exec backend flask db init
   docker compose exec backend flask db migrate -m "Initial migration"
   docker compose exec backend flask db upgrade
   ```

5. **Access applications**
   - Frontend: http://localhost
   - Admin Dashboard: http://localhost/admin
   - Default admin: admin@example.com / adminpassword

## Services
- Web UI: http://localhost
- API: http://localhost/api
- Ollama: http://localhost/ollama
- PostgreSQL: postgres:5432
- Redis: redis:6379

## Project Structure
```
faq-ai-project/
├── backend/          # Python Flask backend
├── frontend/         # React TypeScript frontend
├── nginx/            # Nginx configuration
├── docker-compose.yml # Docker compose configuration
└── README.md         # Project documentation
```

## Management Commands

**View logs**
```bash
docker compose logs -f backend
```

**Stop services**
```bash
docker compose down
```

**Restart a service**
```bash
docker compose restart backend
```

**Run database migrations**
```bash
docker compose exec backend flask db upgrade
```

**Access PostgreSQL**
```bash
docker compose exec db psql -U faqadmin faqdb
```

**Clean up everything**
```bash
docker compose down -v --rmi all
```


```bash
docker compose exec backend flask db init
docker compose exec backend flask db migrate -m "Initial migration"
docker compose exec backend flask db upgrade
```
```bash
rm -rf node_modules
rm package-lock.json
npm cache clean --force
npm install
```
```bash
npm run build
npm run start
npm run dev
```

```bash
docker compose run ollama ollama pull llama3
```

```bash
plsql -h localhost -p 5432 -U faqadmin -d faqdb
plsql -h localhost -p 5432 -U faqadmin -d faqdb -f init.sql
````
## Configuration
Configuration files are located in the config/ directory.
## Security
Ensure your environment is secure.
- Use HTTPS for all services.
- Use environment variables for sensitive information.
- Regularly update dependencies.
## Performance
Monitor and optimize your system for performance.
- Use caching where appropriate.
- Optimize database queries.
- Monitor resource usage.
## Troubleshooting
If you encounter issues, refer to the [troubleshooting guide](TROUBLESHOOTING.md).
## Support
For support, please contact
## Support
For support, please contact EMAIL.
## Acknowledgments
- Thanks to [Ollama](
## Acknowledgments
- Thanks to [Ollama](URL_ADDRESSama.ai/) for providing the AI model.
- Thanks to [React](URL_ADDRESSjs.org/) and [TypeScript](URL_ADDRESSpeScript](https://www.typescriptlang.org/) for the frontend.
- Thanks to [Flask](URL_ADDRESSflask.org/) and [PostgreSQL](URL_ADDRESSpostgresql.org/) for the backend.
- Thanks to [Docker](URL_ADDRESSdocker.com/) for containerization.
- Thanks to [Tailwind CSS](URL_ADDRESStailwindcss.com/) for the styling.
- Thanks to [React Router](URL_ADDRESSreactrouter.com/) for navigation.
- Thanks to [React Query](URL_ADDRESStanstack.com/) for data fetching.
- Thanks to [React Icons](URL_ADDRESSreact-icons.com/) for icons.
- Thanks to [React Select](URL_ADDRESSreact-select.com/) for dropdowns.
- Thanks to [React Datepicker](URL_ADDRESSreactdatepicker.com/) for date pickers.
- Thanks to [React Table](URL_ADDRESSreact-table.com/) for tables.
- Thanks to [React Markdown](URL_ADDRESSreact-markdown.com/) for markdown rendering.
- Thanks to [React Dropzone](URL_ADDRESSreact-dropzone.com/) for file uploads.
- Thanks to [React Redux](URL_ADDRESSreact-redux.com/) for state management.
- Thanks to [React Router Redux](URL_ADDRESSreactrouter.com/) for routing.
- Thanks to [React Redux Form](URL_ADDRESSredux-form.com/) for form management.
- Thanks to [React Redux Thunk](URL_ADDRESSredux-thunk.com/) for async actions.
- Thanks to [React Redux Persist](URL_ADDRESSredux-persist.com/) for state persistence.
- thanks to Vite
)

## Contributing
Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) first.

## License
MIT License
ls