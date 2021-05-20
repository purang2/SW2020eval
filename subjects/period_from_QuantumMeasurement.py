# -*- coding: utf-8 -*-
[final Algorithm to measure the Period for Quantum Computing]

import math
def period_from_quantum_measurement(quantum_measurement,
                                   number_qubits,
                                   a_shor,
                                   N_shor,
                                   max_steps=100):
    """
    a_shor = 쇼어알고리즘의 일부로 선택된 임의의 숫자
    N_shor = 쇼어알고리즘이 인수분해하려는 숫자 
    """
    
    x1=quantum_measurement/2**number_qubits
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
            return all_qs[-1]
            
    