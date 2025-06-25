# 🎬 Smart Clip AI – From Long Videos to Shareable Shorts with AWS & AI

⚡ **Smart Clip AI** is an intelligent, serverless video summarization app that transforms long-form videos into engaging short clips—tailored to your audience's goals. Whether you're aiming to **educate**, **entertain**, or **inspire**, Smart Clip AI makes your content short, sharp, and shareable.

This tool reflects my passion for merging **AI + Cloud** to empower content creators through **automation and storytelling**.

## 🛠️ How It Works

1. **Upload Video:** Drag and drop your video into the Streamlit app. It’s automatically uploaded to an **S3 Input Bucket**.
2. **Trigger the Magic:** An **EventBridge** rule triggers an **AWS Step Function** that orchestrates a pipeline of **`Lambda functions`**.
3. **State Machine Workflow** :
   
   - Transcribe the content
   - Detect key moments based on your audience's intent
   - Auto-generate short-form clips with captions and hashtags
   - Notify you when your clip is ready to post 💥
     
## 🖼️ Demo Architecture

![Smart Clip AI State Machine Diagram](https://github.com/alexbonella/awslambda-hack-smartclip-ai/blob/main/images/New-Flow.gif)

## ⚙️ AWS Lambda Zone – Where the Magic Happens

> Each function is optimized to handle a specific part of the pipeline with speed, precision, and scalability.

| <img src="https://github.com/alexbonella/awslambda-hack-smartclip-ai/blob/main/media/lambda_icon.png" width="20"/> **Lambda Functions** | Description |
|------|-------------|
| 🔤 [**Transcription**](https://github.com/alexbonella/awslambda-hack-smartclip-ai/blob/main/scripts/lambda_functions/audio_transcribe.py) | Transcribes the video using Amazon Transcribe. |
| ✨ [**AWS Bedrock Step**](https://github.com/alexbonella/awslambda-hack-smartclip-ai/blob/main/scripts/lambda_functions/answer-bedrock.py) | Uses the transcript + Bedrock AI to extract key phrases and generate hashtags based on your selected **audience objective**  `["Entertain", "Educate", "Inspire", "Build Community", "Social Impact", "Promote a Product", "Showcase Expertise", "Awareness"]` |
| 🎯 [**Highlight Clip Detection**](https://github.com/alexbonella/awslambda-hack-smartclip-ai/blob/main/scripts/lambda_functions/video_clips.py) | After identifying key phrases based on the audience's intent, I use **`AWS Elemental MediaConvert`** to extract the most impactful video segments *`(this was the hardest part!)`*. |
| 💬 [**New Subtitle Generation**](https://github.com/alexbonella/awslambda-hack-smartclip-ai/blob/main/scripts/lambda_functions/little_video_subtitles.py) | Generates new subtitles for the selected clip. |
| 📲 [**Final Output**](https://github.com/alexbonella/awslambda-hack-smartclip-ai/blob/main/scripts/lambda_functions/hashtag_video.py) | Adds smart hashtag and delivers a ready-to-post video for your social media . 

## 💸 Pricing

On average:
- ✅ 1 video costs **~$0.40** or less aprox 
- ✅ You can process **~12 videos** with **$5 AWS credit**

> Efficient, scalable, and cost-friendly for creators and brands alike.

## ![YouTube](https://img.icons8.com/color/48/000000/youtube-play.png) Video Demo in Action

* [**Go To Demo**](https://youtu.be/owTl5Fg5GVU)

## 🎥 Example Runs

| Input Long Video | Output Short Video | Audience Objective | Duration (Long) | Duration (Short) | Reduction (%) |
|------------------|--------------------|--------------------|------------------|-------------------|----------------|
| [Why AI Is Our Ultimate Test and Greatest Invitation.mp4](https://www.youtube.com/watch?v=6kPHnl-RsVI) | [⚡ Why_AI_Is_Our_Ultimate_Test_audience-SocialImpact_final.mp4](https://drive.google.com/file/d/1VqvoNLzrEV9f62s-6o-7Y60QR8TxK7u4/view?usp=drive_link) | Social Impact | 15:15 min | 1:00 min | 93.4% |
| [Shark Tank US CUPBOP Are Asking For $1M From The Sharks.mp4](https://www.youtube.com/watch?v=MdA1JIUTEHc&t=5s) | [⚡ Cupbob_SharkTank_audience-Entertain_final.mp4](https://drive.google.com/file/d/1-0z0XSAeHv7d3sZH4AOvFZsWzfDJ7QXH/view?usp=drive_link) | Entertain | 14:02 min | 00:47 min | 94.42% |
| [Shark Tank US CUPBOP Are Asking For $1M From The Sharks.mp4](https://www.youtube.com/watch?v=MdA1JIUTEHc&t=5s) | [⚡ Cupbob_SharkTank_audience-PromoteaProduct_final.mp4](https://drive.google.com/file/d/1u70_w96R39Umx3m4usTnSe7NRetj51KP/view?usp=drive_link) | Promote a Product | 14:02 min | 00:52 min | 93.82% |
| [Shakira on Reclaiming Her Resilience in New Album After Ex-Husband, Cardi B Collab and NYC Surprise.mp4](https://www.youtube.com/watch?v=GPmnZdaa1bk) | [⚡ shakira_video_full_audience-Inspire_final.mp4](https://drive.google.com/file/d/1x8ubftd9_9xZdaFcVNwMkuRWOrCQ8WlJ/view?usp=drive_link) | Inspire | 11:13 min | 00:38 min | 94.35% |
| [A Bidding War Breaks Out During Scrub Daddy's Pitch.mp4](https://www.youtube.com/watch?v=ae5MssJ8en4&t=11s) | [⚡ shark_tank_usa_audience-Inspire_final.mp4(https://drive.google.com/file/d/16p8r0DIX6f47n94nv794lSufikOa101Y/view?usp=drive_link) | Inspire | 12:20 min | 0:38 min | 	94.86% |

##  🧠 LLM-Powered Intelligence

In the AI Analysis step, Smart Clip AI randomly selects one of the supported LLM providers to enhance creativity and diversity in outputs.

Currently, the app chooses between:

* **`amazon.titan-text-express-v1 (Amazon Titan)`**
* **`anthropic.claude-3-haiku-20240307-v1:0 (Claude 3 Haiku by Anthropic)`**

This random selection helps experiment with tone, style, and semantic richness during key phrase extraction and hashtag generation.

> **NOTE:** In future releases, support for all available Amazon Bedrock models will be added to give users more flexibility and control over AI behavior.

---

## 🎯 Why Smart Clip App?

Because long content is valuable, but short content *wins* on social. With Smart Clip AI, creators can **repurpose content**, grow audiences, and stay consistent without spending hours editing.

## 🛠️ Built With

- **Frontend**: Streamlit
- **Cloud Storage**: Amazon S3
- **Orchestration**: AWS Step Functions
- **Compute**: AWS Lambda
- **Video Edition**: AWS Elemental MediaConvert
- **AI/LLM**: Amazon Bedrock
- **Notifications**: Amazon SNS
- **Transcription**: Amazon Transcribe

---

## 🤘 Meet the Creator

Hi, I’m Alex – Senior Data Engineer, AI Builder, and 4x **AWS Community Builder** in Data from 🇨🇴 Colombia.  

I specialize in designing intelligent, serverless, and scalable data solutions in the cloud. I'm also a **Udemy instructor** with two hands-on courses:
- [**Build Your Data Engineer Portfolio – 4 Real-World Projects | 1.7K+ students**](https://www.udemy.com/course/crea-tu-portafolio-como-data-engineer-4-proyectos-reales-datexland/?couponCode=B91BB3D-JUNIO)
- [**Streaming Data Analysis – Data Engineer Portfolio Project | 180+ students**](https://www.udemy.com/course/analisis-de-streaming-de-datos-portafolio-data-engineer/?couponCode=4CBC9B3-JUNIO)

## Connect with me: 

 [![LinkedIn](https://img.shields.io/badge/-LinkedIn-3b5998)](https://www.linkedin.com/in/alexanderbolano)
 [![Medium](https://img.shields.io/badge/-Medium-black)](https://datexland.medium.com/)
 [![Twitter](https://img.shields.io/badge/-@datexland-1DA1F2)](https://twitter.com/datexland)
 [![Stackoverflow](https://img.shields.io/badge/-Stackoverflow-ff7c55)](https://stackoverflow.com/users/10906576/alexbonella)
 
