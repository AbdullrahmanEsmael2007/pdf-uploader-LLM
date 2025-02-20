from sentence_transformers import SentenceTransformer, util

# Load lightweight embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Define common boilerplate examples (noise anchors)
noise_examples = [
    "Page 4", "Error fetching Wikipedia article", "Retrieved from Wikipedia",
    "may refer to:", "Contents", "See also", "External links"
]
noise_embeddings = model.encode(noise_examples, convert_to_tensor=True)

def is_noise(chunk, threshold=0.7):
    """
    Determines if a chunk is noise based on semantic similarity to known boilerplate examples.
    """
    chunk_embedding = model.encode(chunk, convert_to_tensor=True)
    # Calculate cosine similarity between the chunk and all noise examples
    similarities = util.cos_sim(chunk_embedding, noise_embeddings)
    max_similarity = similarities.max().item()  # Get the highest similarity score
    return max_similarity > threshold

# Example chunks
chunks = [
    "Page 4",
    "Error fetching Wikipedia article",
    "The company was founded in 2000 and expanded globally.",
    "Retrieved from Wikipedia",
    "This document may refer to something.",
    "It quickly expanded globally with new products."
]

# Filter out noise chunks
cleaned_chunks = [chunk for chunk in chunks if not is_noise(chunk)]

# Result
for i, chunk in enumerate(cleaned_chunks, 1):
    print(f"Chunk {i}: {chunk}")
