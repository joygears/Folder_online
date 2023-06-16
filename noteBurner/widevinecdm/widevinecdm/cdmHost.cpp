#include "cdmHost.h"
#include "fucntion.h"
#include "widevinecdm.h"

CDMHostBuffer* cdmHost::Allocate(int capacity)
{

    if (m_host) {
        CDMHostBuffer* buf = (CDMHostBuffer*)m_host->Allocate(capacity);
        Log("Host::Allocate, %u, %p", capacity, buf);
        return buf;
    }

    return new CDMHostBuffer(capacity);
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



    Log("Host::OnResolveKeyStatusPromise, promise_id %d, %d", promise_id, key_status);

    m_mtx.lock();

    m_mapIdHdcp.erase(promise_id);

    if (promise_id != -1)
    {
        if (m_host)
            m_host->OnResolveKeyStatusPromise(promise_id, key_status);
    }

    m_mtx.unlock();
}

void cdmHost::OnResolveNewSessionPromise(int promise_id, const char* session_id, int session_id_size)
{


    Log("Host::OnResolveNewSessionPromise, %08x, %s", promise_id, (const char*)session_id);
    if (!m_host) {
        m_session_id = promise_id;
        return;
    }
    m_MyProxy->m_mtx.lock();



    m_MyProxy->m_mtx.unlock();
    m_host->OnResolveNewSessionPromise(promise_id, session_id, session_id_size);
}

void cdmHost::OnResolvePromise(int promise_id)
{


    Log("Host::OnResolvePromise, %08x", promise_id);

    if (m_host)
        m_host->OnResolvePromise(promise_id);
}

void cdmHost::OnRejectPromise(uint32_t promise_id, int exception, uint32_t system_code, const char* error_message, uint32_t error_message_size)
{


    Log("Host::OnRejectPromise, %08x %s", promise_id, (const char*)error_message);

    if (m_host)
        m_host->OnRejectPromise(
            promise_id,
            exception,
            system_code,
            error_message,
            error_message_size);
}

void cdmHost::OnSessionMessage(const char* session_id, uint32_t session_id_size, int message_type, const char* message, uint32_t message_size)
{
    Log(
        "[%08x] Host::OnSessionMessage, session_id %s, session_id_size %u, message_type %u, message_size %u, message %p ",
        this,
        (const char*)session_id,
        session_id_size,
        message_type,
        message_size,
        (const void*)message);

    Log("[KREQ]cdm normal mode process OnSessionMessage!");

    if (m_host) {

        m_host->OnSessionMessage(session_id, session_id_size, message_type, message, message_size);
    }
}

void cdmHost::OnSessionKeysChange(const char* session_id, uint32_t session_id_size, bool has_additional_usable_key, const void* keys_info, uint32_t keys_info_count)
{
    Log(
        "Host::OnSessionKeysChange, session_id %s, session_id_size %d, has_additional_usable_key %d, keys_info_count %u",
        (const char*)session_id,
        session_id_size,
        (unsigned __int8)has_additional_usable_key,
        keys_info_count);


    if (m_host) {

        m_host->OnSessionKeysChange(session_id, session_id_size, has_additional_usable_key, keys_info, keys_info_count);
    }
}

void cdmHost::OnExpirationChange(const char* session_id, uint32_t session_id_size, __time64_t new_expiry_time)
{

    Log("Host::OnExpirationChange, %s, %s", session_id, asctime(_gmtime64(&new_expiry_time)));
    if (m_host) {

        m_host->OnExpirationChange(session_id, session_id_size, new_expiry_time);
    }
}

void cdmHost::OnSessionClosed(const char* session_id, uint32_t session_id_size)
{
    Log("Host::OnSessionClosed, %s", session_id);
    if (m_host) {

        m_host->OnSessionClosed(session_id, session_id_size);
    }
}

void cdmHost::SendPlatformChallenge(const char* service_id, uint32_t service_id_size, const char* challenge, uint32_t challenge_size)
{
    Log("Host::SendPlatformChallenge", service_id, service_id_size, challenge, challenge_size);
    if (m_host) {

        m_host->SendPlatformChallenge(service_id, service_id_size, challenge, challenge_size);
    }
}

void cdmHost::EnableOutputProtection(uint32_t desired_protection_mask)
{
    Log("Host::EnableOutputProtection, %u", desired_protection_mask);
    if (m_host) {

        m_host->EnableOutputProtection(desired_protection_mask);
    }
}

void cdmHost::QueryOutputProtectionStatus()
{
    Log("Host::QueryOutputProtectionStatus");

    if (m_host)
        m_host->QueryOutputProtectionStatus();
}

void cdmHost::OnDeferredInitializationDone(int stream_type, int decoder_status)
{
    Log("Host::OnDeferredInitializationDone, %u, %u", stream_type, decoder_status);
    if (m_host)
        m_host->OnDeferredInitializationDone(stream_type, decoder_status);
}

void* cdmHost::CreateFileIO(void* client)
{
    Log("Host::CreateFileIO");
    if (m_host)
        return  m_host->CreateFileIO(client);
    return nullptr;
}

void cdmHost::RequestStorageId(uint32_t version)
{
    Log("Host::RequestStorageId, %u", version);
    if (m_host)
        m_host->RequestStorageId(version);
}

void cdmHost::setMapIdHdcp(int promise_id, std::string hdcp)
{
    m_mtx.lock();
    m_mapIdHdcp[promise_id] = hdcp;
    m_mtx.unlock();
}


cdmHost* g_CDMHost = 0;

CDMHostBuffer::CDMHostBuffer(size_t capacity)
{
    m_buffer = malloc(capacity);
    m_size = 0;
    m_capacity = capacity;

}

CDMHostBuffer::~CDMHostBuffer()
{
    free(m_buffer);
    m_buffer = 0;
}

void CDMHostBuffer::Destroy()
{
    delete this;
}

uint32_t CDMHostBuffer::Capacity() const
{
    return m_capacity;
}

uint8_t* CDMHostBuffer::Data()
{
    return (uint8_t*)m_buffer;
}

void CDMHostBuffer::SetSize(uint32_t size)
{
    m_size = size;

}

uint32_t CDMHostBuffer::Size() const
{
    return m_size;
}
