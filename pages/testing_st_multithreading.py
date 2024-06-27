import streamlit as st
import redis
from functions import hash_pwd, sign_up
import time
import threading
from typing import Any, TypeVar, cast

st.set_page_config(
    page_title="Testing",
    page_icon="🔥",
)

from streamlit.errors import NoSessionContext
from streamlit.runtime.scriptrunner.script_run_context import (
    SCRIPT_RUN_CONTEXT_ATTR_NAME,
    get_script_run_ctx,
)

T = TypeVar("T")


def with_streamlit_context(fn: T) -> T:
    """Fix bug in streamlit which raises streamlit.errors.NoSessionContext."""
    ctx = get_script_run_ctx()

    if ctx is None:
        raise NoSessionContext(
            "with_streamlit_context must be called inside a context; "
            "construct your function on the fly, not earlier."
        )

    def _cb(*args: Any, **kwargs: Any) -> Any:
        """Do it."""

        thread = threading.current_thread()
        do_nothing = hasattr(thread, SCRIPT_RUN_CONTEXT_ATTR_NAME) and (
            getattr(thread, SCRIPT_RUN_CONTEXT_ATTR_NAME) == ctx
        )

        if not do_nothing:
            setattr(thread, SCRIPT_RUN_CONTEXT_ATTR_NAME, ctx)

        # Call the callback.
        ret = fn(*args, **kwargs)

        if not do_nothing:
            # Why delattr? Because tasks for different users may be done by
            # the same thread at different times. Danger danger.
            delattr(thread, SCRIPT_RUN_CONTEXT_ATTR_NAME)
        return ret

    return cast(T, _cb)

panel = st.container(height=100)

def do_work(callback, data):
    nums = [n for n in range(1, data + 1)]
    callback(nums)
        
def report_progress(args):
    with panel:
        st.write(str(args))

val = st.slider("Value", 0, 50, 0)

@with_streamlit_context
def my_callback(*args):
    report_progress(*args)

thread = threading.Thread(target=do_work, kwargs={"callback":my_callback, "data": val})
thread.start()
thread.join()



#Testing multithreading
'Loading chat page'
#def my_handler(message):
        #print('MY HANDLER: ', message['data'])
        #st.write(message['data'])
        #st.session_state.bob.append(message['data'])
#st.session_state.pub = st.session_state.r.pubsub()
#st.session_state.pub.subscribe(**{'my-channel': my_handler})
#pub.get_message()
#thread = st.session_state.pub.run_in_thread(sleep_time=0.001)
#add_script_run_ctx(thread)
#add_script_run_ctx(thread)
