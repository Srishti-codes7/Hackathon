# LearnFlow — Adaptive Learning Frontend

A runnable React + Vite frontend prototype for an adaptive learning recommendation system.

## Requirements

- Node.js 18+
- npm

## Run locally

```bash
npm install
npm run dev
```

Then open the local URL printed by Vite, usually:

http://localhost:5173

## Build for production

```bash
npm run build
npm run preview
```

## What's included

- Responsive learner dashboard
- Sidebar navigation
- Overall mastery / streak / course statistics
- AI recommendation card
- Topic mastery progress
- Mastery trend chart
- Recent activity
- Adaptive learning page
- Mock learning activity screen
- Responsive mobile navigation
- Mock data separated in `src/data/mockData.js`

## Next integration step

Replace the mock data in `src/data/mockData.js` with API calls to the recommendation backend.

A natural API shape is:

GET /api/v1/learners/:learnerId/dashboard
GET /api/v1/recommendations/next?learnerId=:learnerId
POST /api/v1/interactions
GET /api/v1/learners/:learnerId/mastery

The current UI intentionally keeps the backend-independent parts isolated so the API can be added without redesigning the frontend.
