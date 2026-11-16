# SRS & Workflow Review Portal

## Project Overview
This project is a full-stack assessment application for D'ARTEWEB. It allows an administrator to prepare an SRS document, define workflow steps, publish the review to a client, collect feedback against specific steps, and approve or reject comments. Accepted feedback is stored in a project Memory File with traceability back to the original comment and workflow step.

## Project Objectives
- Build a lightweight full-stack app using React + Flask + SQLite.
- Support admin and client roles with role-based restrictions.
- Preserve workflow-step linkage even after edits.
- Prevent duplicate Memory File entries from repeated approvals.
- Deliver a clear, interview-ready implementation with readable code.

## Technology Stack
- Frontend: React.js with Vite
- Backend: Python Flask
- Database: SQLite
- ORM: Flask-SQLAlchemy
- Auth: session-based lightweight authentication
- Styling: custom CSS
- Testing: Python pytest

## Feature Summary
### Admin
- Login with predefined credentials.
- Create, edit, delete and publish projects.
- Add SRS content and workflow steps.
- Reorder workflow steps.
- Review client comments and accept/reject them.
- Add an optional response.
- View the Memory File and export it as Markdown.

### Client
- Login with predefined credentials.
- View published projects.
- Read SRS content and workflow steps.
- Submit comments against individual workflow steps.
- View the status of submitted comments and admin responses.

## Folder Structure
```text
New/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── requirements.txt
│   ├── controllers/
│   ├── database/
│   ├── models/
│   ├── routes/
│   ├── tests/
│   └── utils/
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
├── .gitignore
├── README.md
└── .git
```

## Database Design
### Users
- id
- username
- password_hash
- role
- created_at

### Projects
- id
- name
- description
- srs_content
- review_status
- client_id
- created_at
- updated_at

### Workflow Steps
- id
- project_id
- title
- description
- sequence
- created_at
- updated_at

### Comments
- id
- step_id
- project_id
- client_id
- body
- status
- admin_response
- created_at
- reviewed_at
- reviewed_by

### Memory Entries
- id
- project_id
- step_id
- source_comment_id
- approved_text
- approved_by
- approved_at

## Database Relationships
- One user can own many projects (client_id).
- One project has many workflow steps.
- One project has many comments.
- Each comment is linked to one workflow step and one client.
- Each accepted comment creates exactly one Memory Entry.
- `MemoryEntry.source_comment_id` is unique to prevent duplicate approval.

## Installation and Setup
### Prerequisites
- Python 3.10+
- Node.js 18+
- npm

### Backend Setup
```bash
cd backend
python -m pip install -r requirements.txt
python app.py
```
The backend runs at:
- http://localhost:5000

### Frontend Setup
Open a second terminal:
```bash
cd frontend
npm install
npm run dev
```
The frontend runs at:
- http://localhost:5173

## Demo Credentials
- Admin username: admin
- Admin password: Admin@123
- Client username: client
- Client password: Client@123

## API Endpoints
### Authentication
- POST /api/login
- POST /api/logout
- GET /api/me

### Projects
- GET /api/projects
- POST /api/projects
- GET /api/projects/<id>
- PUT /api/projects/<id>
- DELETE /api/projects/<id>
- POST /api/projects/<id>/publish

### Workflow
- GET /api/projects/<id>/steps
- POST /api/steps
- PUT /api/steps/<id>
- DELETE /api/steps/<id>
- PUT /api/projects/<id>/steps/reorder

### Comments
- POST /api/comments
- GET /api/projects/<id>/comments
- GET /api/comments/my
- PUT /api/comments/<id>/review

### Memory
- GET /api/memory/<project_id>
- GET /api/memory/<project_id>/export

## Memory File Approval Logic
1. Client submits a comment against a workflow step.
2. The comment is saved with status `pending`.
3. Admin reviews the comment.
4. If accepted, the system creates a new Memory Entry and stores:
   - project_id
   - step_id
   - source_comment_id
   - approved_text
   - approved_by
   - approved_at
5. If rejected, no Memory Entry is created.
6. Pending comments remain excluded from the Memory File.

## Duplicate Prevention Mechanism
- Unique database constraint on `MemoryEntry.source_comment_id`.
- Review logic checks for existing approval before insertion.
- Comment review API rejects repeated approval requests after the comment is already accepted or rejected.
- The system uses a database transaction-like flow by committing only after validation.

## Testing
Run:
```bash
cd backend
python -m pytest tests -q
```
Executed and verified:
- Admin login
- Client login
- Comment submission
- Acceptance flow
- Rejection flow
- Duplicate prevention

## Git Information
This project has been initialized with Git and committed in meaningful stages.

## AI Usage Disclosure
AI tools were used to scaffold the project structure and accelerate implementation. All generated code was reviewed manually, verified through runtime testing, and validated with automated backend tests before completion.

## Quick Demonstration Flow
1. Log in as admin.
2. Create or open a project and add SRS content.
3. Add workflow steps.
4. Publish the project.
5. Log in as client.
6. Open the published project and submit a comment on a step.
7. Log in back as admin.
8. Accept the comment.
9. Confirm it appears in Memory File.
10. Reject another comment and confirm it does not appear in the Memory File.

## Interview Notes
This implementation is intentionally simple, readable, and modular so it can be explained confidently in a technical interview. The key business logic lives in the backend controllers and the project relationship model, while the React UI focuses on business workflow rather than unnecessary complexity.
