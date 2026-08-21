import re
from collections import defaultdict

def tokenize(text: str) -> set:
    """Extract normalized lowercase word tokens from text."""
    if not text:
        return set()
    words = re.findall(r'[a-zA-Z0-9]+', text.lower())
    # filter very short stopwords
    stopwords = {'a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'is', 'it'}
    return {w for w in words if len(w) > 1 and w not in stopwords}

class MaterialSearchIndex:
    """Inverted search index for study materials."""
    def __init__(self):
        self.index = defaultdict(set)
        self.documents = {}

    def add_document(self, doc_id: str, doc_data: dict):
        """Index a document with title, subject, tags, and description."""
        self.documents[doc_id] = doc_data
        combined_text = f"{doc_data.get('title', '')} {doc_data.get('subject', '')} {doc_data.get('topic', '')} {' '.join(doc_data.get('tags', []))} {doc_data.get('description', '')}"
        tokens = tokenize(combined_text)
        for token in tokens:
            self.index[token].add(doc_id)

    def search(self, query: str, branch: str = None, semester: int = None) -> list:
        """Search documents matching query with optional branch/semester filter."""
        query_tokens = tokenize(query)
        if not query_tokens:
            results = list(self.documents.values())
        else:
            match_counts = defaultdict(int)
            for token in query_tokens:
                # exact token match
                if token in self.index:
                    for doc_id in self.index[token]:
                        match_counts[doc_id] += 3
                # substring/prefix match
                for idx_token, doc_ids in self.index.items():
                    if token != idx_token and (token in idx_token or idx_token in token):
                        for doc_id in doc_ids:
                            match_counts[doc_id] += 1

            matched_ids = sorted(match_counts.keys(), key=lambda d: match_counts[d], reverse=True)
            results = [self.documents[d] for d in matched_ids]

        if branch:
            results = [r for r in results if r.get('branch') in (branch, 'All', 'General')]
        if semester:
            results = [r for r in results if r.get('semester') == semester or r.get('semester') == 'All']

        return results
