#pragma once


#include <Windows.h>
#include <iostream>

using namespace std;

#define DLL_EXPORT extern "C" __declspec( dllexport )

struct verifyWrap {
	const wchar_t* chDycVfchm;
	HANDLE hFVfchm;
	HANDLE hSigVfchm;
	const wchar_t* chdycWidevine;
	HANDLE HDycWidevinecdm;
	HANDLE HSigWidevinecdm;
};

// ContentDecryptionModule interface that all CDMs need to implement.
// The interface is versioned for backward compatibility.
// Note: ContentDecryptionModule implementations must use the allocator
// provided in CreateCdmInstance() to allocate any Buffer that needs to
// be passed back to the caller. Implementations must call Buffer::Destroy()
// when a Buffer is created that will never be returned to the caller.



bool (*VerifyCdmHost_0)(verifyWrap*, int flag);
void (*_InitializeCdmModule_4)();
void*  (*_CreateCdmInstance)(int interface_version, const char* key_system, uint32_t key_system_len,
	void* host_function, void* extra_data);
void  (*_DeinitializeCdmModule)();
char* (*_GetCdmVersion)();

DLL_EXPORT void InitializeCdmModule_4();
DLL_EXPORT void* CreateCdmInstance(int interface_version, const char* key_system, uint32_t key_system_len,
	void * host_function, void* extra_data);
DLL_EXPORT void  DeinitializeCdmModule();
DLL_EXPORT char* GetCdmVersion();



class  ContentDecryptionModule_9 {
public:
    static const int kVersion = 9;
   
    virtual void Initialize(bool allow_distinctive_identifier,
        bool allow_persistent_state,bool flag) = 0;

    // Gets the key status if the CDM has a hypothetical key with the |policy|.
    // The CDM must respond by calling either Host::OnResolveKeyStatusPromise()
    // with the result key status or Host::OnRejectPromise() if an unexpected
    // error happened or this method is not supported.
    virtual void GetStatusForPolicy(uint32_t promise_id,
        void* policy) = 0;

    // SetServerCertificate(), CreateSessionAndGenerateRequest(), LoadSession(),
    // UpdateSession(), CloseSession(), and RemoveSession() all accept a
    // |promise_id|, which must be passed to the completion Host method
    // (e.g. Host::OnResolveNewSessionPromise()).

    // Provides a server certificate to be used to encrypt messages to the
    // license server. The CDM must respond by calling either
    // Host::OnResolvePromise() or Host::OnRejectPromise().
    virtual void SetServerCertificate(uint32_t promise_id,
        const uint8_t* server_certificate_data,
        uint32_t server_certificate_data_size) = 0;

    // Creates a session given |session_type|, |init_data_type|, and |init_data|.
    // The CDM must respond by calling either Host::OnResolveNewSessionPromise()
    // or Host::OnRejectPromise().
    virtual void CreateSessionAndGenerateRequest(uint32_t promise_id,
        int session_type,
        int init_data_type,
        const uint8_t* init_data,
        uint32_t init_data_size) = 0;

    // Loads the session of type |session_type| specified by |session_id|.
    // The CDM must respond by calling either Host::OnResolveNewSessionPromise()
    // or Host::OnRejectPromise(). If the session is not found, call
    // Host::OnResolveNewSessionPromise() with session_id = NULL.
    virtual void LoadSession(uint32_t promise_id,
        int session_type,
        const char* session_id,
        uint32_t session_id_size) = 0;

    // Updates the session with |response|. The CDM must respond by calling
    // either Host::OnResolvePromise() or Host::OnRejectPromise().
    virtual void UpdateSession(uint32_t promise_id,
        const char* session_id,
        uint32_t session_id_size,
        const uint8_t* response,
        uint32_t response_size) = 0;

    // Requests that the CDM close the session. The CDM must respond by calling
    // either Host::OnResolvePromise() or Host::OnRejectPromise() when the request
    // has been processed. This may be before the session is closed. Once the
    // session is closed, Host::OnSessionClosed() must also be called.
    virtual void CloseSession(uint32_t promise_id,
        const char* session_id,
        uint32_t session_id_size) = 0;

    // Removes any stored session data associated with this session. Will only be
    // called for persistent sessions. The CDM must respond by calling either
    // Host::OnResolvePromise() or Host::OnRejectPromise() when the request has
    // been processed.
    virtual void RemoveSession(uint32_t promise_id,
        const char* session_id,
        uint32_t session_id_size) = 0;

    // Performs scheduled operation with |context| when the timer fires.
    virtual void TimerExpired(void* context) = 0;

    // Decrypts the |encrypted_buffer|.
    //
    // Returns kSuccess if decryption succeeded, in which case the callee
    // should have filled the |decrypted_buffer| and passed the ownership of
    // |data| in |decrypted_buffer| to the caller.
    // Returns kNoKey if the CDM did not have the necessary decryption key
    // to decrypt.
    // Returns kDecryptError if any other error happened.
    // If the return value is not kSuccess, |decrypted_buffer| should be ignored
    // by the caller.
    virtual int Decrypt(void * encrypted_buffer,
        void * decrypted_buffer) = 0;

    // Initializes the CDM audio decoder with |audio_decoder_config|. This
    // function must be called before DecryptAndDecodeSamples() is called.
    //
    // Returns kSuccess if the |audio_decoder_config| is supported and the CDM
    // audio decoder is successfully initialized.
    // Returns kInitializationError if |audio_decoder_config| is not supported.
    // The CDM may still be able to do Decrypt().
    // Returns kDeferredInitialization if the CDM is not ready to initialize the
    // decoder at this time. Must call Host::OnDeferredInitializationDone() once
    // initialization is complete.
    virtual int InitializeAudioDecoder(
       void * audio_decoder_config) = 0;

    // Initializes the CDM video decoder with |video_decoder_config|. This
    // function must be called before DecryptAndDecodeFrame() is called.
    //
    // Returns kSuccess if the |video_decoder_config| is supported and the CDM
    // video decoder is successfully initialized.
    // Returns kInitializationError if |video_decoder_config| is not supported.
    // The CDM may still be able to do Decrypt().
    // Returns kDeferredInitialization if the CDM is not ready to initialize the
    // decoder at this time. Must call Host::OnDeferredInitializationDone() once
    // initialization is complete.
    virtual int InitializeVideoDecoder(
         void * video_decoder_config) = 0;

    // De-initializes the CDM decoder and sets it to an uninitialized state. The
    // caller can initialize the decoder again after this call to re-initialize
    // it. This can be used to reconfigure the decoder if the configuration
    // changes.
    virtual void DeinitializeDecoder(int decoder_type) = 0;

    // Resets the CDM decoder to an initialized clean state. All internal buffers
    // MUST be flushed.
    virtual void ResetDecoder(int decoder_type) = 0;

    // Decrypts the |encrypted_buffer| and decodes the decrypted buffer into a
    // |video_frame|. Upon end-of-stream, the caller should call this function
    // repeatedly with empty |encrypted_buffer| (|data| == NULL) until only empty
    // |video_frame| (|format| == kEmptyVideoFrame) is produced.
    //
    // Returns kSuccess if decryption and decoding both succeeded, in which case
    // the callee will have filled the |video_frame| and passed the ownership of
    // |frame_buffer| in |video_frame| to the caller.
    // Returns kNoKey if the CDM did not have the necessary decryption key
    // to decrypt.
    // Returns kNeedMoreData if more data was needed by the decoder to generate
    // a decoded frame (e.g. during initialization and end-of-stream).
    // Returns kDecryptError if any decryption error happened.
    // Returns kDecodeError if any decoding error happened.
    // If the return value is not kSuccess, |video_frame| should be ignored by
    // the caller.
    virtual int DecryptAndDecodeFrame(const void * encrypted_buffer,
        void * video_frame) = 0;

    // Decrypts the |encrypted_buffer| and decodes the decrypted buffer into
    // |audio_frames|. Upon end-of-stream, the caller should call this function
    // repeatedly with empty |encrypted_buffer| (|data| == NULL) until only empty
    // |audio_frames| is produced.
    //
    // Returns kSuccess if decryption and decoding both succeeded, in which case
    // the callee will have filled |audio_frames| and passed the ownership of
    // |data| in |audio_frames| to the caller.
    // Returns kNoKey if the CDM did not have the necessary decryption key
    // to decrypt.
    // Returns kNeedMoreData if more data was needed by the decoder to generate
    // audio samples (e.g. during initialization and end-of-stream).
    // Returns kDecryptError if any decryption error happened.
    // Returns kDecodeError if any decoding error happened.
    // If the return value is not kSuccess, |audio_frames| should be ignored by
    // the caller.
    virtual int DecryptAndDecodeSamples(void * encrypted_buffer,
        void * audio_frames) = 0;

    // Called by the host after a platform challenge was initiated via
    // Host::SendPlatformChallenge().
    virtual void OnPlatformChallengeResponse(
        void * response) = 0;

    // Called by the host after a call to Host::QueryOutputProtectionStatus(). The
    // |link_mask| is a bit mask of OutputLinkTypes and |output_protection_mask|
    // is a bit mask of OutputProtectionMethods. If |result| is kQueryFailed,
    // then |link_mask| and |output_protection_mask| are undefined and should
    // be ignored.
    virtual void OnQueryOutputProtectionStatus(
        int result,
        uint32_t link_mask,
        uint32_t output_protection_mask) = 0;

    // Called by the host after a call to Host::RequestStorageId(). If the
    // version of the storage ID requested is available, |storage_id| and
    // |storage_id_size| are set appropriately. |version| will be the same as
    // what was requested, unless 0 (latest) was requested, in which case
    // |version| will be the actual version number for the |storage_id| returned.
    // If the requested version is not available, null/zero will be provided as
    // |storage_id| and |storage_id_size|, respectively, and |version| should be
    // ignored.
    virtual void OnStorageId(uint32_t version,
        const uint8_t* storage_id,
        uint32_t storage_id_size) = 0;

    // Destroys the object in the same context as it was created.
    virtual void Destroy() = 0;

protected:
    ContentDecryptionModule_9() {}
    virtual ~ContentDecryptionModule_9() {}
};
