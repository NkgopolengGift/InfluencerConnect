# InfluencerConnect  

## Project Overview  

**InfluencerConnect** is a platform that connects influencers with sponsors by consolidating statistics from platforms like YouTube, Facebook, Instagram, and TikTok into a unified profile. This project was developed for the module **SWP316D (Software Project)** at **Tshwane University of Technology**.  

### Key Features  
- Aggregates influencer data from multiple social media platforms (YouTube, TikTok, Instagram, Facebook).  
- Provides brands with a streamlined way to discover and collaborate with influencers.  
- Secure payment integration for sponsorships (PayStack).  
- PDF and DOCX report generation for influencer profiles.  
- Admin dashboard for managing users and platform activity.  

## Legal Notice  

This project is the intellectual property of **Tshwane University of Technology**. Any unauthorized monetization or distribution of this project without explicit permission from the university will result in legal action.  

## Technologies Used  

- **Backend:** Django  
- **Frontend:** JavaScript, HTML, CSS  
- **Database:** PostgreSQL (hosted on Render)  
- **APIs:** YouTube Data API, TikTok API, PayStack API, Instagram (via Instaloader)  
- **Other Libraries:** python-docx, reportlab, pandas, Pyrebase4, google-api-python-client  

## Setup & Prerequisites  

To clone and run this project locally, you will need:  

- **Python 3.12+**  
- **PostgreSQL database** (local or cloud, e.g., Render)  
- **YouTube Data API Key** – For fetching YouTube analytics.  
- **TikTok API Access** – For TikTok data retrieval.  
- **PayStack API Key & Account** – For payment processing.  
- **Render PostgreSQL credentials** (if using Render)  


### Installation & Running the Project

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

3. Run the development server:
   ```
   python manage.py runserver
   ```
   
### Environment Variables  

Create a `.env` file in your project root with the following (update with your actual credentials):  

```env  
SECRET_KEY=your_django_secret_key_here  
DEBUG=True  
YOUTUBE_API_KEY=your_youtube_api_key_here  
TIKTOK_CLIENT_SECRET=your_tiktok_client_secret  
TIKTOK_CLIENT_KEY=your_tiktok_client_key  
CHAT_ENGINE_PROJECT_ID=your_chat_engine_project_id  
CHAT_ENGINE_PRIVATE_KEY=your_chat_engine_private_key  
PAYSTACK_PUBLIC_KEY=your_paystack_public_key  
PAYSTACK_SECRET_KEY=your_paystack_secret_key  

DB_NAME=your_db_name  
DB_USER=your_db_user  
DB_PASSWORD=your_db_password  
DB_HOST=your_db_host  
DB_PORT=5432  
```  
