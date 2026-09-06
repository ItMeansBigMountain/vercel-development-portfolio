# Local Meeting Transcriber

## Overview
Local Meeting Transcriber is a cross-platform, privacy-first AI meeting assistant that transcribes, diarizes, and summarizes meetings using local models. It is designed to be deployable to the cloud and accessible from mobile.

## Project Structure
```
/local-meeting-transcriber
├── frontend/     # React Native mobile app (Expo)
├── backend/      # ASP.NET Core Web API
├── infra/        # Terraform scripts for Azure deployment
├── readme.md
├── script.sh
└── local-meeting-transcriber.sln
```

### Backend (ASP.NET Core Web API)
- **Location**: `/Backend/src/api`
- **Technology**: .NET 9, ASP.NET Core Web API
- **Features**:
  - API endpoints for audio upload, transcription, diarization, and summarization
  - JWT authentication
  - Services for handling AI processing (WhisperX, pyannote.audio, Ollama)

#### Local backend configuration
1. Copy `Backend/src/api/appsettings.example.json` to `Backend/src/api/appsettings.Development.json` for local development.
2. Keep `ConnectionStrings:Default` pointed at a local SQLite file, for example `Data Source=local-meeting-transcriber.db`.
3. Set `Jwt:Key` to a local-only secret value at least 32 characters long, and keep `Jwt:Issuer` / `Jwt:Audience` aligned with your client configuration.
4. Do not commit real secrets or production connection strings.

#### Local backend validation
```bash
dotnet restore local-meeting-transcriber.sln
dotnet build local-meeting-transcriber.sln --no-restore
```

### Frontend (React Native)
- **Location**: `/Frontend`
- **Technology**: React Native (Expo)
- **Features**: Mobile app for recording and uploading meeting audio

### Infrastructure (Terraform)
- **Location**: `/infra`
- **Technology**: Terraform
- **Features**: Scripts for deploying to Azure App Service

## Key Technologies
| Layer               | Technology                            |
| ------------------- | ------------------------------------- |
| Frontend            | React Native (Expo)                   |
| Backend API         | ASP.NET Core Web API (.NET 8)         |
| Auth                | ASP.NET Identity + JWT                |
| AI Transcription    | WhisperX (Python subprocess)          |
| Speaker Diarization | pyannote.audio                        |
| AI Summarization    | Ollama + LangChain                    |
| Database            | MS SQL Server or MySQL/Postgres       |
| Deployment          | Azure App Service + Terraform         |

## Current State (based on dev roadmap in readme.md)
- [x] Project initialized
- [ ] Audio file upload endpoint
- [ ] WhisperX + diarization integration
- [ ] LLM-based meeting summarizer
- [ ] LangChain memory store
- [ ] Azure Terraform deployment
- [ ] App Store release

## Next Steps for Completion
1. **Backend Development**:
   - Implement audio file upload endpoint
   - Integrate WhisperX for transcription
   - Integrate pyannote.audio for speaker diarization
   - Integrate Ollama LLM for summarization
   - Implement LangChain for memory storage
   - Secure endpoints with JWT authentication

2. **Frontend Development**:
   - Build React Native app for recording audio
   - Implement upload functionality to backend
   - Display transcription and summary results

3. **Infrastructure**:
   - Complete Terraform scripts for Azure deployment
   - Set up Azure App Service and database

4. **Testing**:
   - Test audio processing pipeline
   - Test authentication and authorization
   - Test end-to-end flow from mobile app to cloud

5. **Deployment**:
   - Deploy to Azure App Service
   - Publish to app stores (iOS/Android via Expo)

## Integration Opportunities
This project could integrate with:
- Coding school platform for recording and transcribing lectures
- Journal AI for transcribing personal voice journals
- Social media analysis for transcribing video content
- CombatAtlas for recording and analyzing martial arts training sessions

## Privacy Note
The application is designed to be privacy-first, with processing done locally where possible and user data stored securely.
