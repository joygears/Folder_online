#pragma once
#include <time.h>
#include <mutex>
#include <map>

typedef unsigned int uint32_t;


class  Host {
public:
    // Returns a Buffer* containing non-zero members upon success, or NULL on
    // failure. The caller owns the Buffer* after this call. The buffer is not
    // guaranteed to be zero initialized. The capacity of the allocated Buffer
    // is guaranteed to be not less than |capacity|.
    virtual void * Allocate(int capacity) = 0;

    // Requests the host to call ContentDecryptionModule::TimerFired() |delay_ms|
    // from now with |context|.
    virtual void SetTimer(__int64 delay_ms, void* context) = 0;

    // Returns the current wall time.
    virtual __time64_t GetCurrentWallTime() = 0;

    // Called by the CDM with the result after the CDM instance was initialized.
    virtual void OnInitialized(bool success) = 0;

    // Called by the CDM when a key status is available in response to
    // GetStatusForPolicy().
    virtual void OnResolveKeyStatusPromise(int promise_id,
        int key_status) = 0;

    // Called by the CDM when a session is created or loaded and the value for the
    // MediaKeySession's sessionId attribute is available (|session_id|).
    // This must be called before OnSessionMessage() or
    // OnSessionKeysChange() is called for the same session. |session_id_size|
    // should not include null termination.
    // When called in response to LoadSession(), the |session_id| must be the
    // same as the |session_id| passed in LoadSession(), or NULL if the
    // session could not be loaded.
    virtual void OnResolveNewSessionPromise(int promise_id,
        const char* session_id,
        int session_id_size) = 0;

    // Called by the CDM when a session is updated or released.
    virtual void OnResolvePromise(int promise_id) = 0;

    // Called by the CDM when an error occurs as a result of one of the
    // ContentDecryptionModule calls that accept a |promise_id|.
    // |exception| must be specified. |error_message| and |system_code|
    // are optional. |error_message_size| should not include null termination.
    virtual void OnRejectPromise(uint32_t promise_id,
        int exception,
        uint32_t system_code,
        const char* error_message,
        uint32_t error_message_size) = 0;

    // Called by the CDM when it has a message for session |session_id|.
    // Size parameters should not include null termination.
    virtual void OnSessionMessage(const char* session_id,
        uint32_t session_id_size,
        int message_type,
        const char* message,
        uint32_t message_size) = 0;

    // Called by the CDM when there has been a change in keys or their status for
    // session |session_id|. |has_additional_usable_key| should be set if a
    // key is newly usable (e.g. new key available, previously expired key has
    // been renewed, etc.) and the browser should attempt to resume playback.
    // |keys_info| is the list of key IDs for this session along with their
    // current status. |keys_info_count| is the number of entries in |keys_info|.
    // Size parameter for |session_id| should not include null termination.
    virtual void OnSessionKeysChange(const char* session_id,
        uint32_t session_id_size,
        bool has_additional_usable_key,
        const void * keys_info,
        uint32_t keys_info_count) = 0;

    // Called by the CDM when there has been a change in the expiration time for
    // session |session_id|. This can happen as the result of an Update() call
    // or some other event. If this happens as a result of a call to Update(),
    // it must be called before resolving the Update() promise. |new_expiry_time|
    // represents the time after which the key(s) in the session will no longer
    // be usable for decryption. It can be 0 if no such time exists or if the
    // license explicitly never expires. Size parameter should not include null
    // termination.
    virtual void OnExpirationChange(const char* session_id,
        uint32_t session_id_size,
        __time64_t new_expiry_time) = 0;

    // Called by the CDM when session |session_id| is closed. Size
    // parameter should not include null termination.
    virtual void OnSessionClosed(const char* session_id,
        uint32_t session_id_size) = 0;

    // The following are optional methods that may not be implemented on all
    // platforms.

    // Sends a platform challenge for the given |service_id|. |challenge| is at
    // most 256 bits of data to be signed. Once the challenge has been completed,
    // the host will call ContentDecryptionModule::OnPlatformChallengeResponse()
    // with the signed challenge response and platform certificate. Size
    // parameters should not include null termination.
    virtual void SendPlatformChallenge(const char* service_id,
        uint32_t service_id_size,
        const char* challenge,
        uint32_t challenge_size) = 0;

    // Attempts to enable output protection (e.g. HDCP) on the display link. The
    // |desired_protection_mask| is a bit mask of OutputProtectionMethods. No
    // status callback is issued, the CDM must call QueryOutputProtectionStatus()
    // periodically to ensure the desired protections are applied.
    virtual void EnableOutputProtection(uint32_t desired_protection_mask) = 0;

    // Requests the current output protection status. Once the host has the status
    // it will call ContentDecryptionModule::OnQueryOutputProtectionStatus().
    virtual void QueryOutputProtectionStatus() = 0;

    // Must be called by the CDM if it returned kDeferredInitialization during
    // InitializeAudioDecoder() or InitializeVideoDecoder().
    virtual void OnDeferredInitializationDone(int stream_type,
        int decoder_status) = 0;

    // Creates a FileIO object from the host to do file IO operation. Returns NULL
    // if a FileIO object cannot be obtained. Once a valid FileIO object is
    // returned, |client| must be valid until FileIO::Close() is called. The
    // CDM can call this method multiple times to operate on different files.
    virtual void * CreateFileIO(void  * client) = 0;

  

    // Requests a specific version of the storage ID. A storage ID is a stable,
    // device specific ID used by the CDM to securely store persistent data. The
    // ID will be returned by the host via ContentDecryptionModule::OnStorageId().
    // If |version| is 0, the latest version will be returned. All |version|s
    // that are greater than or equal to 0x80000000 are reserved for the CDM and
    // should not be supported or returned by the host. The CDM must not expose
    // the ID outside the client device, even in encrypted form.
    virtual void RequestStorageId(uint32_t version) = 0;

protected:
    Host() {}
    virtual ~Host() {}
};

class MyContentDecryptionModuleProxy;
class cdmHost
{
public:

    virtual void* Allocate(int capacity);

    // Requests the host to call ContentDecryptionModule::TimerFired() |delay_ms|
    // from now with |context|.
    virtual void SetTimer(__int64 delay_ms, void* context);

    // Returns the current wall time.
    virtual __time64_t GetCurrentWallTime();

    // Called by the CDM with the result after the CDM instance was initialized.
    virtual void OnInitialized(bool success);


    virtual void OnResolveKeyStatusPromise(int promise_id,
        int key_status);

    virtual void OnResolveNewSessionPromise(int promise_id,
        const char* session_id,
        int session_id_size);

    // Called by the CDM when a session is updated or released.
    virtual void OnResolvePromise(int promise_id);

    virtual void OnRejectPromise(uint32_t promise_id,
        int exception,
        uint32_t system_code,
        const char* error_message,
        uint32_t error_message_size);


    virtual void OnSessionMessage(const char* session_id,
        uint32_t session_id_size,
        int message_type,
        const char* message,
        uint32_t message_size);


    virtual void OnSessionKeysChange(const char* session_id,
        uint32_t session_id_size,
        bool has_additional_usable_key,
        const void* keys_info,
        uint32_t keys_info_count);

    virtual void OnExpirationChange(const char* session_id,
        uint32_t session_id_size,
        __time64_t new_expiry_time);

    virtual void OnSessionClosed(const char* session_id,
        uint32_t session_id_size);


    virtual void SendPlatformChallenge(const char* service_id,
        uint32_t service_id_size,
        const char* challenge,
        uint32_t challenge_size);


    virtual void EnableOutputProtection(uint32_t desired_protection_mask);


    virtual void QueryOutputProtectionStatus();

    virtual void OnDeferredInitializationDone(int stream_type,
        int decoder_status);

    virtual void* CreateFileIO(void* client);

    virtual void RequestStorageId(uint32_t version);

public:
    void setMapIdHdcp(int promise_id, std::string hdcp);
    cdmHost(Host * host):m_host(host){}
    virtual ~cdmHost() {}
private:
    Host* m_host;
    void* m_context;
    std::string m_session_id;
    std::map<int, std::string> m_24;
    std::map<int, std::string> m_mapIdHdcp;
    std::mutex m_mtx;
public:
    MyContentDecryptionModuleProxy* m_MyProxy;
};

extern cdmHost* g_CDMHost;
