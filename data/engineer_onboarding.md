# Software Engineer Onboarding

Welcome to the engineering team! This guide covers everything you need to get started as a full-stack Node.js/React engineer at Primr.

---

## 1. Access & Accounts

- **GitHub**  
  - Check your email for the repo invitation.  
  - You should have read/write access to `github.com/primr/app`.  
- **Google Workspace**  
  - Company email is `<yourname>@primr.app`.  
  - Access Google Drive folders under “Engineering”.  
- **Slack**  
  - Join #engineering, #team, and #onboarding channels.  
- **Jira**  
  - Log in at `jira.primr.app` with SSO.  
  - Find your name under the “Engineers” group.

---

## 2. Local Development Setup

**Prerequisites**  
- Node.js v14+  
- npm or yarn  
- MongoDB (local) or Docker (optional)

**Steps**  
1. Clone the repo:  
   ```
   git clone https://github.com/primr/app.git
   cd app
   ```  
2. Install dependencies:  
   ```
   npm install
   ```  
3. Copy environment variables:  
   ```
   cp .env.example .env
   ```  
   - Populate `MONGODB_URI`, `SLACK_BOT_TOKEN`, and `NEXT_PUBLIC_API_URL`.  
4. Start MongoDB:  
   - **Local**: `mongod --dbpath ~/data/db`  
   - **Docker**: `docker run -d -p 27017:27017 --name primr-mongo mongo:4.4`  
5. Run the API server:  
   ```
   npm run dev:api
   ```  
6. Run the frontend:  
   ```
   npm run dev:web
   ```  
7. Verify: Navigate to `http://localhost:3000` in your browser.

---

## 3. Team Rituals & Calendar

Please accept these recurring invites on your calendar:

- **Daily Standup**  
  - When: Weekdays at 10:00 AM EST  
  - Where: #standup channel  
- **Sprint Planning**  
  - When: Mondays at 2:00 PM EST  
  - Where: Zoom link in invite  
- **Design Review**  
  - When: Wednesdays at 3:00 PM EST  
  - Where: #design-review channel  
- **Sprint Demo**  
  - When: Fridays at 4:00 PM EST  
  - Where: #demo channel  
- **Onboarding 1:1**  
  - When: Day 2 at 11:00 AM EST  
  - With your manager (calendar invite sent separately)

---

## 4. Meet the Team

We’ve scheduled short intro sessions with each:

- **Your Manager**: Jane Doe (Lead Engineer)  
- **Frontend Lead**: John Smith  
- **Backend Lead**: Alice Lee  
- **QA Engineer**: Bob Kim  

**Icebreaker:**  
In #introductions, share a fun fact and your favorite open-source project.

---

## 5. First Task: API Health Check

Your first assignment helps you learn our codebase:

1. **Read** `README.md` and `docs/api.md` under `docs/`.  
2. **Implement** a new endpoint:  
   - Route: `GET /api/status`  
   - Response: `{ status: "ok", timestamp: <current ISO> }`  
3. **Write Tests** in `tests/status.test.js`:  
   ```js
   import request from 'supertest';
   import app from '../src/app';

   test('GET /api/status returns ok', async () => {
     const res = await request(app).get('/api/status');
     expect(res.body.status).toBe('ok');
     expect(res.body.timestamp).toBeDefined();
   });
   ```  
4. **Run Tests**:  
   ```
   npm test
   ```  
5. **Create a Pull Request** against the `dev` branch and request review from your team leads.

---

Welcome aboard! Let us know if you hit any roadblocks or have questions.
