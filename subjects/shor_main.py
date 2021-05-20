# -*- coding: utf-8 -*-
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

def controlled_mult_2mod15_quantum(qr,qc,control_qubit):
    """
    2 mod 15로 곱한 제어된 양자 회로
    노트: 제어 큐비트는 3보다 큰 인덱스여야 하고,
    큐비트 0,1,2,3은 회로 동작에 이미 예약되어 있다.
    """
    
    #0번째 큐비트와 3번째 큐비트를 교환
    qc.cswap(control_qubit,qr[0],qr[3])

    #0번째 큐비트와 1번째 큐비트를 교환
    qc.cswap(control_qubit,qr[1],qr[0])
    
    #1번째 큐비트와 2번째 큐비트를 교환
    qc.cswap(control_qubit,qr[1],qr[2])


def shors_subroutine_period_2mod15(qr,qc,cr):
    qc.x(qr[0])
    qc.h(qr[4])
    qc.h(qr[4])
    qc.measure(qr[4],cr[0])
    
    qc.h(qr[5])
    qc.cx(qr[5],qr[0])
    qc.cx(qr[5],qr[2])
    if cr[0]:
        qc.u1(math.pi/2,qr[4]) #pi/2는 호도로 90도다
    qc.h(qr[5])
    qc.measure(qr[5],cr[1])
    
    qc.h(qr[6])
    controlled_mult_2mod15_quantum(qr,qc,qr[6])
    if cr[1]:
        qc.u1(math.pi/2,qr[6]) # pi/2는 90도
    if cr[0]:
        qc.u1(math.pi/4,qr[6]) #pi/4 는 45도
    qc.h(qr[6])
    qc.measure(qr[6],cr[2])



def binary_string_to_decimal(s):
    dec=0
    for i in s[::-1]:
        if int(i):
            dec+=2**int(i)
    return dec

def run_shors_subroutine_period2_mod15():
    qr= QuantumRegister(7)
    cr= ClassicalRegister(3)
    qc= QuantumCircuit(qr,cr)
    #(측정 단계를 포함하는) 회로를 실행한다.
    shors_subroutine_period_2mod15(qr,qc,cr)
    import time
    from qiskit.tools.visualization import plot_histogram
    backend=Aer.get_backend('qasm_simulator')
    job_exp = qiskit.execute(qc,backend=backend,shots=1)
    result = job_exp.result()
    final =result.get_counts(qc)
    
    #최종 결과를 10진수로 변경한다.
    measurement=binary_string_to_decimal(list(final.keys())[0])
    period_r=period_from_quantum_measurement(measurement,3,2,15)
    return period_r


