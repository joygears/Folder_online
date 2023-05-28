#include "cdmHost.h"
#include "fucntion.h"

void* cdmHost::Allocate(int capacity)
{

    if (m_host) {
        void* buf =  m_host->Allocate(capacity);
        Log("Host::Allocate, %u, %p", capacity, buf);
        return buf;
    }
    return nullptr;
}

void cdmHost::SetTimer(__int64 delay_ms, void* context)
{
    Log("Host::SetTimer: %p, %lld", context, delay_ms);
    if (m_host) {
        m_host->SetTimer(delay_ms, context);
    }
    else {
        m_context = context;
    }
  
}

__time64_t cdmHost::GetCurrentWallTime()
{
    Log("Host::GetCurrentWallTime");
   
    if (!m_host)
        return _time64(0);
    
    return m_host->GetCurrentWallTime();
}

void cdmHost::OnInitialized(bool success)
{

    Log("Host::OnInitialized, %d", success);
  
    if (m_host)
        m_host->OnInitialized(success);

}

void cdmHost::OnResolveKeyStatusPromise(int promise_id, int key_status)
{
    

    v4 = promise_id;
    Log("Host::OnResolveKeyStatusPromise, promise_id %d, %d", promise_id, key_status);
   
    m_mtx.lock();

    v6 = (_DWORD*)this[11];
    v7 = v6;
    v8 = (int*)v6[1];
    while (!*((_BYTE*)v8 + 13))
    {
        if (v8[4] >= v4)
        {
            v7 = v8;
            v8 = (int*)*v8;
        }
        else
        {
            v8 = (int*)v8[2];
        }
    }
    if (v7 == v6 || v4 < v7[4])
        v7 = (_DWORD*)this[11];
    if (v7 != (_DWORD*)this[11])
        sub_1005AD10((int)&promise_id, v7);
    if (promise_id != -1)
    {
        if (m_host)
            m_host->OnResolveKeyStatusPromise(promise_id, key_status);
    }

    m_mtx.unlock();
}

