# AI Customer support

**Problem Statement**
How sales, customer support, marketing and other go-to-market functions in the company surface signals to the product team about what is important to build in the product. (These may range from specific asks from existing customers to general ideas they are hearing in the industry).

**My Solution:**
Generative AI 😎

## Key Features:

**Streamlined Feedback Collection Interface:**

- User-friendly Streamlit app for easy text message input. (Used Simple text input for explaining the use case, but it can be linked with Gmail)
- Accommodates various feedback types (complaints, requests, feedback, etc.).

**AI-Powered Information Extraction:**
- LangChain Property Extractor accurately identifies:
  - Category (e.g., complaint, refund request, product feedback)
  - Mentioned product
  - Issue description
  - Sentiment (positive, negative, neutral)
  - Emotion (happy, sad, angry, etc.)
- Leverages OpenAI's GPT-3.5-turbo for advanced language understanding.
  
**Tailored Response Generation:**
- OpenAI ChatGPT model crafts personalized replies based on extracted information.
- Addresses issues directly or acknowledges feedback with appropriate sentiment.
  
**Prioritization and Task Management:**
- Automatically creates cards in a Trello list for issues requiring further action.
- Prioritizes feedback based on type and sentiment.

## How this idea will help to solve the problem 🤔:
- **Automate extraction:** Manual analysis of large volumes of feedback is time-consuming and inefficient.
- **AI-powered insights:** LangChain and OpenAI automate key information extraction, saving considerable time and effort for the product team.
- **Trello integration:** Automatic Trello card creation ensures actionable follow-up and task management for identified issues.
- **Seamless information flow:** The ability to track feedback progression in Trello fosters transparency and collaboration between customer-facing teams and the product team.


