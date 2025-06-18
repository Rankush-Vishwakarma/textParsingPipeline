import hashlib
import io

def compute_file_hash(content):
    return hashlib.sha256(content).hexdigest()
