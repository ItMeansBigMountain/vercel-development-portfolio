# Codology Deployment Plan

## Platform Recommendation
- **Primary**: Vercel (based on existing `.vercel/project.json` configuration)
- **Alternative**: AWS EC2 / DigitalOcean Droplet (for full control)
- **Container**: Docker (optional)

## Steps

### 1. Preparation
- Clone repository to target environment
- Navigate to `/data/OpEnCLAw/Codology`
- Install Node.js dependencies:
  ```bash
  cd /data/OpEnCLAw/CodologySERVER && npm install
  ```

### 2. Configuration
- Set environment variables:
  - `DB_CONNECTION_STRING` for MySQL
  - `SECRET_KEY` for authentication
  - `NODE_ENV=production`
- Create `.env` in `SERVER/` with variables

### 3. Security Hardening
- Reference `/data/OpEnCLAw/SECURITY_SANITIZATION_NOTES.md`:
  - Enable HTTPS via Vercel/load balancer
  - Implement rate limiting
  - Sanitize inputs per security checklist
- Configure firewall rules

### 4. Deployment
#### Vercel Deployment
1. Create Vercel account
2. Connect GitHub repository
3. Build command: `npm install && npm run build` (if applicable)
4. Output directory: `SERVER/`
5. Deploy and test endpoints

#### Manual Deployment
1. Set up MySQL database
2. Run `sequelize.sync()` to create tables
3. Configure systemd service

### 5. Validation
- Test endpoints (`GET /health`, `POST /login`)
- Verify database connection
- Check security checklist compliance
- Validate against `security_sanitization_notes.md`

### Success Criteria
✓ Deployment completes without errors  
✓ Application responds on HTTPS  
✓ Database connection established  
✓ Security checklist validated  

## Dependencies
- Vercel account (free tier)
- MySQL database
- Node.js v18+