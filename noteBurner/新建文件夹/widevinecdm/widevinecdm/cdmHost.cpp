#include "cdmHost.h"
#include "fucntion.h"
#include "widevinecdm.h"
#include "base64.h"

string getLicense(string url ,string session_id, string challeageBase64) {
    std::string command = "getLicense.exe \"" + url +"\" " + session_id + " " + challeageBase64;
    std::string output = getCommandOutput(command);

    std::vector<std::string> lines = splitString(output, '\n');
    string license;
   
    for (const std::string& line : lines) {
        if (line.substr(0, 8) == "license:") {
            license = splitString(line, ':')[1];
        }
    }
    return license;
}

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

double cdmHost::GetCurrentWallTime()
{
    Log("Host::GetCurrentWallTime");

    if (!m_host)
        return (double)_time64(0);

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

    std::map<int, std::string>::iterator it = m_mapIdHdcp.find(promise_id);
    if (it != m_mapIdHdcp.end()) {
        Log( "%p, %08x, %s, status:%u", m_MyProxy, promise_id, it->second.c_str(), key_status);
        m_hdcpStatus[it->second] = key_status;
        m_mapIdHdcp.erase(it);
    }

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
    string url = "https://www.netflix.com/watch/81405170?trackId=15036064&tctx=3%2C1%2C524805d0-02c8-484c-9d97-3dbe4ce44a77-2104468%2CNES_743E7DB0564DECE5F267D736BB9848-A3F87CB3ABAB23-15A789EEBD_p_1689650198442%2CNES_743E7DB0564DECE5F267D736BB9848_p_1689647325866%2C%2C%2C%2C%2CVideo%3A81281579%2CdetailsPagePlayButton";
   
    Log(
        "[%08x] Host::OnSessionMessage, session_id %s, session_id_size %u, message_type %u, message_size %u, message %p ",
        this,
        (const char*)session_id,
        session_id_size,
        message_type,
        message_size,
        (const void*)message);
    string licenseRequest = base64_encode(string(message, message_size));
    Log("licenseRequest: %s",licenseRequest.c_str());
    g_session_id = session_id;
    license = getLicense(url,session_id, licenseRequest);
    Log("license: %s", license.c_str());
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

void cdmHost::OnExpirationChange(const char* session_id, uint32_t session_id_size, __int64  new_expiry_time)
{
    
    __int64 timestamp = (__int64)*(double*)&new_expiry_time;

 /*   __time64_t ttimestamp = (__int64)*(double*)&timestamp;
    struct tm* timeinfo = _gmtime64(&ttimestamp);
    int a = GetLastError();
    char buffer[80];

    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", timeinfo);*/
    Log("Host::OnExpirationChange, %s, %s", session_id, asctime(_gmtime64(&timestamp)));
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
