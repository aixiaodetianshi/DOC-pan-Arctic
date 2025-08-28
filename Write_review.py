# write papers review

import os
import PyPDF2
import spacy
from transformers import pipeline
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# 解决 Hugging Face 缓存问题
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# 关闭 TensorFlow OneDNN 以减少无关警告
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# 初始化 OpenAI GPT-4
os.environ["OPENAI_API_KEY"] = "sk-...svEA"  # 这里需要替换为你的 API Key

# 加载 NLP 处理模型
nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
llm = ChatOpenAI(model_name="gpt-4", temperature=0.5)

# 读取 PDF 文件并提取文本
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text[:5000]  # 限制 PDF 长度，避免超出 BART 处理范围

# 提取关键词
def extract_keywords(text, num_keywords=5):
    doc = nlp(text)
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    return list(set(keywords[:num_keywords]))

# 生成摘要（确保不会超出 BART 的 token 限制）
def generate_summary(text, chunk_size=800):
    """处理超长文本，分批次摘要"""
    if len(text) > chunk_size:
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        summaries = [summarizer(chunk, max_length=150, min_length=50, do_sample=False)[0]['summary_text'] for chunk in chunks]
        return " ".join(summaries)
    else:
        return summarizer(text, max_length=500, min_length=100, do_sample=False)[0]['summary_text']

# 生成综述
def generate_review(summaries):
    review_prompt = PromptTemplate(
        input_variables=["summaries"],
        template="""
        Given the following research summaries, generate a structured literature review on the topic of dissolved organic carbon (DOC) flux in Arctic rivers:
        {summaries}
        Include key findings, trends, and research gaps. Make it concise and well-organized.
        """
    )
    response = llm(review_prompt.format(summaries="\n\n".join(summaries)))
    return response

# 处理所有 PDF 文件
folder_path = r"D:\UZH\2024\20240122 Nutrient and Organic Carbon references\reference"
summaries = []

for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        print(f"Processing: {filename}")

        text = extract_text_from_pdf(pdf_path)
        keywords = extract_keywords(text)
        summary = generate_summary(text)

        summaries.append(f"{filename} - Keywords: {', '.join(keywords)}\n{summary}")

# 生成文献综述
final_review = generate_review(summaries)

# 输出到 Markdown 文件
output_file = "literature_review.md"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("# Arctic River DOC Flux Literature Review\n\n")
    file.write(final_review)

print(f"✅ 综述已生成，文件名：{output_file}")