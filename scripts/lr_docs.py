"""LightRAG document listing helper (POST /documents/paginated).
Replaces the legacy GET /documents, which was removed in LightRAG v1.5.7."""
import json, urllib.request

def list_docs(base_url, token, status='processed', page_size=200):
    docs, page = [], 1
    while True:
        body = json.dumps({'status_filter': status, 'page': page, 'page_size': page_size,
                           'sort_field': 'updated_at', 'sort_direction': 'desc'}).encode()
        req = urllib.request.Request(f'{base_url}/documents/paginated', data=body, method='POST',
                                     headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as resp:
            d = json.load(resp)
        batch = d.get('documents', [])
        docs.extend(batch)
        p = d.get('pagination', {})
        if not batch or not p.get('has_next', False):
            break
        page += 1
    return docs

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/docker/lightrag/scripts')
    import mcp_remote as m
    ds = list_docs('http://127.0.0.1:9621', m.get_token())
    print(len(ds), sorted(ds[0].keys()) if ds else None)
