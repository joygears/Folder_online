#include <iostream>

class Size {
public:
    Size() : width(0), height(0) {}
    Size(int32_t width, int32_t height) : width(width), height(height) {}

    int32_t width;
    int32_t height;
};
// Surface formats based on FOURCC labels, see: http://www.fourcc.org/yuv.php
// Values are chosen to be consistent with Chromium's VideoPixelFormat values.
enum VideoFormat {
    kUnknownVideoFormat = 0,  // Unknown format value. Used for error reporting.
    kYv12 = 1,                // 12bpp YVU planar 1x1 Y, 2x2 VU samples.
    kI420 = 2,                // 12bpp YUV planar 1x1 Y, 2x2 UV samples.

    // In the following formats, each sample uses 16-bit in storage, while the
    // sample value is stored in the least significant N bits where N is
    // specified by the number after "P". For example, for YUV420P9, each Y, U,
    // and V sample is stored in the least significant 9 bits in a 2-byte block.
    kYUV420P9 = 16,
    kYUV420P10 = 17,
    kYUV422P9 = 18,
    kYUV422P10 = 19,
    kYUV444P9 = 20,
    kYUV444P10 = 21,
    kYUV420P12 = 22,
    kYUV422P12 = 23,
    kYUV444P12 = 24,
};

class  Buffer {
public:
    // Destroys the buffer in the same context as it was created.
    virtual void Destroy() = 0;

    virtual uint32_t Capacity() const = 0;
    virtual uint8_t* Data() = 0;
    virtual void SetSize(uint32_t size) = 0;
    virtual uint32_t Size() const = 0;

    Buffer() {}
    virtual ~Buffer() {}

private:
    Buffer(const Buffer&);
    void operator=(const Buffer&);
};
class  DecryptedBlock {
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

class  VideoFrame {
public:
    enum VideoPlane {
        kYPlane = 0,
        kUPlane = 1,
        kVPlane = 2,
        kMaxPlanes = 3,
    };

    virtual void SetFormat(VideoFormat format) = 0;
    virtual VideoFormat Format() const = 0;

    virtual void SetSize(Size size) = 0;
    virtual Size SSize() const = 0;

    virtual void SetFrameBuffer(Buffer* frame_buffer) = 0;
    virtual Buffer* FrameBuffer() = 0;

    virtual void SetPlaneOffset(VideoPlane plane, uint32_t offset) = 0;
    virtual uint32_t PlaneOffset(VideoPlane plane) = 0;

    virtual void SetStride(VideoPlane plane, uint32_t stride) = 0;
    virtual uint32_t Stride(VideoPlane plane) = 0;

    virtual void SetTimestamp(int64_t timestamp) = 0;
    virtual int64_t Timestamp() const = 0;

    public:
    VideoFrame() {}
    virtual ~VideoFrame() {}
};
