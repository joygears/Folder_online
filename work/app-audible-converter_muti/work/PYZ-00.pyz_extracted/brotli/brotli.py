# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: brotli\brotli.py
import math, enum
from ._brotli import ffi, lib

class Error(Exception):
    __doc__ = '\n    Raised whenever an error is encountered with compressing or decompressing\n    data using brotlipy.\n\n    .. versionadded:: 0.5.1\n    '


error = Error

class BrotliEncoderMode(enum.IntEnum):
    __doc__ = '\n    Compression modes for the Brotli encoder.\n\n    .. versionadded:: 0.5.0\n    '
    GENERIC = lib.BROTLI_MODE_GENERIC
    TEXT = lib.BROTLI_MODE_TEXT
    FONT = lib.BROTLI_MODE_FONT


DEFAULT_MODE = BrotliEncoderMode(lib.BROTLI_DEFAULT_MODE)
MODE_GENERIC = BrotliEncoderMode.GENERIC
MODE_TEXT = BrotliEncoderMode.TEXT
MODE_FONT = BrotliEncoderMode.FONT

def decompress(data):
    """
    Decompress a complete Brotli-compressed string.

    :param data: A bytestring containing Brotli-compressed data.
    """
    d = Decompressor()
    data = d.decompress(data)
    d.finish()
    return data


def compress(data, mode=DEFAULT_MODE, quality=lib.BROTLI_DEFAULT_QUALITY, lgwin=lib.BROTLI_DEFAULT_WINDOW, lgblock=0, dictionary=b''):
    """
    Compress a string using Brotli.

    .. versionchanged:: 0.5.0
       Added ``mode``, ``quality``, `lgwin``, ``lgblock``, and ``dictionary``
       parameters.

    :param data: A bytestring containing the data to compress.
    :type data: ``bytes``

    :param mode: The encoder mode.
    :type mode: :class:`BrotliEncoderMode` or ``int``

    :param quality: Controls the compression-speed vs compression-density
        tradeoffs. The higher the quality, the slower the compression. The
        range of this value is 0 to 11.
    :type quality: ``int``

    :param lgwin: The base-2 logarithm of the sliding window size. The range of
        this value is 10 to 24.
    :type lgwin: ``int``

    :param lgblock: The base-2 logarithm of the maximum input block size. The
        range of this value is 16 to 24. If set to 0, the value will be set
        based on ``quality``.
    :type lgblock: ``int``

    :param dictionary: A pre-set dictionary for LZ77. Please use this with
        caution: if a dictionary is used for compression, the same dictionary
        **must** be used for decompression!
    :type dictionary: ``bytes``

    :returns: The compressed bytestring.
    :rtype: ``bytes``
    """
    compressor = Compressor(mode=mode,
      quality=quality,
      lgwin=lgwin,
      lgblock=lgblock,
      dictionary=dictionary)
    compressed_data = compressor._compress(data, lib.BROTLI_OPERATION_FINISH)
    if not lib.BrotliEncoderIsFinished(compressor._encoder) == lib.BROTLI_TRUE:
        raise AssertionError
    elif not lib.BrotliEncoderHasMoreOutput(compressor._encoder) == lib.BROTLI_FALSE:
        raise AssertionError
    return compressed_data


def _validate_mode(val):
    """
    Validate that the mode is valid.
    """
    try:
        val = BrotliEncoderMode(val)
    except ValueError:
        raise Error('%s is not a valid encoder mode' % val)


def _validate_quality(val):
    """
    Validate that the quality setting is valid.
    """
    if not 0 <= val <= 11:
        raise Error('%d is not a valid quality, must be between 0 and 11' % val)


def _validate_lgwin(val):
    """
    Validate that the lgwin setting is valid.
    """
    if not 10 <= val <= 24:
        raise Error('%d is not a valid lgwin, must be between 10 and 24' % val)


def _validate_lgblock(val):
    """
    Validate that the lgblock setting is valid.
    """
    if val != 0:
        if not 16 <= val <= 24:
            raise Error('%d is not a valid lgblock, must be either 0 or between 16 and 24' % val)


def _set_parameter(encoder, parameter, parameter_name, val):
    """
    This helper function sets a specific Brotli encoder parameter, checking
    the return code and raising :class:`Error <brotli.Error>` if it is
    invalid.
    """
    rc = lib.BrotliEncoderSetParameter(encoder, parameter, val)
    if parameter == lib.BROTLI_PARAM_MODE:
        _validate_mode(val)
    else:
        if parameter == lib.BROTLI_PARAM_QUALITY:
            _validate_quality(val)
        else:
            if parameter == lib.BROTLI_PARAM_LGWIN:
                _validate_lgwin(val)
            else:
                if parameter == lib.BROTLI_PARAM_LGBLOCK:
                    _validate_lgblock(val)
                else:
                    raise RuntimeError('Unexpected parameter!')
    if rc != lib.BROTLI_TRUE:
        raise Error('Error setting parameter %s: %d' % (parameter_name, val))


class Compressor(object):
    __doc__ = '\n    An object that allows for streaming compression of data using the Brotli\n    compression algorithm.\n\n    .. versionadded:: 0.5.0\n\n    :param mode: The encoder mode.\n    :type mode: :class:`BrotliEncoderMode` or ``int``\n\n    :param quality: Controls the compression-speed vs compression-density\n        tradeoffs. The higher the quality, the slower the compression. The\n        range of this value is 0 to 11.\n    :type quality: ``int``\n\n    :param lgwin: The base-2 logarithm of the sliding window size. The range of\n        this value is 10 to 24.\n    :type lgwin: ``int``\n\n    :param lgblock: The base-2 logarithm of the maximum input block size. The\n        range of this value is 16 to 24. If set to 0, the value will be set\n        based on ``quality``.\n    :type lgblock: ``int``\n\n    :param dictionary: A pre-set dictionary for LZ77. Please use this with\n        caution: if a dictionary is used for compression, the same dictionary\n        **must** be used for decompression!\n    :type dictionary: ``bytes``\n    '
    _dictionary = None
    _dictionary_size = None

    def __init__(self, mode=DEFAULT_MODE, quality=lib.BROTLI_DEFAULT_QUALITY, lgwin=lib.BROTLI_DEFAULT_WINDOW, lgblock=0, dictionary=b''):
        enc = lib.BrotliEncoderCreateInstance(ffi.NULL, ffi.NULL, ffi.NULL)
        if not enc:
            raise RuntimeError('Unable to allocate Brotli encoder!')
        enc = ffi.gc(enc, lib.BrotliEncoderDestroyInstance)
        _set_parameter(enc, lib.BROTLI_PARAM_MODE, 'mode', mode)
        _set_parameter(enc, lib.BROTLI_PARAM_QUALITY, 'quality', quality)
        _set_parameter(enc, lib.BROTLI_PARAM_LGWIN, 'lgwin', lgwin)
        _set_parameter(enc, lib.BROTLI_PARAM_LGBLOCK, 'lgblock', lgblock)
        if dictionary:
            self._dictionary = ffi.new('uint8_t []', dictionary)
            self._dictionary_size = len(dictionary)
            lib.BrotliEncoderSetCustomDictionary(enc, self._dictionary_size, self._dictionary)
        self._encoder = enc

    def _compress(self, data, operation):
        """
        This private method compresses some data in a given mode. This is used
        because almost all of the code uses the exact same setup. It wouldn't
        have to, but it doesn't hurt at all.
        """
        original_output_size = int(math.ceil(len(data) + (len(data) >> 2) + 10240))
        available_out = ffi.new('size_t *')
        available_out[0] = original_output_size
        output_buffer = ffi.new('uint8_t []', available_out[0])
        ptr_to_output_buffer = ffi.new('uint8_t **', output_buffer)
        input_size = ffi.new('size_t *', len(data))
        input_buffer = ffi.new('uint8_t []', data)
        ptr_to_input_buffer = ffi.new('uint8_t **', input_buffer)
        rc = lib.BrotliEncoderCompressStream(self._encoder, operation, input_size, ptr_to_input_buffer, available_out, ptr_to_output_buffer, ffi.NULL)
        if rc != lib.BROTLI_TRUE:
            raise Error('Error encountered compressing data.')
        elif not not input_size[0]:
            raise AssertionError
        size_of_output = original_output_size - available_out[0]
        return ffi.buffer(output_buffer, size_of_output)[:]

    def compress(self, data):
        """
        Incrementally compress more data.

        :param data: A bytestring containing data to compress.
        :returns: A bytestring containing some compressed data. May return the
            empty bytestring if not enough data has been inserted into the
            compressor to create the output yet.
        """
        return self._compress(data, lib.BROTLI_OPERATION_PROCESS)

    def flush(self):
        """
        Flush the compressor. This will emit the remaining output data, but
        will not destroy the compressor. It can be used, for example, to ensure
        that given chunks of content will decompress immediately.
        """
        chunks = []
        chunks.append(self._compress(b'', lib.BROTLI_OPERATION_FLUSH))
        while lib.BrotliEncoderHasMoreOutput(self._encoder) == lib.BROTLI_TRUE:
            chunks.append(self._compress(b'', lib.BROTLI_OPERATION_FLUSH))

        return (b'').join(chunks)

    def finish(self):
        """
        Finish the compressor. This will emit the remaining output data and
        transition the compressor to a completed state. The compressor cannot
        be used again after this point, and must be replaced.
        """
        chunks = []
        while lib.BrotliEncoderIsFinished(self._encoder) == lib.BROTLI_FALSE:
            chunks.append(self._compress(b'', lib.BROTLI_OPERATION_FINISH))

        return (b'').join(chunks)


class Decompressor(object):
    __doc__ = '\n    An object that allows for streaming decompression of Brotli-compressed\n    data.\n\n    .. versionchanged:: 0.5.0\n       Added ``dictionary`` parameter.\n\n    :param dictionary: A pre-set dictionary for LZ77. Please use this with\n        caution: if a dictionary is used for compression, the same dictionary\n        **must** be used for decompression!\n    :type dictionary: ``bytes``\n    '
    _dictionary = None
    _dictionary_size = None

    def __init__(self, dictionary=b''):
        dec = lib.BrotliDecoderCreateInstance(ffi.NULL, ffi.NULL, ffi.NULL)
        self._decoder = ffi.gc(dec, lib.BrotliDecoderDestroyInstance)
        if dictionary:
            self._dictionary = ffi.new('uint8_t []', dictionary)
            self._dictionary_size = len(dictionary)
            lib.BrotliDecoderSetCustomDictionary(self._decoder, self._dictionary_size, self._dictionary)

    def decompress(self, data):
        """
        Decompress part of a complete Brotli-compressed string.

        :param data: A bytestring containing Brotli-compressed data.
        :returns: A bytestring containing the decompressed data.
        """
        chunks = []
        available_in = ffi.new('size_t *', len(data))
        in_buffer = ffi.new('uint8_t[]', data)
        next_in = ffi.new('uint8_t **', in_buffer)
        while 1:
            buffer_size = 5 * len(data)
            available_out = ffi.new('size_t *', buffer_size)
            out_buffer = ffi.new('uint8_t[]', buffer_size)
            next_out = ffi.new('uint8_t **', out_buffer)
            rc = lib.BrotliDecoderDecompressStream(self._decoder, available_in, next_in, available_out, next_out, ffi.NULL)
            if rc == lib.BROTLI_DECODER_RESULT_ERROR:
                error_code = lib.BrotliDecoderGetErrorCode(self._decoder)
                error_message = lib.BrotliDecoderErrorString(error_code)
                raise Error('Decompression error: %s' % ffi.string(error_message))
            chunk = ffi.buffer(out_buffer, buffer_size - available_out[0])[:]
            chunks.append(chunk)
            if rc == lib.BROTLI_DECODER_RESULT_NEEDS_MORE_INPUT:
                assert available_in[0] == 0
                break
            else:
                if rc == lib.BROTLI_DECODER_RESULT_SUCCESS:
                    break
                else:
                    assert rc == lib.BROTLI_DECODER_RESULT_NEEDS_MORE_OUTPUT

        return (b'').join(chunks)

    def flush(self):
        """
        Complete the decompression, return whatever data is remaining to be
        decompressed.

        .. deprecated:: 0.4.0

            This method is no longer required, as decompress() will now
            decompress eagerly.

        :returns: A bytestring containing the remaining decompressed data.
        """
        return b''

    def finish(self):
        """
        Finish the decompressor. As the decompressor decompresses eagerly, this
        will never actually emit any data. However, it will potentially throw
        errors if a truncated or damaged data stream has been used.

        Note that, once this method is called, the decompressor is no longer
        safe for further use and must be thrown away.
        """
        assert lib.BrotliDecoderHasMoreOutput(self._decoder) == lib.BROTLI_FALSE
        if lib.BrotliDecoderIsFinished(self._decoder) == lib.BROTLI_FALSE:
            raise Error('Decompression error: incomplete compressed stream.')
        return b''