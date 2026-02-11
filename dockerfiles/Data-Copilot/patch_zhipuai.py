"""Patch lab_llms_call.py to handle zhipuai v2/pydantic v1 conflict."""
p = '/app/lab_llms_call.py'
t = open(p).read()

old_import = "from zhipuai import ZhipuAI"
new_import = """try:
    from zhipuai import ZhipuAI
except Exception:
    ZhipuAI = None"""

old_client = 'client = ZhipuAI(api_key="<your api key>")'
new_client = 'client = ZhipuAI(api_key="<your api key>") if ZhipuAI else None'

t = t.replace(old_import, new_import)
t = t.replace(old_client, new_client)
open(p, 'w').write(t)
