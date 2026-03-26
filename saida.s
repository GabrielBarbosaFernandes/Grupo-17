.text
.global _start

_start:
    @ Expressao 1 -> FLOAT
    ldr r0, =CONSTF_3_5
    vldr d0, [r0]
    ldr r1, =CONSTF_2_0
    vldr d1, [r1]
    vadd.f64 d2, d0, d1
    ldr r2, =RESULTADOF_1
    vstr d2, [r2]

    @ Expressao 2 -> FLOAT
    ldr r0, =CONSTF_10_0
    vldr d0, [r0]
    ldr r1, =CONSTF_4_0
    vldr d1, [r1]
    vsub.f64 d2, d0, d1
    ldr r2, =RESULTADOF_2
    vstr d2, [r2]

    @ Expressao 3 -> FLOAT
    ldr r0, =CONSTF_6_0
    vldr d0, [r0]
    ldr r1, =CONSTF_7_0
    vldr d1, [r1]
    vmul.f64 d2, d0, d1
    ldr r2, =RESULTADOF_3
    vstr d2, [r2]

    @ Expressao 4 -> FLOAT
    ldr r0, =CONSTF_8_0
    vldr d0, [r0]
    ldr r1, =CONSTF_2_0
    vldr d1, [r1]
    vdiv.f64 d2, d0, d1
    ldr r2, =RESULTADOF_4
    vstr d2, [r2]

    @ Expressao 5 -> MEMORIA MEM
    ldr r0, =2
    ldr r1, =MEM
    str r0, [r1]
    ldr r2, =RESULTADO_5
    str r0, [r2]

    @ Expressao 6 -> LE MEMORIA MEM
    ldr r0, =MEM
    ldr r1, [r0]
    ldr r2, =RESULTADO_6
    str r1, [r2]

    @ Expressao 7 -> RES
    ldr r0, =RESULTADO_6
    ldr r1, [r0]
    ldr r2, =RESULTADO_7
    str r1, [r2]

fim:
    b fim

@ ------------------------------
@ divisao inteira
@ entrada: r0 = dividendo, r1 = divisor
@ saida:   r2 = quociente
@ ------------------------------
rot_div:
    cmp r1, #0
    beq rot_div_zero
    mov r2, #0
    mov r3, r0
rot_div_loop:
    cmp r3, r1
    blt rot_div_fim
    sub r3, r3, r1
    add r2, r2, #1
    b rot_div_loop
rot_div_zero:
    mov r2, #0
rot_div_fim:
    bx lr

@ ------------------------------
@ resto da divisao
@ entrada: r0 = dividendo, r1 = divisor
@ saida:   r2 = resto
@ ------------------------------
rot_mod:
    cmp r1, #0
    beq rot_mod_zero
    mov r2, r0
rot_mod_loop:
    cmp r2, r1
    blt rot_mod_fim
    sub r2, r2, r1
    b rot_mod_loop
rot_mod_zero:
    mov r2, #0
rot_mod_fim:
    bx lr

@ ------------------------------
@ potencia inteira
@ entrada: r0 = base, r1 = expoente
@ saida:   r2 = resultado
@ ------------------------------
rot_pow:
    cmp r1, #0
    beq rot_pow_zero
    mov r2, r0
    sub r1, r1, #1
rot_pow_loop:
    cmp r1, #0
    beq rot_pow_fim
    mul r2, r2, r0
    sub r1, r1, #1
    b rot_pow_loop
rot_pow_zero:
    mov r2, #1
rot_pow_fim:
    bx lr

.data
MEM:
    .double 0.0
RESULTADO_1:
    .word 0
RESULTADO_2:
    .word 0
RESULTADO_3:
    .word 0
RESULTADO_4:
    .word 0
RESULTADO_5:
    .word 0
RESULTADO_6:
    .word 0
RESULTADO_7:
    .word 0
RESULTADOF_1:
    .double 0.0
RESULTADOF_2:
    .double 0.0
RESULTADOF_3:
    .double 0.0
RESULTADOF_4:
    .double 0.0
RESULTADOF_5:
    .double 0.0
RESULTADOF_6:
    .double 0.0
RESULTADOF_7:
    .double 0.0
CONSTF_3_5:
    .double 3.5
CONSTF_2_0:
    .double 2.0
CONSTF_10_0:
    .double 10.0
CONSTF_4_0:
    .double 4.0
CONSTF_6_0:
    .double 6.0
CONSTF_7_0:
    .double 7.0
CONSTF_8_0:
    .double 8.0
