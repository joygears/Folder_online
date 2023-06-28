#pragma once


#include <Windows.h>
#include <iostream>
#include <list>
#include <mutex>
using namespace std;

#define DLL_EXPORT extern "C" __declspec( dllexport )

extern string license;
extern string g_session_id;



// The encryption scheme. The definitions are from ISO/IEC 23001-7:2016.
enum class EncryptionScheme : uint32_t {
    kUnencrypted = 0,
    kCenc,  // 'cenc' subsample encryption using AES-CTR mode.
    kCbcs   // 'cbcs' pattern encryption using AES-CBC mode.
};
struct SubsampleEntry {
    uint32_t clear_bytes;
    uint32_t cipher_bytes;
};
struct Pattern {
    uint32_t crypt_byte_block;  // Count of the encrypted blocks.
    uint32_t skip_byte_block;   // Count of the unencrypted blocks.
};
struct InputBuffer_2 {
    const uint8_t* data;  // Pointer to the beginning of the input data.
    uint32_t data_size;   // Size (in bytes) of |data|.

    EncryptionScheme encryption_scheme;

    const uint8_t* key_id;  // Key ID to identify the decryption key.
    uint32_t key_id_size;   // Size (in bytes) of |key_id|.
    uint32_t : 32;          // Padding.

    const uint8_t* iv;  // Initialization vector.
    uint32_t iv_size;   // Size (in bytes) of |iv|.
    uint32_t : 32;      // Padding.

    const struct SubsampleEntry* subsamples;
    uint32_t num_subsamples;  // Number of subsamples in |subsamples|.
    uint32_t : 32;            // Padding.

                              // |pattern| is required if |encryption_scheme| specifies pattern encryption.
    Pattern pattern;

    int64_t timestamp;  // Presentation timestamp in microseconds.
};


struct VideoDecoderConfig {
    int codec;
    int profile;
    int alpha_mode;
    int color_space;
    int width;
    int height;
    int m_18;
    int m_1C;
    int m_20;
};

class Buffer {
public:
    // Destroys the buffer in the same context as it was created.
    virtual void Destroy() = 0;
    virtual uint32_t Capacity() const = 0;
    virtual uint8_t* Data() = 0;
    virtual void SetSize(uint32_t size) = 0;
    virtual uint32_t Size() const = 0;
protected:
    Buffer() {}
    virtual ~Buffer() {}
private:
    Buffer(const Buffer&);
    void operator=(const Buffer&);
};

class DecryptedBlock {
public:
    virtual void SetDecryptedBuffer(Buffer* buffer) = 0;
    virtual Buffer* DecryptedBuffer() = 0;
    // TODO(tomfinegan): Figure out if timestamp is really needed. If it is not,
    // we can just pass Buffer pointers around.
    virtual void SetTimestamp(int64_t timestamp) = 0;
    virtual int64_t Timestamp() const = 0;
protected:
    DecryptedBlock() {}
    virtual ~DecryptedBlock() {}
};

class DecryptedProxyBlock : public DecryptedBlock {
public:
    void SetDecryptedBuffer(Buffer* buffer) override;
    Buffer* DecryptedBuffer() override;

    void SetTimestamp(int64_t timestamp) override;
    int64_t Timestamp() const override;

    DecryptedProxyBlock() = default;

    ~DecryptedProxyBlock() override = default;

private:
    int64_t ts = 0;
    Buffer* buf = nullptr;

};

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



extern bool (*VerifyCdmHost_0)(verifyWrap*, int flag);
extern void (*_InitializeCdmModule_4)();
extern void*  (*_CreateCdmInstance)(int interface_version, const char* key_system, uint32_t key_system_len,
	void* host_function, void* extra_data);
extern void  (*_DeinitializeCdmModule)();
extern char* (*_GetCdmVersion)();
extern void* (*originHostFunction)(int host_version, void* user_data);
extern void* HostFunction(int host_version, void* user_data);


DLL_EXPORT void InitializeCdmModule_4();
DLL_EXPORT void* CreateCdmInstance(int interface_version, const char* key_system, uint32_t key_system_len,
	void * host_function, void* extra_data);
DLL_EXPORT void  DeinitializeCdmModule();
DLL_EXPORT char* GetCdmVersion();



class  ContentDecryptionModule_10 {
public:
    
    virtual void Initialize(bool allow_distinctive_identifier,
        bool allow_persistent_state,bool flag) = 0;

    // Gets the key status if the CDM has a hypothetical key with the |policy|.
    // The CDM must respond by calling either Host::OnResolveKeyStatusPromise()
    // with the result key status or Host::OnRejectPromise() if an unexpected
    // error happened or this method is not supported.
    virtual void GetStatusForPolicy(uint32_t promise_id,
        int* policy) = 0;

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
        DecryptedBlock* decrypted_buffer) = 0;

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

    ContentDecryptionModule_10() {}
    virtual ~ContentDecryptionModule_10() {};
 
};

class cdmHost;

class  MyContentDecryptionModuleProxy:ContentDecryptionModule_10 {
public:

    virtual void Initialize(bool allow_distinctive_identifier,
        bool allow_persistent_state, bool flag);


    virtual void GetStatusForPolicy(uint32_t promise_id,
        int* policy);

    virtual void SetServerCertificate(uint32_t promise_id,
        const uint8_t* server_certificate_data,
        uint32_t server_certificate_data_size);

    virtual void CreateSessionAndGenerateRequest(uint32_t promise_id,
        int session_type,
        int init_data_type,
        const uint8_t* init_data,
        uint32_t init_data_size);


    virtual void LoadSession(uint32_t promise_id,
        int session_type,
        const char* session_id,
        uint32_t session_id_size);

  
    virtual void UpdateSession(uint32_t promise_id,
        const char* session_id,
        uint32_t session_id_size,
        const uint8_t* response,
        uint32_t response_size);


    virtual void CloseSession(uint32_t promise_id,
        const char* session_id,
        uint32_t session_id_size);


    virtual void RemoveSession(uint32_t promise_id,
        const char* session_id,
        uint32_t session_id_size);

    virtual void TimerExpired(void* context);

   
    virtual int Decrypt(void* encrypted_buffer,
        DecryptedBlock* decrypted_buffer);

   
    virtual int InitializeAudioDecoder(
        void* audio_decoder_config);

   
    virtual int InitializeVideoDecoder(
        void* video_decoder_config);

   
    virtual void DeinitializeDecoder(int decoder_type);

    
    virtual void ResetDecoder(int decoder_type);

    
    virtual int DecryptAndDecodeFrame(const void* encrypted_buffer,
        void* video_frame);

  
    virtual int DecryptAndDecodeSamples(void* encrypted_buffer,
        void* audio_frames);

    virtual void OnPlatformChallengeResponse(
        void* response);

    virtual void OnQueryOutputProtectionStatus(
        int result,
        uint32_t link_mask,
        uint32_t output_protection_mask);

    virtual void OnStorageId(uint32_t version,
        const uint8_t* storage_id,
        uint32_t storage_id_size);

 
    virtual void Destroy();
    std::string getLink_maskMean(int link_mask);
    std::string getOutput_protection_mean(int output_protection_mask);
    void setHost(cdmHost* host);
    explicit  MyContentDecryptionModuleProxy(ContentDecryptionModule_10* instance);
    virtual ~MyContentDecryptionModuleProxy();
private:
    ContentDecryptionModule_10* m_instance;
    cdmHost* m_host;
    FILE * mDecFile;
    std::mutex m_mtx;
    std::string m_d4;
    std::string m_baseServerCertificate;
    friend class cdmHost;
private:
    static std::list<MyContentDecryptionModuleProxy*> g_listInstance;
    static std::mutex g_mtx;
};


