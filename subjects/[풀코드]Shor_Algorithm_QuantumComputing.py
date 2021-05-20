# -*- coding: utf-8 -*-

%matplotlib inline
# Importing standard Qiskit libraries and configuring account
from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit.compiler import transpile, assemble
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from qiskit import *

from qiskit.visualization import plot_histogram
# Loading your IBM Q account(s)
provider = IBMQ.load_account()   


import math
import numpy

def period_from_quantum_measurement(quantum_measurement,
                                   number_qubits,
                                   a_shor,
                                   N_shor,
                                   max_steps=100):
    """
    a_shor = 쇼어알고리즘의 일부로 선택된 임의의 숫자
    N_shor = 쇼어알고리즘이 인수분해하려는 숫자 
    """
    
    xi=quantum_measurement/2**number_qubits
    # a와 xi 초기화
    all_as=[]
    all_xis=[]
    a_0=math.floor(xi)
    xi_0=xi-a_0
    all_as+=[a_0]
    all_xis+=[xi_0]
    # p, q 초기화
    all_ps=[]
    all_qs=[]
    p_0=all_as[0]
    q_0=1
    all_ps+=[p_0]
    all_qs+=[q_0]
    xi_n=xi_0
    while not numpy.isclose(xi_n,0,atol=-1e-7):
        if len(all_as)>=max_steps:
            print("Warning: algorithm did not converge within max_steps %d steps, try increasing max_steps" %max_steps)
            break
        #a와 xi 계산
        a_nplus1=math.floor(1/xi_n)
        xi_nplus1=1/xi_n-a_nplus1
        all_as+=[a_nplus1]
        all_xis+=[xi_nplus1]
        xi_n=xi_nplus1
                  
        #p와 q를 계산
        n=len(all_as)-1
        if n==1:
            p_1=all_as[1]*all_as[0]+1
            q_1=all_as[1]
            all_ps+=[p_1]
            all_qs+=[q_1]
        else:
            p_n=all_as[n]*all_ps[n-1]+all_ps[n-2]
            q_n=all_as[n]*all_qs[n-1]+all_qs[n-2]
            all_ps+=[p_n]
            all_qs+=[q_n]
        #q가 정답인지 확인
        # (첫번째 q는 사소한 경우로 생략함)
        if a_shor**all_qs[-1]%N_shor == 1 % N_shor:
            print("PERIOD = ", all_qs[-1])
            return all_qs[-1]
            
  from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
import time
from qiskit.tools.visualization import plot_histogram
  
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
    backend=Aer.get_backend('qasm_simulator')
    job_exp = qiskit.execute(qc,backend=backend,shots=1)
    result = job_exp.result()
    final =result.get_counts(qc)
    qc.draw(output='mpl') 
    #최종 결과를 10진수로 변경한다.
    measurement=binary_string_to_decimal(list(final.keys())[0])
    period_r=period_from_quantum_measurement(measurement,3,2,15)
    return period_r

def period_finding_quantum(a,N):
    #에제를 위해서 이 알고리즘을 완전하게 구현하지는 않을 것이며,
    #대신 한개의 선택된 a와 N을 가진 예제를 만든다.
    #이는 일반적인 경우로 확장이 가능하다
    
    if a==2 and N==15:
        return run_shors_subroutine_period2_mod15()
    else:
        raise Exception("Not implemented for N=%d, a=%d" %(N,a))

def shors_algorithm_quantum(N,fixed_a=None):
    assert(N>0)
    assert(int(N)==N)
    while True:
        
        if not fixed_a:
            a=random.randint(0,N-1)
        else:
            a=fixed_a
            
        g=math.gcd(a,N)
        if g!=1 or N==1:
            first_factor=g
            second_factor=int(N/g)
            return first_factor,second_factor
        else:
            r=period_finding_quantum(a,N)
            if not r:
                continue
            if r % 2 != 0:
                continue
            elif a**(int(r/2)) % N == -1 % N:
                continue
            else:
                first_factor=math.gcd(a**int(r/2)+1,N)
                second_factor=math.gcd(a**int(r/2)-1,N)
                if first_factor==N or second_factor==N:
                    continue
                if first_factor*second_factor!=N:
                    #결과를 확인한다
                    continue
                return first_factor,second_factor

#코드에서 직접 임의의 a값을 선택하도록 하는 경우에 알고리즘이 어떻게 동작하는지 확인하기 위해 시도한다.
t_start =time.time()
for a in range(15):
    #다음은 주어진 a에 대한 결과다:
    try:
        t1=time.time()    
        print("Result =%s with a randomly chosen a=%d" %(shors_algorithm_quantum(15,fixed_a=a),a),end=", ")
        t2=time.time()
        print("Each RunTime: ", t2-t1)
    except:
        print("ALGORITHM DOESN'T WORK with a randomly chosen a=%d" %a)
t_end =time.time()

print("--------------------------------")
print("start time:",t_start)
print("end time:", t_end)
print("RUN TIME(ms): ",t_end-t_start)