section .data
  msg db 'Sum: %u', 10, 0

  arr dd 0, 254, 126, 126, 126, 126, 126, 126, 126, 254
  arr_len equ 10

section .text
  global main
  extern printf

  main:

    mov esi, arr
    mov ecx, arr_len

    xor ebx, ebx

  loop:
    mov eax, dword[esi]
    test eax, 10000000b
    jz summary

  not al

  summary:
    add ebx, eax

    add esi, 4
    dec ecx
    cmp ecx, 0

  jne loop

  push ebx
  push msg
  call printf

exit:
  mov eax, 01
  mov ebx, 0
  int 80h