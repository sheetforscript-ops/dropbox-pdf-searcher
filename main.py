"""
PDF/Text Analyzer & Local Q&A Tool (Lightweight Version)
Author: Codebro

Features:
- Reads PDF files
- Extracts text
- Performs word frequency analysis
- Allows basic keyword-based question answering
- No heavy libraries like PyTorch; fully free and lightweight
"""

# ------------------ Imports ------------------ #
import PyPDF2
from collections import Counter
from textblob import TextBlob

# ------------------ PDF Functions ------------------ #
def extract_text_from_pdf(pdf_path):
    """
    Extract all text from a PDF file
    :param pdf_path: str, path to PDF
    :return: str, all text from PDF
    """
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# ------------------ Analysis Functions ------------------ #
def analyze_word_frequency(text, top_n=10):
    """
    Count the most common words in the text
    :param text: str
    :param top_n: int, number of top words
    :return: list of tuples (word, count)
    """
    words = [word.lower() for word in text.split() if word.isalpha()]
    counter = Counter(words)
    return counter.most_common(top_n)

def keyword_based_answer(text, question):
    """
    Basic keyword-based QA: returns sentences containing the keyword
    :param text: str, document text
    :param question: str
    :return: str, answer
    """
    # Extract keyword (take nouns or important words)
    blob = TextBlob(question)
    keywords = [word.lemmatize() for word, pos in blob.tags if pos.startswith("NN")]  # nouns
    if not keywords:
        keywords = question.lower().split()

    # Find sentences containing keyword(s)
    sentences = TextBlob(text).sentences
    relevant = [str(s) for s in sentences if any(k.lower() in str(s).lower() for k in keywords)]
    if relevant:
        return "\n".join(relevant[:3])  # return top 3 sentences
    else:
        return "No relevant information found."

# ------------------ Main Program ------------------ #
if __name__ == "__main__":
    print("=== PDF/Text Analyzer & Local Q&A Tool (Lightweight) ===")
    
    # Step 1: Load PDF file
    file_path = input("Enter PDF file path: ")
    text = extract_text_from_pdf(file_path)
    print("\n[INFO] Text extracted successfully!\n")

    # Step 2: Word frequency analysis
    print("Top 10 words in the document:")
    for word, count in analyze_word_frequency(text):
        print(f"{word}: {count}")

    # Step 3: Local keyword-based Q&A
    while True:
        question = input("\nAsk a question about the document (or type 'quit'): ")
        if question.lower() == "quit":
            print("Exiting...")
            break
        answer = keyword_based_answer(text, question)
        print("Answer:\n", answer)
