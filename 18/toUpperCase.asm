.model flat, c
option casemap :none
.code
toUpperCase	proc arg_0:DWORD
                 push    esi
                 mov     esi, arg_0
                 push    edi
                 mov     edi, esi
                 or      ecx, 0FFFFFFFFh
                 xor     eax, eax
                 repne scasb
                 not     ecx
                 dec     ecx
                 xor     edx, edx
                 test    ecx, ecx
                 jle     short loc_40102D

 loc_401018:                             
                 mov     al, [edx+esi]
                 cmp     al, 61h ; 'a'
                 jl      short loc_401028
                 cmp     al, 7Ah ; 'z'
                 jg      short loc_401028
                 sub     al, 20h ; ' '
                 mov     [edx+esi], al

 loc_401028:                            
                                         
                 inc     edx
                 cmp     edx, ecx
                 jl      short loc_401018

 loc_40102D:                             
                 pop     edi
                 pop     esi
                 ret
toUpperCase     endp
END 