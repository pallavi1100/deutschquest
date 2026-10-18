"""Offline UI smoke test, with Streamlit mocked because runtime is not available here."""
import importlib
import runpy
import sys
import types

class State(dict):
    __getattr__ = dict.__getitem__
    def __setattr__(self, k, v): self[k] = v

class Block:
    def __enter__(self): return self
    def __exit__(self, *a): return False

fake_st = types.ModuleType("streamlit")
fake_st.__path__ = []
fake_st.session_state = State()
ignore = lambda *args, **kwargs: None
for name in ('set_page_config','markdown','title','subheader','write','progress','info','warning','success','error','caption','audio'):
    setattr(fake_st,name,ignore)
for name in ('container','expander'):
    setattr(fake_st,name,lambda *args,**kwargs:Block())
fake_st.columns = lambda n, **kw: [Block() for _ in range(n if isinstance(n,int) else len(n))]
fake_st.button = lambda *args,**kwargs: False
fake_st.radio = lambda *args,**kwargs: None
fake_st.toggle = lambda label,value=False,**kw: value
fake_st.selectbox = lambda label,options,index=0,**kw: options[index]
fake_st.text_input = lambda *args,**kwargs: ""
fake_st.audio_input = lambda *args,**kwargs: None
fake_st.rerun = lambda: None

comp = types.ModuleType('streamlit.components')
comp.__path__ = []
comp_v1 = types.ModuleType('streamlit.components.v1')
comp_v1.html = ignore
fake_st.components=comp
comp.v1=comp_v1
sys.modules['streamlit']=fake_st
sys.modules['streamlit.components']=comp
sys.modules['streamlit.components.v1']=comp_v1
mr = types.ModuleType('streamlit_mic_recorder')
mr.speech_to_text = ignore
sys.modules['streamlit_mic_recorder']=mr

# Minimal copy of existing starter schema to exercise conditional pages
lessons = types.ModuleType('lessons')
lessons.MISSIONS = [{"id":f"starter{i}","title":"Hallo", "emoji":"👋","location":"Main Street", "subtitle":"Hello", "grammar":"sein", "questions":[{"prompt":"Choose", "options":["wrong","right","wrong"],"answer":1,"grammar":"Sein rule","example":"Ich bin hier."}]} for i in range(5)]
sys.modules['lessons']=lessons

if __name__ == '__main__':
    for screen in ['lobby','map','quiz','results','voice','progress']:
        fake_st.session_state.clear()
        fake_st.session_state['screen']=screen
        fake_st.session_state['hero']='LENA'
        runpy.run_path('app.py',run_name=f'__test_{screen}__')
        print(f'{screen}: OK')
    # Render all supported question types
    from bonus_lessons import EXTRA_MISSIONS
    for mode in ['choice','type','order','listen']:
        q=next(x for m in EXTRA_MISSIONS for x in m['questions'] if x.get('mode')==mode)
        fake_st.session_state.clear()
        fake_st.session_state['screen']='quiz'
        lessons.MISSIONS=[{"id":"test","title":"Test","emoji":"🧠","location":"Area","subtitle":"Quest","grammar":"grammar","questions":[q]}]
        runpy.run_path('app.py',run_name='__test_q__')
        print(f'{mode} question: OK')
