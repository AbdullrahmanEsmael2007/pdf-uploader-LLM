import spacy
import re
from sentence_transformers import SentenceTransformer, util

# Load SpaCy model globally
nlp = spacy.load("en_core_web_sm")

# Load SentenceTransformer model for semantic noise detection
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Define boilerplate examples for semantic filtering
noise_examples = [
    "Page 4", "Error fetching Wikipedia article", "Retrieved from Wikipedia",
    "may refer to:", "Contents", "See also", "External links",
    "References", "This article is about", "Table of Contents",
    "Abstract", "Introduction", "Chapter", "Appendix", "Bibliography",
    "Acknowledgements", "Index", "Disclaimer", "Notice", "Copyright",
    "All rights reserved", "Version", "Update", "For further reading",
    "Contact information", "Terms and Conditions", "Additional Resources",
    "Source:", "Published:", "Featured Article", "Summary", "Overview"
]

noise_embeddings = embedding_model.encode(noise_examples, convert_to_tensor=True)


def is_noise(chunk, threshold=0.7):
    """
    Determines if a chunk is noise based on semantic similarity to known boilerplate examples.
    """
    chunk_embedding = embedding_model.encode(chunk, convert_to_tensor=True)
    similarities = util.cos_sim(chunk_embedding, noise_embeddings)
    max_similarity = similarities.max().item()
    return max_similarity > threshold


def clean_chunk(chunk):
    """
    Cleans a chunk by removing noise through heuristic checks and semantic similarity.
    """
    chunk = chunk.strip()

    # Heuristic cleaning: remove empty, short, or special character-heavy chunks
    if not chunk or len(chunk) < 10:
        return None
    if len(re.findall(r"[^\w\s]", chunk)) > len(chunk) * 0.3:  # Too many special characters
        return None
    if len(chunk.split()) < 5:  # Too few words
        return None

    # Semantic cleaning: remove chunks similar to boilerplate examples
    if is_noise(chunk, threshold=0.7):
        return None

    return chunk


def split_text_into_chunks(text, max_tokens=30, overlap=1):
    """
    Splits text into chunks based on sentence boundaries, token limits, and overlap.
    Cleans chunks before adding them to the final list.
    """
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        token_count = len(nlp(sentence))

        if current_length + token_count <= max_tokens:
            current_chunk.append(sentence)
            current_length += token_count
        else:
            raw_chunk = " ".join(current_chunk)
            cleaned_chunk = clean_chunk(raw_chunk)
            if cleaned_chunk:
                chunks.append(cleaned_chunk)

            # Start new chunk with overlap
            current_chunk = current_chunk[-overlap:] if overlap > 0 else []
            current_chunk.append(sentence)
            current_length = token_count

    # Add the final chunk
    if current_chunk:
        raw_chunk = " ".join(current_chunk)
        cleaned_chunk = clean_chunk(raw_chunk)
        if cleaned_chunk:
            chunks.append(cleaned_chunk)

    return chunks


def process_loaded_documents(documents, max_tokens=30, overlap=1):
    """
    Processes a list of documents (loaded via PyPDFLoader) and splits their pages into cleaned chunks.
    Returns a dictionary with document metadata and chunks.
    """
    all_chunks = {}

    for doc_index, document in enumerate(documents):
        doc_chunks = []

        for page_index, page in enumerate(document):
            text = page.page_content
            chunks = split_text_into_chunks(text, max_tokens, overlap)

            for i, chunk in enumerate(chunks):
                doc_chunks.append({
                    "page": page_index + 1,
                    "chunk_number": i + 1,
                    "chunk": chunk
                })

        all_chunks[f"Document_{doc_index + 1}"] = doc_chunks

    return all_chunks
