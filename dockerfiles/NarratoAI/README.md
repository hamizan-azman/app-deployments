# NarratoAI

Pull pre-built image:
```bash
docker pull hoomzoom/narratoai
docker run -d -p 9000:8501 hoomzoom/narratoai
```

## Dockerfile
Uses the original repo's Dockerfile with one change: swapped the Chinese pip mirror
(`pypi.tuna.tsinghua.edu.cn`) for default PyPI. No other modifications.

To rebuild from source:
```bash
git clone https://github.com/linyqh/NarratoAI
cd NarratoAI
# Optionally edit Dockerfile to change pip mirror
docker build -t narratoai .
```

See `docs/NarratoAI_reasoning.md` for full details on what was changed and why.
