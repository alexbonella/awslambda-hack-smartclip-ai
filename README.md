# awslambda-hack-smartclip-ai

# 🎬 Smart Clip AI – From Long Videos to Viral Shorts with AI

⚡ **Smart Clip AI** is an intelligent, serverless video summarization app that transforms long-form videos into engaging short clips—tailored to your audience's goals. Whether you're aiming to **educate**, **entertain**, or **inspire**, Smart Clip AI makes your content short, sharp, and shareable.

## 🚀 Try the Demo

> 📥 Drag & Drop your video in our **Streamlit Web App**, and let AI do the magic.

## 🧠 What It Does

Smart Clip AI uses AI and AWS serverless architecture to:
- Upload your video
- Transcribe the content
- Detect key moments based on your audience intent
- Auto-generate short-form clips with captions and hashtags
- Notify you when your clip is ready to post 💥

> 🧩 Audience Goals Supported:  
`["Entertain", "Educate", "Inspire", "Build Community", "Social Impact", "Promote a Product", "Showcase Expertise", "Awareness"]`

## 🖼️ Demo Architecture

![Smart Clip AI State Machine Diagram](demo_image.png)

## 🛠️ How It Works

### 📥 1. Upload Video
Drag and drop your video in the Streamlit app. It’s automatically uploaded to an **S3 Input Bucket**.

### ⚙️ 2. Trigger the Magic
An **EventBridge** rule triggers an **AWS Step Function** that orchestrates a pipeline of Lambda functions.

### 🧩 3. State Machine Workflow

| Step | Description |
|------|-------------|
| 🔤 **Transcription** | Transcribes the video using Amazon Transcribe. |
| ✨ **AI Analysis** | Uses the transcript + Bedrock AI to extract key phrases and generate hashtags based on your selected **audience objective**. |
| 🎯 **Highlight Detection** | Detects the most impactful video segments using smart heuristics and AI (this was the hardest part!). |
| 💬 **Subtitle Generation** | Generates subtitles for the selected clip. |
| 📲 **Final Output** | Adds hashtags + creates a shareable version of your clip. |
| 📧 **Notification** | Sends an email when your final video is ready and saved back into S3. |

## 💸 Pricing

On average:
- ✅ 1 video costs **~$0.40** or less aprox 
- ✅ You can process **~12 videos** with **$5 AWS credit**

> Efficient, scalable, and cost-friendly for creators and brands alike.

## 🎥 Example Runs

| Input Long Video | Output Short Video | Audience Objective | Duration (Long) | Duration (Short) | Reduction (%) |
|------------------|--------------------|--------------------|------------------|-------------------|----------------|
| [🎞️ interview_full.mp4](videos/input/interview_full.mp4) | [⚡ interview_short.mp4](videos/output/interview_short.mp4) | Showcase Expertise | 12:00 min | 1:30 min | 87.5% |
| [🎞️ product_demo_full.mp4](videos/input/product_demo_full.mp4) | [⚡ product_demo_short.mp4](videos/output/product_demo_short.mp4) | Promote a Product | 8:30 min | 1:10 min | 86.3% |
| [🎞️ event_talk_full.mp4](videos/input/event_talk_full.mp4) | [⚡ event_talk_short.mp4](videos/output/event_talk_short.mp4) | Inspire | 15:00 min | 2:00 min | 86.7% |
| [🎞️ vlog_day1_full.mp4](videos/input/vlog_day1_full.mp4) | [⚡ vlog_day1_short.mp4](videos/output/vlog_day1_short.mp4) | Entertain | 10:00 min | 1:20 min | 86.7% |
| [🎞️ campaign_full.mp4](videos/input/campaign_full.mp4) | [⚡ campaign_short.mp4](videos/output/campaign_short.mp4) | Social Impact | 9:45 min | 1:15 min | 87.2% |

##  🧠 LLM-Powered Intelligence

In the AI Analysis step, Smart Clip AI randomly selects one of the supported LLM providers to enhance creativity and diversity in outputs.

Currently, the app chooses between:

* amazon.titan-text-express-v1 (Amazon Titan)
* anthropic.claude-3-haiku-20240307-v1:0 (Claude 3 Haiku by Anthropic)

This random selection helps experiment with tone, style, and semantic richness during key phrase extraction and hashtag generation.

> **NOTE:** In future releases, support for all available Amazon Bedrock models will be added to give users more flexibility and control over AI behavior.

---

## 🎯 Why Smart Clip App?

Because long content is valuable—but short content *wins* on social.  
With Smart Clip AI, creators can **repurpose content**, grow audiences, and stay consistent—without spending hours editing.

## 🛠️ Built With

- **Frontend**: Streamlit
- **Cloud Storage**: Amazon S3
- **Orchestration**: AWS Step Functions
- **Compute**: AWS Lambda
- **AI/LLM**: Amazon Bedrock
- **Notifications**: Amazon SNS
- **Transcription**: Amazon Transcribe

---

## 🤘 Meet the Creator

👋 Hi, I’m Alex – Senior Data Engineer, AI Builder, and 4x **AWS Community Builder** in Data from 🇨🇴 Colombia.  

I specialize in designing intelligent, serverless, and scalable data solutions in the cloud. I'm also a **Udemy instructor** with two hands-on courses:
- 🧰 **Portfolio Data Engineer**
- 📡 **Analysis Streaming with Real-Time Data**

This tool reflects my passion for merging **AI + Cloud** to empower content creators through **automation and storytelling**.

Let’s build the future of content—together.

> 🏁 Built with ❤️ for the [AWS Lambda Hackathon](https://github.com/aws-samples/aws-lambda-hackathon)
